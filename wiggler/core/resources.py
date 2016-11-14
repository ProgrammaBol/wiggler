import os
import yaml
import pkg_resources
import pygame

from wiggler.engine.factories.sounds import SoundChannels, Sound
from wiggler.engine.factories.sheets import Animation, Costume, Sheet
from wiggler.engine.factories.sprites import Sprite
from wiggler.engine.factories.templates import Template
from wiggler.engine.factories.characters import Character
from wiggler.core.factories.ui_images import UIimage
from wiggler.core.cast import Cast


class EventQueue(object):

    def __init__(self):
        self.subs = dict()
        self.subs["keyboard"] = dict()
        self.events = []

    def subscribe(self, source, e_type, e_id, callback, lock=False):
        if e_type not in self.subs[source]:
            self.subs[source][e_type] = dict()
        if e_id not in self.subs[source][e_type]:
            self.subs[source][e_type][e_id] = []
        event = self.subs[source][e_type][e_id]
        event.append(callback)

    def unsubscribe(self, source, e_type, e_id, callback):
        try:
            event = self.subs[source][e_type][e_id]
            event.remove(callback)
        except KeyError:
            pass

    def handle_events(self):
        while self.events:
            event = self.events.pop()
            if event.type == pygame.QUIT:
                return False
            try:
                callbacks = self.subs["keyboard"][event.type][event.key]
                for handler in callbacks:
                    handler(event)
            except KeyError:
                pass
        return True

    def update(self):
        for event in pygame.event.get():
            self.events.append(event)
        # TODO: Implement event passthrough
        # for event in wx.events
        #     self.events.append(event.translate)


class Resources(object):

    def __init__(self, library_basepath, project_basepath):

        self.clock = None
        # pygame resource
        self.resolution = None
        # self.main_event_queue = EventQueue()
        self.library_basepath = pkg_resources.resource_filename(
            'wiggler', library_basepath)
        self.project_basepath = project_basepath

        # directory resources
        self.library_paths = {}
        self.project_paths = {}
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
        for resource_type in self.types:
            self.library_paths[resource_type] = os.path.join(
                self.library_basepath, resource_type)
            self.project_paths[resource_type] = os.path.join(
                self.project_basepath, "resources", resource_type)
            setattr(self, resource_type, {})

        self.factories = {}
        # sounds
        self.factories['sounds'] = Sound
        self.factories['sheets'] = Sheet
        self.factories['costumes'] = Costume
        self.factories['animations'] = Animation
        self.factories['characters'] = Character
        self.factories['sprites'] = Sprite
        self.factories['templates'] = Template
        self.factories['ui_images'] = UIimage
        self.scan_resources(library=True)
        self.scan_resources()

        self.load_project_file()
        self.load_conf()
        self.cast = Cast(self)

    def set_pygame_resources(self):
        self.resolution = self.conf['stage_resolution']
        sound_channels = self.conf['sound_channels']
        reserved_channels = self.conf['reserved_channels']
        self.sound_channels = SoundChannels(sound_channels, reserved_channels)
        self.clock = pygame.time.Clock()
        self.events = EventQueue()

    def load_project_file(self):
        project_filename = os.path.join(self.project_basepath, "project.yaml")
        with open(project_filename) as project_file:
            self.project_definition = yaml.load(project_file.read())

    def load_conf(self):
        self.conf = {
            'sound_channels': 32,
            'reserved_channels': 4,
            'stage_resolution': (400, 400),
        }
        conf_filename = os.path.join(self.project_basepath, "conf.yaml")
        try:
            with open(conf_filename) as conf_file:
                self.conf = yaml.load(conf_file.read())
        except IOError:
            pass

    def save_metadata(self):
        for resource_type, type_def in self.types.items():
            meta_only = type_def['meta_only']
            resources = getattr(self, resource_type)
            save_data = []
            for resource_name, resource_definition in resources.items():
                if resource_definition.pop('library', False) \
                   and resource_definition.pop('modified', False):
                    metadata_filename = resource_type + os.extsep + "yaml"
                    metadata_path = os.path.join(
                        self.project_basepath, resource_type,
                        metadata_filename)
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
                self.project_basepath, resource_type, filename)
        resource_dict[resource_name] = definition
        resource = self.load_resource(resource_type, resource_name)
        return resource

    def save_resource(self, resource_definition, data):
        filename = resource_definition['abs_path']
        with open(filename, "w") as resource_file:
            resource_file.write(data)

    def load_metadata(self, filename):
        metadata = {}
        with open(filename) as metadata_file:
            try:
                for doc in yaml.load_all(metadata_file):
                    metadata.update(doc)
            except yaml.ScannerError:
                pass
        return metadata

    def scan_resource_type(self, resource_type, tree_walk, library=False):
        type_metadata = {}
        paths = self.project_paths
        if library is True:
            paths = self.library_paths
        type_path = paths[resource_type]
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
            if library:
                resource['library'] = True
            resource_attr[resource_name] = resource

    def load_resource(self, resource_type, resource_name):
        resource_def = getattr(self, resource_type)[resource_name]
        factory = self.factories[resource_type]
        content = factory(self, resource_name, resource_def)
        return content

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

    def scan_resources(self, library=False):
        tree_walk = {}
        base_path = self.project_basepath
        if library:
            base_path = self.library_basepath
        for root, dirs, files in os.walk(base_path):
            tree_walk[root] = (dirs, files)
        for resource_type in self.types:
            self.scan_resource_type(resource_type, tree_walk, library=library)
