# INTRODUCTION

"pil_plus" is a Python package that makes it easier to work with images. It provides a collection of functions that build upon the Python Imaging Library (PIL) and OpenCV, adding additional features and functionality.

Some of the features offered by "pil_plus" include:

* Image resizing: Functions for quickly and easily resizing images to different dimensions.
* Image rotation: Functions for rotating images by any angle.
* Image filtering: Functions for applying various image filters, such as blur, sharpen, and edge detection.
* Writing Text on Images
* Removing background of Images
* Replacing a specific color in the image with another

Overall, "pil_plus" aims to provide a simple and intuitive interface for working with images in Python, making it easy to perform common image manipulation tasks.

# Usage

using pil_plus is as simple as the following:

* [Importing the package](#importing-the-package)
* [Opening an image](#opening-an-image)
* [Getting size of the image](#getting-size-of-the-image)
* [Resizing and rotating](#resizing-and-rotating)
* [Image filtering](#image-filtering)
* [Writing text on image](#writing-text-on-image)
* [Removing background of the image](#removing-background-of-the-image)
* [Replacing one color with another](#replacing-one-color-with-another)
* [Other common functions](#other-common-functions)

#### Importing the package
```python
from pil_plus import PilPlus
```
#### Opening an image
```python
# using path of the image
image = PilPlus("test.jpg")

# converting numpy array to PilPlus object
image = PilPlus(some_numpy_image_array)

# converting Pil Image to PilPlus object
image = PilPlus(some_pil_image_variable)
```
#### Getting size of the image
```python
# Getting image width
width = image.get_width()

# Getting image height
height = image.get_height()

# Getting image size tuple
size = image.get_size()
```
#### Resizing and rotating

Resizing:
```python
# changing width and keeping aspect ratio
image.resize(new_width=1000)

# changing height and keeping aspect ratio
image.resize(new_height=1000)

# changing both width and height
image.resize(new_width=600, new_height=800)
```
Rotating:
```python
# rotating -45 degrees
image.rotate(-45)
```
#### Image filtering
```python
# applying Guassian Blur
image.apply_gaussian_blur()

# sharpening the image
image.sharpen()

# applying background
image.apply_background((255,255,255)) # changes background from transparent (see Removing background of the image) to black

# getting canny edges and showing the returned image
edges = image.get_canny_edges()
edges.show()
```
#### Writing Text on image
```python
image.draw_text("The is sample text", text_color=(0, 0, 0), coordinates=(0, 0))
```
#### Removing Background of the image
```python
image.remove_background()
```
#### Replacing one color with another
```python
# replace black with white
image.replace_color((0,0,0), (255,255,255))
```
#### Other common functions
```python
# showing the image
image.show()

# saving the image
image.save() # save as outputs\output.png (incrementing _1 in the file name if it exists)
image.save('some_dir/name.extension') # save in some other path

# returning base64 string
image.get_base64()

# get PIL Image object
image.get_image()

# getting numpy array
image.get_numpy_array()

# Conversion between different color models and conventions

image.rgb_to_bgr()
image.bgr_to_rgb()
image.convert_to_grayscale()
image.convert_to_rgb()

```
