import copy
import os
import pkg_resources
import pygame
import shutil
import tempfile
import yaml

from wiggler.core.cast import Cast
from wiggler.core.datastructures import OverlayDict
from wiggler.core.factories.characters import Character
from wiggler.core.factories.projectres import ProjectRes
from wiggler.core.factories.templates import Template
from wiggler.core.factories.ui_images import UIimage
from wiggler.core.self_sufficiency import SelfSufficiency
from wiggler.engine.background import Background
from wiggler.engine.events import EventQueue
from wiggler.engine.factories.images import Image
from wiggler.engine.factories.sheets import Animation, Costume, Sheet
from wiggler.engine.factories.sounds import SoundChannels, Sound
from wiggler.engine.factories.sprites import SpriteBuilder


class Resources(object):

    def __init__(self):

        # self.main_event_queue = EventQueue()
        self.factories = {}
        self.factories['sounds'] = Sound
        self.factories['sheets'] = Sheet
        self.factories['costumes'] = Costume
        self.factories['animations'] = Animation
        self.factories['characters'] = Character
        self.factories['sprites'] = SpriteBuilder
        self.factories['templates'] = Template
        self.factories['ui_images'] = UIimage
        self.factories['images'] = Image

        self.load_conf()
        self.types = set(
            ['sounds', 'sheets', 'sprites', 'images', 'musics', 'fonts',
             'animations', 'costumes', 'templates', 'characters',
             'ui_images'])
        self.modules_dir = None
        self.reset_modules_dir()
        self.instances = None
        self.reset_instances()
        for resource_type in self.types:
            setattr(self, resource_type, OverlayDict())
        library_basepath = pkg_resources.resource_filename('wiggler',
                                                           "resources")

        self.meta_files = OverlayDict()
        self.scan_tree(library_basepath)
        # Switch all the dicts to overlay
        for resource_type in self.types:
            res_attr = getattr(self, resource_type)
            res_attr.switch = "both"
        self.meta_files.switch = "both"
        self.projectres = None
        self.project_def = None

        # pygame resources
        self.clock = None
        self.resolution = None
        self.cast = Cast(self)
        self.engine_events = None
        self.background = Background(self)

        self.selfsuff = SelfSufficiency(self)

    def reset_instances(self):
        self.instances = {}
        for resource_type in self.types:
            self.instances[resource_type] = {}

    def reset_modules_dir(self):
        if self.modules_dir is not None:
            shutil.rmtree(self.modules_dir)
        self.modules_dir = tempfile.mkdtemp(prefix="wiggler-modules-")
        self.module_dirs = {}
        for resource_type in self.types:
            module_dir = os.path.join(self.modules_dir, resource_type)
            os.mkdir(module_dir)
            self.module_dirs[resource_type] = module_dir
        self.controller_module = os.path.join(self.modules_dir,
                                              "controller.py")

    def reset_overlays(self):
        for resource_type in self.types:
            res_attr = getattr(self, resource_type)
            res_attr.reset_overlay()
        self.meta_files.reset_overlay()

    def load_metadata_file(self, resource_type):
        metadata = {}
        file_path = self.meta_files[resource_type]
        try:
            metadata_file = open(file_path)
        except IOError:
            return metadata

        try:
            for resource in yaml.safe_load_all(metadata_file):
                if 'name' in resource:
                    name = resource['name']
                elif 'file' in resource:
                    name, __ = os.path.splitext(resource['file'])
                else:
                    # log error: cannot find name for resource
                    continue
                resource['modified'] = False
                metadata[name] = resource
        except yaml.ScannerError:
            pass
        return metadata

    def scan_tree(self, base_path, reset=False):
        if reset:
            self.reset_overlays()
        tree_walk = {}
        for root, dirs, files in os.walk(base_path):
            tree_walk[root] = (dirs, files)
        fileres_dirs, metadata_files = tree_walk.pop(base_path)

        for resource_type in self.types:
            filename = resource_type + os.path.extsep + "yaml"
            meta_path = os.path.join(base_path, filename)
            self.meta_files[resource_type] = meta_path

            resource_attr = getattr(self, resource_type)
            metadata = self.load_metadata_file(resource_type)
            resource_attr.update(metadata)

        for resource_type in fileres_dirs:
            try:
                resource_attr = getattr(self, resource_type)
            except AttributeError:
                continue

            type_path = os.path.join(base_path, resource_type)
            __, file_list = tree_walk[type_path]
            for filename in file_list:
                name = None
                for resource_name, resource in resource_attr.items():
                    if resource.get('file', None) == filename:
                        name = resource_name
                        break
                if name is None:
                    name, __ = os.path.splitext(filename)
                    resource_attr[name] = {}

                abs_path = os.path.join(type_path, filename)
                resource_attr[name]['abs_path'] = abs_path
                resource_attr[name]['modified'] = False

    def set_pygame_resources(self):
        self.resolution = self.conf['stage_resolution']
        sound_channels = self.conf['sound_channels']
        reserved_channels = self.conf['reserved_channels']
        self.sound_channels = SoundChannels(sound_channels, reserved_channels)
        self.clock = pygame.time.Clock()
        self.engine_events = EventQueue()

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

    def change_default_background(self, back_type, back_spec):
        background_def = {
            'type': back_type,
        }
        if back_type == "solid":
            background_def['color'] = back_spec
        elif back_type == "image":
            background_def['image_name'] = back_spec
        self.project_def['background'] = background_def

    def create_new_project(self, project_def=None):
        if self.projectres is not None:
            self.projectres.cleanup()
        self.projectres = ProjectRes()
        project_def = self.projectres.create_new(project_def)
        self.scan_tree(self.projectres.resources_dir, reset=True)
        self.reset_modules_dir()
        self.reset_instances()
        self.project_def = project_def
        return project_def

    def load_project(self, filename):
        if self.projectres is not None:
            self.projectres.cleanup()
        self.projectres = ProjectRes()
        project_def = self.projectres.load(filename=filename)
        self.scan_tree(self.projectres.resources_dir, reset=True)
        self.reset_modules_dir()
        self.reset_instances()
        self.project_def = project_def
        return project_def

    def cleanup(self):
        shutil.rmtree(self.modules_dir)
        if self.projectres is not None:
            self.projectres.cleanup()

    def import_resources(self, filename):
        '''Merge a resources file with current resources tree'''
        pass

    def save_project(self, filename):
        if self.projectres is not None:
            for resource_type in self.types:
                self.save_resources(resource_type, save_all=True)
            self.projectres.save(filename)

    def add_resource(self, resource_type, name, definition,
                     source_file=None):
        res_dict = getattr(self, resource_type)
        if source_file is not None:
            __, ext = os.path.splitext(source_file)
            res_dir = os.path.join(self.projectres.resources_dir,
                                   resource_type, "")
            try:
                os.mkdir(res_dir)
            except OSError:
                pass
            definition['abs_path'] = res_dir + name + ext
            definition['file'] = name + ext
            shutil.copy(source_file, definition['abs_path'])
        res_dict[name] = definition

        self.save_resources(resource_type, name=name, save_all=False)

        resource = self.load_resource(resource_type, name)
        return resource

    def find_deps(self, resource_type, name):
        # hard deps
        # costumes -> sheets
        # animations -> sheets
        # soft_deps
        # character -> sprites
        # sprite -> costumes
        # sprite -> sounds
        # sprite -> animations
        hard_deps = set()
        soft_deps = set()
        if resource_type == 'sheets':
            abs_path = getattr(self, 'sheets')[name]['abs_path']
            sheet_file = os.path.basename(abs_path)
            for costume_name, costume_def in getattr(self, 'costumes').items():
                if costume_def['sheet'] == sheet_file:
                    hard_deps.update(set([('costumes', costume_name)]))
                    hard, soft = self.find_deps('costumes', costume_name)
                    hard_deps.update(hard)
                    soft_deps.update(soft)
            animations = getattr(self, 'animations').items()
            for animation_name, animation_def in animations:
                if animation_def['sheet'] == sheet_file:
                    hard_deps.update(set([('animations', animation_name)]))
                    hard, soft = self.find_deps('animations', animation_name)
                    hard_deps.update(hard)
                    soft_deps.update(soft)
        elif resource_type == 'costumes':
            for sprite_name, sprite_def in getattr(self, 'sprites').items():
                if name in sprite_def['costumes']:
                    soft_deps.update(set([('sprites', sprite_name)]))
                    __, soft = self.find_deps('sprites', sprite_name)
                    soft_deps.update(soft)
        elif resource_type == 'sounds':
            for sprite_name, sprite_def in getattr(self, 'sprites').items():
                if name in sprite_def['sounds']:
                    soft_deps.update(set([('sprites', name)]))
                    __, soft = self.find_deps('sprites', sprite_name)
                    soft_deps.update(soft)
        elif resource_type == 'animations':
            for sprite_name, sprite_def in getattr(self, 'sprites').items():
                if name in sprite_def['animations']:
                    soft_deps.update(set([('sprites', name)]))
                    __, soft = self.find_deps('sprites', sprite_name)
                    soft_deps.update(soft)
        elif resource_type == 'sprites':
            for character_name, character_def in \
                    getattr(self, 'characters').items():
                if name in character_def['sprites']:
                    soft_deps.update(set([('sprites', name)]))

        return list(hard_deps), list(soft_deps)

    def remove_resource(self, resource_type, name):
        res_dict = getattr(self, resource_type)
        definition = res_dict[name]
        if not res_dict.is_overlay(name):
            # library resources cannot be removed
            return
        try:
            os.unlink(definition['abs_path'])
        except KeyError:
            pass
        resource_type_metadata = self.load_metadata_file(resource_type)
        del resource_type_metadata[name]
        self.save_metadata(resource_type, resource_type_metadata)
        del res_dict[name]
        if not res_dict:
            res_dir = os.path.join(self.projectres.resources_dir,
                                   resource_type, "")
            os.rmdir(res_dir)

    def save_resources(self, resource_type, name=None, save_all=False):
        resource_type_metadata = {}

        if save_all:
            resource_attr = getattr(self, resource_type)
            for name, __ in resource_attr.items():
                resource_def = self.save_resource_file(resource_type, name)
                if resource_def:
                    resource_type_metadata[name] = resource_def
        elif name is not None:
            resource_type_metadata = self.load_metadata_file(resource_type)
            resource_def = self.save_resource_file(resource_type, name)
            if resource_def:
                resource_type_metadata[name] = resource_def

        if resource_type_metadata:
            self.save_metadata(resource_type, resource_type_metadata)

    def save_metadata(self, resource_type, resource_type_metadata):
        save_data = []
        for __, definition in resource_type_metadata.items():
            save_data.append(definition)
        metadata_path = self.meta_files[resource_type]
        if save_data:
            with open(metadata_path, "w") as metadata_file:
                yaml.safe_dump_all(
                    save_data, metadata_file, indent=4,
                    default_flow_style=False)
        else:
            os.unlink(metadata_path)

    def save_resource_file(self, resource_type, name):
        resource_attr = getattr(self, resource_type)
        definition = copy.copy(resource_attr[name])
        if 'modified' not in definition or not definition.pop('modified'):
            return {}
        abs_path = None
        if 'abs_path' in definition:
            abs_path = definition.pop('abs_path')
            try:
                data = definition.pop('data')
                with open(abs_path, "w") as resource_file:
                    resource_file.write(data)
            except KeyError:
                pass

            fileres_filename = os.path.basename(abs_path)
            fileres_defaultname, __ = os.path.splitext(fileres_filename)
            if name != fileres_defaultname:
                # the file resource has a been assigned a name different
                # from the default name from filename
                # we need to report it into metadata
                definition['name'] = name

        return definition

    def load_resource(self, resource_type, resource_name):
        module_dir = self.module_dirs[resource_type]
        module_file = os.path.join(module_dir,
                                   resource_name + os.extsep + "py")
        resource_def = getattr(self, resource_type)[resource_name]
        factory = self.factories[resource_type]
        instance = factory(self, resource_name, resource_def,
                           events=self.engine_events,
                           module_file=module_file)
        self.instances[resource_type][resource_name] = instance
        return instance

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
