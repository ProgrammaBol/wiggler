import pygame


class EventQueue(object):

    def __init__(self):
        self.subs = {}
        # custom event types map
        self.e_types = {}

    def subscribe(self, source, events):
        for e_type in events:
            if e_type not in self.subs:
                self.subs[e_type] = pygame.sprite.Group()
            self.subs[e_type].add(source)

    def unsubscribe(self, source, e_type, e_id, callback):
        try:
            event = self.subs[source][e_type][e_id]
            event.remove(callback)
        except KeyError:
            pass

    def post(self, e_type, **data):
        event = pygame.event.Event(e_type, data)
        pygame.event.post(event)

    def update(self):
        for event in pygame.event.get():
            try:
                spritegroup = self.subs[event.type]
            except KeyError:
                continue
            for sprite in spritegroup.sprites():
                sprite.add_event(event)
