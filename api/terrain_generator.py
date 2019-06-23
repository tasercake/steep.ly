from copy import deepcopy
from PIL import Image


class TerrainGenerator:
    DEFAULT_OPTIONS = {
        'size': 512
    }

    def __init__(self, options):
        self.options = deepcopy(self.DEFAULT_OPTIONS)
        self.options.update(options)
        self.size = self.options['size']

    def get_height(self):
        height = Image.new('L', (self.size, self.size))
        return height

    def generate_images(self):
        height = self.get_height()
        return {'height': height}
