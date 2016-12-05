import copy
import os
import yaml
import pkg_resources
import pygame
import tempfile

from wiggler.engine.factories.sounds import SoundChannels, Sound
from wiggler.engine.factories.sheets import Animation, Costume, Sheet
from wiggler.engine.factories.sprites import Sprite
from wiggler.engine.events import EventQueue
from wiggler.core.factories.templates import Template
from wiggler.core.factories.characters import Character
from wiggler.core.factories.ui_images import UIimage
from wiggler.core.cast import Cast


class ResourcesTree(object):

    def __init__(self, base_path, types):
        self.base_path = base_path
        self.types = types

        self.paths = {}
        for resource_type in self.types:
            self.paths[resource_type] = os.path.join(base_path, resource_type)
            setattr(self, resource_type, {})

        tree_walk = {}
        for root, dirs, files in os.walk(self.base_path):
            tree_walk[root] = (dirs, files)
        for resource_type in self.types:
            self.scan_resource_type(resource_type, tree_walk)

    @staticmethod
    def load_metadata(filename):
        metadata = {}
        with open(filename) as metadata_file:
            try:
                for doc in yaml.load_all(metadata_file):
                    metadata.update(doc)
            except yaml.ScannerError:
                pass
        return metadata

    def scan_resource_type(self, resource_type, tree_walk):
        type_metadata = {}
        type_path = self.paths[resource_type]
        resource_attr = getattr(self, resource_type)
        try:
            void, resources_list = tree_walk[type_path]
        except KeyError:
            return
        type_metadata_filename = os.extsep.join([resource_type, "yaml"])
        type_metadata_path = os.path.join(type_path, type_metadata_filename)
        try:
            resources_list.pop(resources_list.index(type_metadata_filename))
            type_metadata = self.load_metadata(type_metadata_path)
        except (IndexError, ValueError):
            pass
        meta_only = self.types[resource_type]['meta_only']
        if meta_only:
            resource_attr.update(type_metadata)
            return
        for resource_file in resources_list:
            resource = {}
            resource_path = os.path.join(type_path, resource_file)
            resource_name, resource_ext = os.path.splitext(resource_file)
            try:
                resource_metadata = type_metadata[resource_file]
                try:
                    resource_name = resource_metadata.pop('name')
                except KeyError:
                    pass
                resource.update(resource_metadata)
            except KeyError:
                pass

            resource['abs_path'] = os.path.join(resource_path)
            resource_attr[resource_name] = resource

    def save_metadata(self):
        for resource_type, type_def in self.types.items():
            meta_only = type_def['meta_only']
            resources = getattr(self, resource_type)
            save_data = []
            for resource_name, resource_definition in resources.items():
                if resource_definition.pop('modified', False):
                    metadata_filename = resource_type + os.extsep + "yaml"
                    metadata_path = os.path.join(
                        self.base_path, resource_type, metadata_filename)
                    if meta_only is True:
                        resource_data = {resource_name: resource_definition}
                    else:
                        resource_filename = os.path.basename(
                            resource_definition['abs_path'])
                        resource_data = {
                            resource_filename: resource_definition}
                    save_data.append(resource_data)
            yaml.dump_all(save_data, metadata_path)

    def new_resource(self, resource_type, resource_name, definition):
        resource_dict = getattr(self, resource_type)
        meta_only = self.types[resource_type]['meta_only']
        if meta_only is False:
            filename = definition.pop('filename')
            definition['abs_path'] = os.path.join(
                self.base_path, resource_type, filename)
        resource_dict[resource_name] = definition

    def save_resource(self, resource_definition, data):
        filename = resource_definition['abs_path']
        with open(filename, "w") as resource_file:
            resource_file.write(data)


class Resources(object):

    def __init__(self):

        self.types = {'sounds': {'meta_only': False},
                      'sheets': {'meta_only': False},
                      'sprites': {'meta_only': True},
                      'images': {'meta_only': False},
                      'musics': {'meta_only': False},
                      'fonts': {'meta_only': False},
                      'animations': {'meta_only': True},
                      'costumes': {'meta_only': True},
                      'templates': {'meta_only': False},
                      'characters': {'meta_only': True},
                      'ui_images': {'meta_only': False},
                      }

        # self.main_event_queue = EventQueue()
        self.factories = {}
        self.factories['sounds'] = Sound
        self.factories['sheets'] = Sheet
        self.factories['costumes'] = Costume
        self.factories['animations'] = Animation
        self.factories['characters'] = Character
        self.factories['sprites'] = Sprite
        self.factories['templates'] = Template
        self.factories['ui_images'] = UIimage

        self.load_conf()
        library_basepath = pkg_resources.resource_filename('wiggler',
                                                           "resources")

        self.library = ResourcesTree(library_basepath, self.types)
        self.project = None
        self.set_dicts()

        self.cast = Cast(self)

        # pygame resources
        self.clock = None
        self.resolution = None

    def set_dicts(self):
        for resource_type in self.types:
            d = copy.copy(getattr(self.library, resource_type))
            if self.project is not None:
                d.update(getattr(self.project, resource_type))
            setattr(self, resource_type, d)

    def remove_resource(self, resource_type, name):
        d = getattr(self, resource_type)
        if self.project is not None:
            dp = getattr(self.project, resource_type)
            del dp[name]
        dl = getattr(self.library, resource_type)
        try:
            d[name] = copy.copy(dl[name])
        except KeyError:
            del d[name]

    def new_resource(self, resource_type, name, definition):
        d = getattr(self, resource_type)
        if self.project is not None:
            dp = getattr(self.project, resource_type)
        self.project.new_resource(resource_type, name, definition)
        d[name] = copy.copy(dp[name])
        resource = self.load_resource(resource_type, name)
        return resource

    def load_resource(self, resource_type, resource_name):
        resource_def = getattr(self, resource_type)[resource_name]
        factory = self.factories[resource_type]
        instance = factory(self, resource_name, resource_def)
        return instance

    def set_pygame_resources(self):
        self.resolution = self.conf['stage_resolution']
        sound_channels = self.conf['sound_channels']
        reserved_channels = self.conf['reserved_channels']
        self.sound_channels = SoundChannels(sound_channels, reserved_channels)
        self.clock = pygame.time.Clock()
        self.events = EventQueue()

    def create_new_project(self, name=None):
        if name is None:
            name = "untitled1"
        project_dir = tempfile.mkdtemp(prefix="wiggler-")
        os.mkdir(os.path.join(project_dir, "resources"))
        project_def = {
            'name': name,
            'characters': None,
            'background': None,
        }
        with open(os.path.join(project_dir,
                               "project.yaml"), "w") as project_file:
            yaml.dump(project_def, project_file)
        self.load_project(project_dir=project_dir)

    def load_project(self, project_filename=None, project_dir=None):
        if project_filename is not None:
            # unzip project file to project_dir
            pass
        self.project = ResourcesTree(os.path.join(project_dir,
                                                  "resources"), self.types)
        try:
            projectdef_filename = os.path.join(project_dir,
                                               "project.yaml")
            with open(projectdef_filename) as project_file:
                self.project_definition = yaml.load(project_file.read())
        except IOError:
            pass
        self.set_dicts()

    def load_conf(self):
        self.conf = {
            'sound_channels': 32,
            'reserved_channels': 4,
            'stage_resolution': (400, 400),
            'library_reldir': "resources"
        }
        # conf_filename = os.path.join(self.project_basepath, "conf.yaml")
        # try:
        #    with open(conf_filename) as conf_file:
        #        self.conf = yaml.load(conf_file.read())
        # except IOError:
        #    pass

    def load_ui_images(self, ui_image_name):
        return self.load_resource('ui_images', ui_image_name)

    def load_sound(self, sound_name):
        return self.load_resource("sounds", sound_name)

    def load_sheet(self, sheet_name):
        return self.load_resource('sheets', sheet_name)

    def load_sheet_by_filename(self, filename):
        for sheetname, definition in self.sheets.items():
            if os.path.basename(definition['abs_path']) == filename:
                return self.load_sheet(sheetname)
