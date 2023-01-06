from setuptools import setup, find_packages


setup(
    name='pil_plus',
    version='0.1',
    license='APACHE-2.0',
    author="Fahad Maqsood Qazi",
    author_email='qazifahadmaqsood@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/fahadmaqsood/pil_plus',
    keywords=['PIL', 'image processing', 'PIL wrapper', 'easy PIL', 'pillow'],
    install_requires=[
          'opencv-python',
          'pillow',
          'matplotlib',
          'numpy',
          'backgroundremover'
      ],
)
