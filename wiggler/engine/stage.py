import pygame


class Stage(object):

    def __init__(self, resources):
        self.resources = resources
        self.players = dict()
        self.status = "menu-init"
        self.screen = None
        self.elements = pygame.sprite.LayeredUpdates()
        self.sprite_groups = dict()
        self.pause = False
        # self.event_queue.subscribe("keyboard",
        #                           pygame.KEYDOWN,
        #                           pygame.K_p,
        #                           self.toggle_pause)
        self.currentstatus_elements = dict()

    def start(self):
        pygame.init()
        self.resources.set_pygame_resources()
        self.screen = pygame.display.set_mode(self.resources.resolution)

    def toggle_pause(self):
        self.pause = not self.pause

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

    def set_background(self):
        # load resourc images, let it support crop
        pass

    def populate(self):
        self.elements.empty()
        for name, character in self.resources.cast.characters.items():
            character.build_sprites()
            self.elements.add(character.sprites())

    def sweep(self):
        self.elements.empty()
        for character in self.resources.cast:
            character.destroy_sprites()

    def update(self):
        self.resources.events.update()
        self.resources.clock.tick()
        self.screen.fill((255, 255, 255))
        # pygame.draw.circle(self.screen, (250, 0, 0), (100, 100), 50)
        # screen.fill(default_backcolor)
        # screen.blit(background_image, (0, 0))
        background_change, \
            background, \
            screen_elements = self.elements_update()
        # screen_elements.draw(screen)
        self.elements.draw(self.screen)
        pygame.event.pump()
        pygame.display.flip()
        # clock.tick(max_fps)

    def elements_update(self):
        if self.pause:
            return False, None, self.elements
        for sprite in self.elements.sprites():
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

        self.elements.update()

        return False, None, self.elements
