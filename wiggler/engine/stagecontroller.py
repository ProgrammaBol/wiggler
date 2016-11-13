import pygame
import pprint
from engine.maps import RoomMap, WorldMap
# levels (roomid)


def weightedcollide():
    pass


class StageController(object):

    def __init__(self, event_queue, game_context):
        self.players = dict()
        self.status = "menu-init"
        self.worldmap = WorldMap(game_context, (1, 5))
        self.elements = pygame.sprite.LayeredUpdates()
        self.event_queue = event_queue
        self.clock = game_context.clock
        self.resolution = game_context.resolution
        self.game_context = game_context
        self.sprite_groups = dict()
        self.pause = False
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYDOWN,
                                   pygame.K_p,
                                   self.toggle_pause)
        self.currentstatus_elements = dict()

    def toggle_pause(self):
        self.pause = not self.pause

    def init_controls(self, controls_config):
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYDOWN,
                                   pygame.K_LEFT,
                                   self.players["player_one"].keypress_left)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYUP,
                                   pygame.K_LEFT,
                                   self.players["player_one"].keyrelease_left)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYDOWN,
                                   pygame.K_RIGHT,
                                   self.players["player_one"].keypress_right)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYUP,
                                   pygame.K_RIGHT,
                                   self.players["player_one"].keyrelease_right)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYDOWN,
                                   pygame.K_UP,
                                   self.players["player_one"].keypress_up)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYUP,
                                   pygame.K_UP,
                                   self.players["player_one"].keyrelease_up)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYUP,
                                   pygame.K_DOWN,
                                   self.players["player_one"].keyrelease_down)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYDOWN,
                                   pygame.K_SPACE,
                                   self.players["player_one"].keypress_space)
        self.event_queue.subscribe("keyboard",
                                   pygame.KEYUP,
                                   pygame.K_SPACE,
                                   self.players["player_one"].keyrelease_space)

    def collisions(self):
        collision_elements = self.elements.copy()
        collision_pairs = []
        for sprite in collision_elements:
            if not sprite.immutable:
                sprite.active_collisions.empty()
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
                if collided_sprite.shape != "line" and sprite.shape != "line":
                    point = pygame.sprite.collide_mask(sprite, collided_sprite)
                elif collided_sprite.shape == "line" and sprite.shape != "line":
                    y = collided_sprite.m * sprite.centerx + collided_sprite.q
                    if y >= sprite.rect.y \
                       and y <= sprite.rect.y + sprite.rect.height:
                        point = pygame.sprite.collide_mask(
                            sprite,
                            collided_sprite
                        )
                elif collided_sprite.shape != "line" and sprite.shape == "line":
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
                        sprite.active_collisions.add(collided_sprite)
                        sprite.collision_points[collided_sprite] = point
                    if not collided_sprite.immutable:
                        point = pygame.sprite.collide_mask(
                            collided_sprite,
                            sprite
                        )
                        collided_sprite.active_collisions.add(sprite)
                        collided_sprite.collision_points[sprite] = point

    def update(self):
        if self.pause:
            return False, None, self.elements
        for sprite in self.elements.sprites():
            if getattr(sprite, "destroyed", False):
                sprite.kill()
                try:
                    sprite.active_collisions.empty()
                    sprite.handled_collisions.empty()
                except AttributeError, e:
                    print e
                    pass

                try:
                    sprite.parent.remove(sprite)
                except (TypeError, AttributeError):
                    pass

        self.elements.update()

        return False, None, self.elements
