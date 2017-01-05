import pygame

from wiggler.core.code_handler import CodeHandler


class Controller(object):

    def __init__(self, resources):
        self.status = "menu-init"
        self.resources = resources
        self.elements = Elements(self.resources)
        self.sufficiency_level = 0
        self.update_user_code()

    def update_user_code(self):
        try:
            self.user_code = self.resources.project_def['controller_user_code']
        except KeyError:
            self.user_code = {
                'custom_update': ''
            }
        self.code_handler = CodeHandler(
            self.resources, 'controller', 'custom_controller', self.user_code,
            self.sufficiency_level)
        # Make controller custom_update a bound method for class controller
        custom_module = self.code_handler.module.controller_custom_update
        self.custom_update = custom_module.__get__(self, self.__class__)

    def populate(self):
        self.elements.empty()
        for name, character in self.resources.cast.characters.items():
            character.build_sprites()
            self.elements.add(character.sprites())

    def sweep(self):
        self.elements.empty()
        for character in self.resources.cast.characters.values():
            character.destroy_sprites()

    def update(self):
        self.custom_update()
        self.elements.update()
        self.collisions()
        self.elements.purge()
        return self.elements

    def collisions(self):
        collision_elements = self.elements.copy()
        collision_pairs = []
        for sprite in collision_elements:
            if not sprite.immutable:
                sprite.collisions['active'].empty()
        while collision_elements.sprites():
            sprite = collision_elements.sprites().pop(0)
            collision_elements.remove(sprite)
            collided = pygame.sprite.spritecollide(
                sprite,
                collision_elements,
                False
            )
            if not collided:
                continue
            for collided_sprite in collided:
                pair = set([sprite, collided_sprite])
                if pair in collision_pairs:
                    continue
                else:
                    collision_pairs.append(pair)
                point = None
                if collided_sprite.collisions['shape'] != "line" \
                        and sprite.collisions['shape'] != "line":
                    point = pygame.sprite.collide_mask(sprite, collided_sprite)
                elif collided_sprite.collisions['shape'] == "line" \
                        and sprite.collisions['shape'] != "line":
                    y = collided_sprite.m * sprite.centerx + collided_sprite.q
                    if y >= sprite.rect.y \
                       and y <= sprite.rect.y + sprite.rect.height:
                        point = pygame.sprite.collide_mask(
                            sprite,
                            collided_sprite
                        )
                elif collided_sprite.collisions['shape'] != "line" \
                        and sprite.collisions['shape'] == "line":
                    y = sprite.m * collided_sprite.centerx + sprite.q
                    if y >= collided_sprite.rect.y \
                       and y <= collided_sprite.rect.y \
                            + collided_sprite.rect.height:
                        point = pygame.sprite.collide_mask(
                            sprite,
                            collided_sprite
                        )
                if point:
                    if not sprite.immutable:
                        sprite.collisions['active'].add(collided_sprite)
                        sprite.collisions['points'][collided_sprite] = point
                    if not collided_sprite.immutable:
                        point = pygame.sprite.collide_mask(
                            collided_sprite,
                            sprite
                        )
                        collided_sprite.collisions['active'].add(sprite)
                        collided_sprite.collisions['points'][sprite] = point


class Elements(pygame.sprite.LayeredUpdates):

    def __init__(self, resources):
        self.resources = resources
        super(Elements, self).__init__()

    def purge(self):
        for sprite in self.sprites():
            if getattr(sprite, "destroyed", False):
                sprite.kill()
                try:
                    sprite.collisions['active'].empty()
                    sprite.collisions['handled'].empty()
                except AttributeError:
                    pass

                try:
                    sprite.parent.remove(sprite)
                except (TypeError, AttributeError):
                    pass


class Stage(object):

    def __init__(self, resources):
        self.resources = resources
        self.screen = None
        self.controller = Controller(self.resources)
        self.pause = False

    def start(self):
        pygame.init()
        self.resources.set_pygame_resources()
        self.screen = pygame.display.set_mode(self.resources.resolution)

    def toggle_pause(self):
        self.pause = not self.pause

    def reset(self):
        self.controller.sweep()
        self.controller.update_user_code()
        self.controller.populate()

    def sweep(self):
        self.controller.sweep()
        self.controller.update_user_code()

    def background_draw(self, background):
        if background.type == 'solid':
            self.screen.fill(background.color)
        elif background.type == 'image':
            self.screen.blit(background.image, (0, 0))

    def update(self):
        if self.pause:
            return
        else:
            self.resources.engine_events.update()
            self.resources.clock.tick()
            elements = self.controller.update()
            self.background_draw(self.resources.background)
            elements.draw(self.screen)
            pygame.event.pump()
            pygame.display.flip()
