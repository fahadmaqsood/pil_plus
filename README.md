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

Importing the package
```python
from pil_plus import PilPlus
```
Opening an image
```python
# using path of the image
image = PilPlus("test.jpg")

# converting numpy array to PilPlus object
image = PilPlus(some_numpy_image_array)

# converting Pil Image to PilPlus object
image = PilPlus(some_pil_image_variable)
```
Getting information about the image
```python
# Getting width
image.get_width()

# Getting height
image.get_height()

# Getting size tuple
image.get_size()
```


