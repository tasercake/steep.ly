import numpy as np
from copy import deepcopy
from PIL import Image


class TerrainGenerator:
    DEFAULT_OPTIONS = {
        'seed': 0,
        'preview_size': 512,
        'preview': True,
        'size': 4096,
        'depth': 1,
        'scale': 512,
    }

    def __init__(self, options):
        self.options = deepcopy(self.DEFAULT_OPTIONS)
        self.options.update(options)
        self._load_options(self.options)

    def _load_options(self, options):
        self.options = options
        self.preview_size = options['preview_size']
        self.size = options['size']
        self.seed = options['seed']
        self.preview = options['preview']
        self.scale = options['scale']
        self.depth = options['depth']

    def normalize(self, image):
        return self._normalize(image, image.min(), image.max())

    def _normalize(self, image, image_low, image_high):
        """
        Normalizes an image given the theoretical bounds of the pixel values.

        Args:
            image: The image to normalize
            image_low: Theoretical minimum pixel value in the image
            image_high: Theoretical maximum pixel value in the image

        Returns:
            Normalized image
        """
        if image_high == 0:
            return image
        dtype = image.dtype
        image = image.astype(np.float64)
        image -= image_low
        image = image / image_high
        return image.astype(dtype)

    def _perlin(self, size: int, scale: int):
        def f(g):
            return 6 * g ** 5 - 15 * g ** 4 + 10 * g ** 3

        delta = (scale / size, scale / size)
        d = (size // scale, size // scale)
        grid = np.mgrid[0:scale:delta[0], 0:scale:delta[1]].transpose(1, 2, 0) % 1
        # Gradients
        angles = 2 * np.pi * np.random.rand(scale + 1, scale + 1)
        gradients = np.dstack((np.cos(angles), np.sin(angles)))
        g00 = gradients[0:-1, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g10 = gradients[1:, 0:-1].repeat(d[0], 0).repeat(d[1], 1)
        g01 = gradients[0:-1, 1:].repeat(d[0], 0).repeat(d[1], 1)
        g11 = gradients[1:, 1:].repeat(d[0], 0).repeat(d[1], 1)
        # Ramps
        n00 = np.sum(grid * g00, 2)
        n10 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1])) * g10, 2)
        n01 = np.sum(np.dstack((grid[:, :, 0], grid[:, :, 1] - 1)) * g01, 2)
        n11 = np.sum(np.dstack((grid[:, :, 0] - 1, grid[:, :, 1] - 1)) * g11, 2)
        # Interpolation
        t = f(grid)
        n0 = n00 * (1 - t[:, :, 0]) + t[:, :, 0] * n10
        n1 = n01 * (1 - t[:, :, 0]) + t[:, :, 0] * n11
        return (np.sqrt(2) * ((1 - t[:, :, 1]) * n0 + t[:, :, 1] * n1)) + 1

    def fractal_noise(self, size, scale, depth: int = 1, persistence=0.5, amplitudes=None):
        if 2 ** depth > size:
            depth = size.bit_length() - 1
        noise = np.zeros((size, size))
        frequencies = [2 ** i for i in range(depth)]
        amplitudes = amplitudes or [persistence ** i for i in range(depth)]
        assert len(amplitudes) == len(frequencies)
        for freq, amp in zip(frequencies, amplitudes):
            print(scale, freq * scale)
            noise += amp * self._perlin(size, (freq * scale))
        return self.normalize(noise)

    def get_height(self):
        height = self.fractal_noise(self.preview_size, self.scale, depth=self.depth)
        if self.preview:
            height = Image.fromarray((height * 255).astype(np.uint8), 'L')
        else:
            height = Image.fromarray((height * 65535).astype(np.uint16), 'F')
        return height

    def generate_images(self):
        np.random.seed(self.seed)
        height = self.get_height()
        return {'height': height}
