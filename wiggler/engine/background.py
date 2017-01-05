
class Background(object):

    def __init__(self, resources):
        self.resources = resources
        self.type = 'solid'
        self.color = (255, 255, 255)
        self.image = None
        self.image_name = ''

    def set_solid(self, color):
        self.type = 'solid'
        if color != self.color:
            if type(color) == tuple:
                self.color = color
            if type(color) == str:
                color_tuple = tuple(map(int, color.split(',')))
                self.color = color_tuple

    def set_image(self, image_name):
        self.type = 'image'
        if image_name != self.image_name:
            image = self.resources.load_resource('images', image_name)
            self.image = image.content
            self.image_name = image_name
