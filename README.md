# Simple DFT (DCT) Compression


## Overview

This scripts offers a simple implementation of using FFT for compression of 
images.

## Example

The following example yielded a 88% reduction in size compared to the original image:

Original:
![original](/samples/sample.original.jpg)

After FFT:
![new](/samples/sample.new.jpg)

## Usage

```
usage: dft [-h] [--epsilon EPSILON] [--bw] [--conv] path

preforms image compression using DFT reduction on a given image

positional arguments:
  path               path to the target image

optional arguments:
  -h, --help         show this help message and exit
  --epsilon EPSILON  truncate all values in specter that are less than epsilon
  --bw               convert image to grayscale before reduction
  --conv             convert image to jpg
```

## Usage examples

This script can be installed using `pip` or used separately.

For a `pip` based installation, run `pip install -e <this directory>`.
Otherwise, when running each command, replace `dft` with `python -m dft` when
inside the base directory.

For conversion of a given image to an AAA format, run:

```
dft --epsilon 200 image.bmp
```

Output is written as image.aaa.

For conversion of an AAA image back to JPG (for comparison), do:

```
dft --conv image.aaa
```

Image is outputed as image.jpg.


## Installation

Inside a working python environment run:

```
pip install -r requirements.txt
```

or

```
pip install pillow scipy matplotlib numpy
```


## Requirements

- matplotlib
- numpy
- Pillow
- scipy

See: requirements.txt
