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

* [Importing the package](#importing_the_package)
* [Opening an image](#opening_an_image)
* [Getting size of the image](#getting_size_of_the_image)
* [Resizing and rotating](#resizing_and_rotating)
* [Image filtering](#image_filtering)
* [Writing text on image](#writing_text_on_image)
* [Removing background of the image](#removing_background_of_the_image)
* [Other common functions](#other_common_functions)

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

# getting canny edges and showing the returned image
edges = image.get_canny_edges()
edges.show()
```
#### Writing Text on image
```python
image.draw_text("The is sample text", text_color=(0, 0, 0), coordinates=(0, 0))
```
Removing Background of the image
```python
image.remove_background()
```
#### Other common functions
```python
#showing the image
image.show()

# returning base64 string
image.get_base64()
```
