import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import matplotlib.pyplot as plt
import os
import subprocess

import base64
from io import BytesIO


BLANK = "blank"

class PilPlus():

    img = None
    BLANK = "blank"

    def __init__(self, img, size=None) -> None:
        self.setImage(img, size)

        self.arial_font = ImageFont.truetype("arial.ttf", size=12)

    def setImage(self, img, size=None):
        if type(img) == str and img == BLANK:
            if type(size) is not tuple:
                raise ValueError("size for a blank image must be defined")

            self.img = Image.new("RGB", size, (255, 255, 255))

            return

        if type(img) == np.ndarray:
            self.img = Image.fromarray(img)
        elif type(img) == Image.Image:
            self.img = img
        elif type(img) == PilPlus:
            self.img = img.get_image()
        else:
            self.img = Image.open(img)

    def get_width(self) -> int:
        """
            Outputs the width of the image

            @param self:
            @return: int
                width of image
        """
        
        return self.img.size[0]

    def get_height(self) -> int:
        """
            Outputs the height of the image

            @param self:
            @return: int
                Height of the image
        """
        
        return self.img.size[1]

    def get_size(self):
        """
            Outputs a tuple containing the size of the image

            @param self:
            @return: tuple(width, height)
        """
        
        return self.img.size

    def get_draw(self):
        """
            Outputs the ImageDraw for the image

            @param self:
            @return: PIL.ImageDraw
        """
        
        return ImageDraw.Draw(self.img)        
        
    
    def convert_to_grayscale(self):
        """
            Converts the image to grayscale

            @param self:
            @return: self
                current PilPlus object
        """
        
        self.img = Image.fromarray(cv2.cvtColor(np.asarray(self.img.convert('L')), cv2.COLOR_GRAY2RGB))
        
        return self

    def bgr_to_rgb(self):
        """
            Converts the image from bgr to rgb (opencv uses bgr)

            @param self:
            @return: None
        """
        
        self.img = Image.fromarray(cv2.cvtColor(np.asarray(self.img), cv2.COLOR_BGR2RGB))

    def convert_to_rgb(self):
        """
            Converts image to rgb

            @param self:
            @return: PilPlus
                internally changes the image to rgb
        """
        if self.img.mode == 'L':
            self.img = Image.fromarray(cv2.cvtColor(np.asarray(self.img), cv2.COLOR_GRAY2RGB))
        elif self.img.mode == 'RGBA':
            self.img = Image.fromarray(cv2.cvtColor(np.asarray(self.img), cv2.COLOR_RGBA2RGB))

        return self

    def rgb_to_bgr(self):
        """
            Converts the image from rgb to bgr (opencv uses bgr)

            @param self:
            @return: None
        """
        
        self.img = Image.fromarray(cv2.cvtColor(self.get_numpy_array(), cv2.COLOR_RGB2BGR))


    

    def apply_gaussian_blur(self):
        """
            apply gaussian blur to the current image

            @param self:
            @return: None
        """
        
        self.img = self.img.filter(ImageFilter.GaussianBlur(10))

    def apply_background(self, color):     
        """
            if current image has a transparent background (see remove_background function) then apply
            a specific color as a background.

            @param self:
            @param color: What color to use for the image.  Default is black.
                        If given, this should be a single integer or floating point value
                        for single-band modes, and a tuple for multi-band modes (one value
                        per band).  When creating RGB images, you can also use color
                        strings as supported by the ImageColor module.  If the color is
                        None, the image is not initialized. 
            
            @return: None
        """
        
        if len(self.img.split()) == 4:
            background = Image.new("RGB", self.img.size, color=color)
            background.paste(self.img, mask=self.img.split()[3]) # 3 is the alpha channel

            self.img = background

    def draw_text(self, text: str, text_color: tuple, font:ImageFont = None, coordinates=(0,0)):
        """
        @param self:
        @param text: str
            Text to be written on the image.
        @param font: ImageFont
            Font to use for the text. Default is Arial with size 12
        @param text_color: tuple
            Tuple containing RGB or RGBA color
        
        @return: PilPlus Object
        """

        if font is None:
            font = self.arial_font
        
        W, H = (self.get_width(), self.get_height())

        self.draw = self.get_draw() 

        _, _, w, h = self.draw.textbbox(coordinates, text, font=font)

        self.draw.text(((W-w)/2, (H-h)/2), text, font=font, fill=text_color)

        return self.img

    def resize(self, new_width: int = None, new_height: int = None):
        """
            Resizes the image to new dimensions. If only `new_width` is defined, `new_height` can be calculated to keep aspect ratio and vice versa. If both are defined at the same time, then image will be resized to those dimensions.

            @param self:
            @param new_width: int
                If only new width is defined, new_height can be calculated to keep aspect ratio. Both can also be defined at the same time to not keep the aspect ratio.
            @param new_height: int
                If only new_height is defined, new_width can be calculated to keep aspect ratio. Both can also be defined at the same time to not keep the aspect ratio.
            
            @return: None
        """

        if new_height == None and new_width == None:
            raise ValueError("New height and New width can not be none at the same time.")
        
        if new_height == None and new_width != None:
            new_height = new_width * self.get_height() // self.get_width() 
        
        if new_width == None and new_height != None:
            new_width = new_height * self.get_width() // self.get_height()

        self.img = self.img.resize((new_width, new_height), Image.ANTIALIAS)


    def rotate(self, degrees: int):
        """
            Rotates the image 

            @param self:
            @param degrees: int
                degrees of rotation. Can be positive or negative.

            @return: None
                changes rotation internally
        """
        self.img = self.img.rotate(degrees)

    def sharpen(self):
        """
            Sharpens the image

            @param self:
            @return: None
        """
        
        sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharped_img = cv2.filter2D(np.array(self.img), -1, sharpen_filter)

        self.setImage(sharped_img)

    def save_brightness_scale(self, file_name: str):
        """
        Saves an image in which each pixel is the luminosity of the pixel of original image

        @param: str
            File name of output image
        @return: None 
        """
        img = np.array(self.img)

        for row in range(self.get_height()):
            for col in range(self.get_width()):
                bg = self.img.getpixel((col, row))

                luminosity = self.calculate_luminosity(bg)
                
                img[row][col] = (luminosity, luminosity, luminosity)

        
        self.save(file_name, img)

    def remove_background(self):
        """
            removes background from the image

            @param self:
            @return: None
        """

        if not os.path.exists("tmp"):
            os.mkdir("tmp")
        
        self.save("tmp/_____temp_____.png", replace_file=True)
        
        subprocess.call('backgroundremover -i "tmp/_____temp_____.png" -a -ae 15 -o "tmp/_____temp_____.png.bgremoved.png"')

        self.setImage('tmp/_____temp_____.png.bgremoved.png')

    def fill(self, color) -> None:
        """
            Fill whole image with a particular color

            @param self:
            @param color: tuple or list
            @return: None
        """
        
        img = np.array(self.img)
        color = tuple(color)

        for row in range(self.get_height()):
            for col in range(self.get_width()):
                img[row][col] = color

        self.setImage(img)

    def get_canny_edges(self):
        """
            Outputs a PilPlus object of detected Canny Edges of the image
 
            @param self:
            @return: PilPlus
        """
        
        return PilPlus(cv2.Canny(np.asarray(self.img),100,200))

    
    def replace_color(self, color: tuple, replacement_color: tuple) -> None:
        """
            @param self:
            @param color: tuple
                rgb(a) representation of color to be replaced
            @param replacement_color: tuple
                new color
            
            @return: PilPlus
                PilPlus object with changes made (image will also be changed internally inside the class) 
        """

        img = np.array(self.img)

        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if np.array_equal(img[row][col], color):
                    print(np.array_equal(img[row][col], color))
                    img[row][col] = replacement_color
            
        self.setImage(img)


    def copy_pixels_from(self, mask: 'PilPlus', destinationColoredPixel=(255,255,255), follow_luminosity=False):
        if mask.get_width() != self.get_width() and mask.get_height() != self.get_height():
            raise ValueError("input and current image dimensions should be same")
        
        mask_width = mask.get_width()
        mask_height = mask.get_height()

        img = np.array(self.img)

        
        # restriction for only painting upto 3 points (for follow_luminosity)
        painted = False
        paint_limit = 2
        paint_num = 0

        
        scale = 256 / 8


        for row in range(mask_height):
            for col in range(mask_width):
                mask_color = mask.get_image().getpixel((col, row))
                if self.img.getpixel((col, row)) != destinationColoredPixel:
                    # if it is destination pixel then copy
                    img[row][col] = mask_color


                    if painted == True:
                        paint_num += 1
                    
                    if paint_num >= paint_limit:
                        painted = False
                        paint_num = 0

                elif follow_luminosity:
                    # if it's not a destination pixel,
                    # then it means it's a white pixel and we need to shrink
                    # black pixels depending on the mask's pixel

                    if self.calculate_luminosity(mask_color) >  scale * 7:
                        continue

                    if painted == False:
                        increasing_paths = self.find_luminosity_increasing_path((col, row), mask)

                        for path in increasing_paths:
                            if path == "left":
                                try:
                                    for i in range(col, col + paint_limit):
                                        bg = mask.get_image().getpixel((i, row))
                            
                                        optimalFilling = self.calculateOptimalFilling(bg)
                                        img = self.fill_surrounding_points(
                                            row, 
                                            i, 
                                            _range=optimalFilling[0], 
                                            color=optimalFilling[1], 
                                            axis="x", 
                                            img=img,
                                            mask=mask)
                                except IndexError:
                                    pass
                            elif path == "right":
                                try:
                                    for i in range(col - paint_limit, col):
                                        bg = mask.get_image().getpixel((i, row))
                            
                                        optimalFilling = self.calculateOptimalFilling(bg)
                                        img = self.fill_surrounding_points(
                                            row, 
                                            i, 
                                            _range=optimalFilling[0], 
                                            color=optimalFilling[1], 
                                            axis="x", 
                                            img=img,
                                            mask=mask)
                                except IndexError:
                                    pass
                            elif path == "up":
                                try:
                                    for i in range(row - paint_limit, row):
                                        bg = mask.get_image().getpixel((col, i))
                            
                                        optimalFilling = self.calculateOptimalFilling(bg)
                                        img = self.fill_surrounding_points(
                                            i, 
                                            col, 
                                            _range=optimalFilling[0], 
                                            color=optimalFilling[1], 
                                            axis="y", 
                                            img=img,
                                            mask=mask)
                                except IndexError:
                                    pass
                            elif path == "down":
                                try:
                                    for i in range(row, row + paint_limit):
                                        bg = mask.get_image().getpixel((col, i))
                            
                                        optimalFilling = self.calculateOptimalFilling(bg)
                                        img = self.fill_surrounding_points(
                                            i, 
                                            col, 
                                            _range=optimalFilling[0], 
                                            color=optimalFilling[1], 
                                            axis="y", 
                                            img=img,
                                            mask=mask)
                                except IndexError:
                                    pass

                        paint_num += 1
                    
                    if paint_num >= paint_limit:
                        painted = True
                        paint_num = 0

        self.setImage(img)

    def calculate_luminosity(self, pixel):
        """
        Calculate the luminosity of an rgb pixel

        @param: tuple or list
            a tuple of list containing rgb values of a pixel
        @return: float
            luminosity of a pixel
        """
        
        return 0.2126 * pixel[0] + 0.7152 * pixel[1] + 0.0722 * pixel[2] # per ITU-R BT.709

    def calculateOptimalFilling(self, bg):
        luma = self.calculate_luminosity(bg)
        brightness_scale = 256 / 8
        
        
        range, color, axis = (0, 0), (0, 0, 0), "x"
        follow_limit = 0 
        

        if luma <= brightness_scale * 1:
            range = 1, 1
            color = (0, 0, 0)
            axis = "x"
            follow_limit = 1
        elif luma <= brightness_scale * 2:
            range = 1, 1
            color = (0, 0, 0)
            axis ="xy"
            follow_limit = 2
        elif luma <= brightness_scale * 3:
            range = 1, 1
            color = (0, 0, 0)
            axis="x"
            follow_limit = 2
        elif luma <= brightness_scale * 4:
            range = 1, 1
            color = (0, 0, 0)
            axis="x"
            follow_limit = 2
        elif luma <= brightness_scale * 5:
            range = 1, 1
            color = (0, 0, 0)
            axis="x"   
            follow_limit = 2
        elif luma <= brightness_scale * 6:
            range = 1, 1
            color = (0, 0, 0)
            axis="x"


        return range, bg, axis, follow_limit

    def _are_all_elems_same(self, arr):
        """
            Internal function for checking if all elements of a list are same

            @param arr: list
            @return: bool
        """
        if arr == []:
            return False

        return arr.count(arr[0])==len(arr)

    def is_luminosity_increasing(self, luminos):
        """
        Given an array of luminosities, return if luminosity is in increasing order

        @param self:
        @param luminos: list 
            list of luminosities
        @return: bool 
            True if luminosity is in decreasing order, False otherwise
        """

        if luminos == []:
            return False

        last_lumas = [256]
        for luma in luminos:
            if luma <= last_lumas[-1]:
                last_lumas.append(luma)
            else:
                return False

        return self._are_all_elems_same(last_lumas[1:]) == False

    def is_luminosity_decreasing(self, luminos):
        """
        Given an array of luminosities, return if luminosity is in decreasing order

        @param self:
        @param luminos: list 
            list of luminosities
        @return: bool
            True if luminosity is in decreasing order, False otherwise
        """
        
        if luminos == []:
            return False

        last_lumas = [0]
        for luma in luminos:
            if luma >= last_lumas[-1]:
                last_lumas.append(luma)
            else:
                return False

        return self._are_all_elems_same(last_lumas[1:]) == False

    def find_luminosity_increasing_path(self, coordinates, img=None):
        """
        Given x and y coordinates, if checks 4 pixels in all directions and outputs a list of directions in which luminosity is increasing

        @param self:
        @param coordinates: tuple
            x and y coordinates
        @param img: PIL.Image 
            if None, use current image object otherwise use passed image
        @return: list 
            list of directions in which luminosity is increasing. Example ["left", "right", "up", "down"]
        """
        
        if img == None:
            img = self

        x = coordinates[0]
        y = coordinates[1]
        
        try:
            left = [self.calculate_luminosity(img.get_image().getpixel((_x, y))) for _x in range(x, x + 4)]
        except IndexError:
            left = []
        try:
            right = [self.calculate_luminosity(img.get_image().getpixel((_x, y))) for _x in range(x - 4, x)]
        except IndexError:
            right = []

        try:
            up = [self.calculate_luminosity(img.get_image().getpixel((x, _y))) for _y in range(y - 4, y)]
        except IndexError:
            up = []
        
        try:
            down = [self.calculate_luminosity(img.get_image().getpixel((x, _y))) for _y in range(y, y + 4)]
        except IndexError:
            down = []

        result = []
        
        if self.is_luminosity_increasing(left): result.append("left")
        if self.is_luminosity_decreasing(right): result.append("right")
        if self.is_luminosity_decreasing(up): result.append("up")
        if self.is_luminosity_increasing(down): result.append("down")

        return result


    def fill_surrounding_points(self, y, x, _range, color=(255, 255, 255), img=None, mask=None, follow_limit=2, _follow_num=0):
        """
        Given a mask, an image and xy coordinates, Fill the image's surrounding points of the xy coordinates with a specific color depending on the luminosity of the surrounding points of the mask.

        @param y: int
            y coordinate
        @param x: int
            x coordinate
        @param _range: int
            how many pixels is the surrounding?
        @param color: tuple
            color to be filled
        @param img: PilPlus
            Default is the image object that this class holds
        @param mask: PilPlus
            An image to be used as a mask from which
        @param follow_limit: int
            Number of pixels to follow for luminosity based point filling.

        @return: PilPlus
            A PilPlus object containing the image with specified changes.
        """
        if img is None:
            img = self.img

        # print(followMask)

        if mask == None:
            return img
        
        if _follow_num >= follow_limit:
            return img

        col = x
        row = y

        for i in range(y - _range[0], y + _range[0]):
            for j in range(x - _range[0], x + _range[1]):
                try:
                    img[i][j] = color
                except IndexError:
                    pass    

        paths = self.find_luminosity_increasing_path((col, row), mask)

        limit = 1

        for path in paths:
            if path == "left":
                try:
                    for i in range(col, col + limit):
                        bg = mask.get_image().getpixel((i, row))
            
                        optimalFilling = self.calculateOptimalFilling(bg)
                        img = self.fill_surrounding_points(
                            row, 
                            i, 
                            _range=optimalFilling[0], 
                            color=optimalFilling[1], 
                            axis="x", 
                            img=img,
                            mask=mask,
                            follow_limit=follow_limit-1,
                            follow_num=_follow_num+1)
                except IndexError:
                    pass
            elif path == "right":
                try:
                    for i in range(col - limit, col):
                        bg = mask.get_image().getpixel((i, row))
            
                        optimalFilling = self.calculateOptimalFilling(bg)
                        img = self.fill_surrounding_points(
                            row, 
                            i, 
                            _range=optimalFilling[0], 
                            color=optimalFilling[1], 
                            axis="x", 
                            img=img,
                            mask=mask,
                            follow_limit=follow_limit-1,
                            follow_num=_follow_num+1)
                except IndexError:
                    pass
            elif path == "up":
                try:
                    for i in range(row - limit, row):
                        bg = mask.get_image().getpixel((col, i))
            
                        optimalFilling = self.calculateOptimalFilling(bg)
                        img = self.fill_surrounding_points(
                            i, 
                            col, 
                            _range=optimalFilling[0], 
                            color=optimalFilling[1], 
                            axis="y", 
                            img=img,
                            mask=mask,
                            follow_limit=follow_limit-1,
                            follow_num=_follow_num+1)
                except IndexError:
                    pass
            elif path == "down":
                try:
                    for i in range(row, row + limit):
                        bg = mask.get_image().getpixel((col, i))
            
                        optimalFilling = self.calculateOptimalFilling(bg)
                        img = self.fill_surrounding_points(
                            i, 
                            col, 
                            _range=optimalFilling[0], 
                            color=optimalFilling[1], 
                            axis="y", 
                            img=img,
                            mask=mask,
                            follow_limit=follow_limit-1,
                            follow_num=_follow_num+1)
                except IndexError:
                    pass

        return img
                
    def get_image(self) -> Image:
        """
        
        @return: PIL.Image 
            Current Image
        """
        
        return self.img

    def get_numpy_array(self) -> np.ndarray: 
        """
 
            @param self:
            @return: np.ndarray 
                numpy array of the image
        """
        return np.array(self.img)

    def show(self) -> None:
        """
            displays the image
            
            @param self:
            @return: None
        """
        
        self.rgb_to_bgr()
        cv2.imshow('image', self.get_numpy_array())
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        self.bgr_to_rgb()
        

    def save(self, path="outputs/output.png", img=None, replace_file=False, add_top_border=True) -> None:
        """
            saves the image

            @param self:
            @param path: str
                path of output file including the its name. 
            @param img: PIL.Image 
                if None, it will save the image that this particular class holds. Passing another image to it will save that image
            @param replace_file: bool 
                Replace the file if filename already exists?
            @param add_top_border: bool 
                if True, output file will have 8px white border on top of the image.   
            @return: None
        """

        if img is None:
            img = self.img

        if path == "outputs/output.png" and not os.path.exists(path):
            os.mkdir("outputs")

        if not replace_file:
            count = 0
            while os.path.exists(path):
                path = path.split(".")[0].split("_")[0] + "_" + str(count + 1) +  ".png"
                count += 1

        if add_top_border:
            new_size = (self.get_width(), self.get_height() + 8)

            new_im = Image.new("RGB", new_size, (255,255,255))
            box = tuple((n - o) for n, o in zip(new_size, self.get_size()))
            new_im.paste(img, box)

            img = new_im

        plt.imshow(img, interpolation="bilinear")
        plt.axis("off")
        plt.savefig(path, bbox_inches='tight', pad_inches=0, dpi=600)


    def return_base64(self):
        """
            Returns the base64 data of the image

            @param self:
            @return: -> bytes 
                base64 data of the image
        """

        buffered = BytesIO()
        self.img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue())