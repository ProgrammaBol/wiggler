import pygame


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
