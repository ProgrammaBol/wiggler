import os
import yaml
import pkg_resources
import pygame

from wiggler.engine.factories.sounds import SoundChannels, Sound
from wiggler.engine.factories.sheets import Animation, Costume, Sheet
from wiggler.engine.factories.sprites import Sprite
from wiggler.engine.events import EventQueue
from wiggler.core.factories.templates import Template
from wiggler.core.factories.characters import Character
from wiggler.core.factories.ui_images import UIimage
from wiggler.core.cast import Cast
from wiggler.core.project import Project
from wiggler.core.datastructures import OverlayDict


class Resources(object):

    def __init__(self):

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
        self.types = set(
            ['sounds', 'sheets', 'sprites', 'images', 'musics', 'fonts',
             'animations', 'costumes', 'templates', 'characters',
             'ui_images'])
        for resource_type in self.types:
            setattr(self, resource_type, OverlayDict())
        library_basepath = pkg_resources.resource_filename('wiggler',
                                                           "resources")

        self.scan_tree(library_basepath)
        # Switch all the dicts to overlay
        for resource_type in self.types:
            res_attr = getattr(self, resource_type)
            res_attr.switch = "both"
        self.new_project()

        # TODO: move to project
        self.cast = Cast(self)

        # pygame resources
        self.clock = None
        self.resolution = None

    @staticmethod
    def load_metadata(base_path, filename):
        metadata = {}
        file_path = os.path.join(base_path, filename)
        with open(file_path) as metadata_file:
            try:
                for doc in yaml.load_all(metadata_file):
                    metadata.update(doc)
            except yaml.ScannerError:
                pass
        return metadata

    @staticmethod
    def load_file_resource(type_path, filename, metadata=None):
        resource = {}
        resource['abs_path'] = os.path.join(type_path, filename)
        resource_name, resource_ext = os.path.splitext(filename)
        if metadata is not None:
            resource.update(metadata)
            try:
                resource_name = metadata.pop('name')
            except KeyError:
                pass
        return resource_name, resource

    def scan_tree(self, base_path):
        tree_walk = {}
        for root, dirs, files in os.walk(base_path):
            tree_walk[root] = (dirs, files)
        avail_fileres, metadata_files = tree_walk.pop(base_path)
        metadata_paths = {}
        for filename in metadata_files:
            name, ext = os.path.splitext(filename)
            if ext == ".yaml":
                metadata_paths[name] = filename
        avail_metadata = metadata_paths.keys()
        # Validation, only valid resources will be taken into consideration
        avail_fileres = set(avail_fileres).intersection(self.types)
        avail_metadata = set(avail_metadata).intersection(self.types)
        self.load_metaonly_res(
            base_path, avail_fileres, avail_metadata, metadata_paths)
        self.load_fileonly_res(
            base_path, tree_walk, avail_fileres, avail_metadata)
        self.load_filemeta_res(
            base_path, tree_walk, avail_fileres, avail_metadata,
            metadata_paths)

    def load_metaonly_res(self, base_path, avail_fileres, avail_metadata,
                          metadata_paths):
        # metadata-only resources
        metaonly_res = avail_metadata - avail_fileres
        for resource_type in metaonly_res:
            metadata = self.load_metadata(
                base_path, metadata_paths[resource_type])
            resource_attr = getattr(self, resource_type)
            resource_attr.update(metadata)

    def load_fileonly_res(self, base_path, tree_walk, avail_fileres,
                          avail_metadata):
        # file only resources
        file_only_resources = avail_fileres - avail_metadata
        for resource_type in file_only_resources:
            resource_attr = getattr(self, resource_type)
            type_path = os.path.join(base_path, resource_type)
            void, file_list = tree_walk[type_path]
            for filename in file_list:
                resource_name, resource = self.load_file_resource(
                    type_path, filename)
                resource_attr[resource_name] = resource

    def load_filemeta_res(self, base_path, tree_walk, avail_fileres,
                          avail_metadata, metadata_paths):
        # file resources with metadata
        file_and_meta_res = avail_fileres.intersection(avail_metadata)
        for resource_type in file_and_meta_res:
            resource_attr = getattr(self, resource_type)
            type_path = os.path.join(base_path, resource_type)
            void, file_list = tree_walk[type_path]
            for filename in file_list:
                metadata = self.load_metadata(
                    base_path, metadata_paths[resource_type])
                try:
                    resource_metadata = metadata[filename]
                except KeyError:
                    resource_metadata = None
                resource_name, resource = self.load_file_resource(
                    type_path, filename, metadata=resource_metadata)
                resource_attr[resource_name] = resource

    def set_pygame_resources(self):
        self.resolution = self.conf['stage_resolution']
        sound_channels = self.conf['sound_channels']
        reserved_channels = self.conf['reserved_channels']
        self.sound_channels = SoundChannels(sound_channels, reserved_channels)
        self.clock = pygame.time.Clock()
        self.events = EventQueue()

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

    def new_project(self):
        self.load_project(filename=None)

    def load_project(self, filename):
        if hasattr(self, "project"):
            if self.project.needs_save:
                pass
            self.project.cleanup()
        self.project = Project(filename=filename)
        self.scan_tree(self.project.temp_dir)

    def save_project(self, filename):
        self.project.save(filename)

    def new_resource(self, resource_type, name, definition):
        res_dict = getattr(self, resource_type)

        try:
            filename = definition.pop('filename')
            data = definition.pop('data')
            definition['abs_path'] = os.path.join(
                self.project.temp_dir, resource_type, filename)
            filename = definition['abs_path']
            with open(filename, "w") as resource_file:
                resource_file.write(data)
        except KeyError:
            pass
        res_dict[name] = definition

        resource = self.load_resource(resource_type, name)
        return resource

    def save_resource(self, res_type, definition):
        try:
            filename = definition.pop('abs_path')
            data = definition.pop('data')
            with open(filename, "w") as resource_file:
                resource_file.write(data)
        except KeyError:
            pass

        # This part should rewrite metadata file
        # res_dict = getattr(self, resource_type)
        # save_data = []
        # for resource_name, resource_definition in res_dict.items():
        #    metadata_filename = resource_type + os.extsep + "yaml"
        #    metadata_path = os.path.join(
        #        self.project.temp_dir, resource_type, metadata_filename)
        #    if meta_only is True:
        #        resource_data = {resource_name: resource_definition}
        #    else:
        #        resource_filename = os.path.basename(
        #            resource_definition['abs_path'])
        #        resource_data = {
        #            resource_filename: resource_definition}
        #    save_data.append(resource_data)
        # yaml.dump_all(save_data, metadata_path)

    def load_resource(self, resource_type, resource_name):
        resource_def = getattr(self, resource_type)[resource_name]
        factory = self.factories[resource_type]
        instance = factory(self, resource_name, resource_def)
        return instance

    def remove_resource(self, resource_type, name):
        res_dict = getattr(self, resource_type)
        del res_dict[name]

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
