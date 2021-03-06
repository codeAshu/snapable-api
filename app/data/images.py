# django/tastypie/libs
from PIL import Image, ImageEnhance


class SnapImage(object):
    """
    A helper class that wraps the PIL Image class with useful Snapable
    functionality.
    """

    def __init__(self, image=None):
        # read the opject into the wrapper
        if image is not None:
            self._img = image
            self._img.load()
        else:
            self._img = Image.new()

    def __getattr__(self, name):
        if name == 'img':
            return self._img
        elif name == 'exif':
            try:
                return dict(self._img._getexif().items())
            except:
                return {}
        else:
            return getattr(self._img, name)

    def copy(self):
        return SnapImage(self._img.copy())

    def crop(self, box):
        try:
            # The crop rectangle, as a (left, upper, right, lower)-tuple.
            self._img = self._img.crop(box=box)

        except Exception:
            return False

    def crop_square(self):
        self.rotate_upright()
        # x > y
        if self.size[0] > self.size[1]:
            left = (self.size[0] - self.size[1]) / 2
            crop_box = (left, 0, left + self.size[1], self.size[1])
        # y > x
        else:
            top = (self.size[1] - self.size[0]) / 2
            crop_box = (0, top, self.size[0], top + self.size[0])

        return self.crop(box=crop_box)

    def resize(self, size):
        if self.rotate_upright():
            try:
                # get the size param
                self._img = self._img.resize(size, Image.ANTIALIAS)
                return True
            except Exception:
                return False

    def rotate_upright(self):
        try:
            exif = self.exif
            # rotate as required
            # 0x0112 = orientation
            if 0x0112 in exif and exif[0x0112] == 3:
                self._img = self._img.rotate(180, expand=True)
            elif 0x0112 in exif and exif[0x0112] == 6:
                self._img = self._img.rotate(270, expand=True)
            elif 0x0112 in exif and exif[0x0112] == 8:
                self._img = self._img.rotate(90, expand=True)

            return True
        except Exception:
            return False

    def watermark(self, watermark, opacity=0.75, resize=0.5, corner=2):
        # validate opacity
        if opacity <= 0:
            opacity = 0.1
        if opacity > 1.0:
            opacity = 1.0
        # validate resize
        if resize <= 0:
            resize = 0.1
        if resize > 1.0:
            resize = 1.0

        try:
            # get the target size (image * resize)
            target_size = ((self._img.size[0] * resize), (self._img.size[1] * resize))

            # get target scaling ratios
            scale_x = float(target_size[0]) / float(watermark.size[0])
            scale_y = float(target_size[1]) / float(watermark.size[1])
            scale = min(scale_x, scale_y) # figure out the smallest scaling value (ie. fit inside target size)

            # resize watermark image based on saling ration
            watermark = watermark.resize((int(scale * watermark.size[0]), int(scale * watermark.size[1])), Image.ANTIALIAS)

            #Opacity
            layer = Image.new("RGBA", self._img.size)

            # top right
            if corner == 1:
                pos = (self._img.size[0]-watermark.size[0], 0)
            # bottom right
            elif corner == 2:
                pos = (self._img.size[0]-watermark.size[0], self._img.size[1]-watermark.size[1])
            # bottom left
            elif corner == 3:
                pos = (0, self._img.size[1]-watermark.size[1])
            # top left
            else:
                pos = (0, 0)

            # set/get other properties
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            watermark.putalpha(alpha)
            layer.paste(watermark, pos)
            self._img = Image.composite(layer, self._img, layer)

            return True
        except Exception:
            return False
