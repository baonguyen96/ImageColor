Bao Nguyen
BCN140030
CS 4391.001

Project 1 Report

I. Problem statements
- Write two programs related to the manipulation of color in digital images.
- Write a program that gets as input a color image, performs linear scaling in the Luv domain, and writes
the scaled image as output. The scaling in Luv should stretch only the luminance values. You are asked to
apply linear scaling that would map the smallest L value in the specified window and all values below it
to 0, and the largest L value in the specified window and all values above it to 100.
- Write a program that gets as input a color image, performs histogram equalization in the Luv domain, and
writes the scaled image as output. Histogram equalization in Luv is applied to the luminance values, as
computed in the specified window. It requires a discretization step, where the real-valued L is discretized
into 101 values.

II. Prerequisites
- Python 3.5+
- OpenCV
- Numpy
- Built-in modules: os, sys, shutil

III. Execution
- Navigate to Project1 directory. All .py files must be in this directory.
- In the CLI, type command in this format:
        py name w1 h1 w2 h2 ImageIn ImageOut
  where
        name: program name (linear_scaling.py or histogram_equalization.py)
        w1: "from" x-coordinate (from 0 to 1)
        h1: "from" y-coordinate (from 0 to 1)
        w1: "to" x-coordinate (from 0 to 1)
        h1: "to" y-coordinate (from 0 to 1)
        ImageIn: PATH to the original image
        ImageOut: NAME of the output image
- When execute, the programs will create a directory called "images"
in the same directory that they are located. All output images will be saved
in this "images" directory.

IV. Results
- In my observation, Linear Scaling consistently produces better images than Histogram Equalization.
- Histogram Equalization tries to spread the histogram out, which in cases where the image is
intentionally underexposed (such as Black & White or film images), it will tries to boost white level
of the black pixels (which is bad). This causes those images to become too grainy.
- In some cases, the program actually makes the image worse than the original.
For example, if user choose to sample a very bright area from the original image,
the output image will be very dark. On the other hand, if a very dark area is sampled,
then the output image will be very bright. For the best result, user should sample the entire image.

V. Special notes
- Because the program has to repeatedly read the image over and over again
while switching color space and changing the luminance, it is SLOW for larger images (*).
- To improve the speed, I decide not to convert the entire image from RGB -> XYZ -> Luv and back.
Instead, while reading every pixel in RGB, I convert that pixel to XYZ then Luv. And I do the
same thing while converting back (2). This reduces the needs to re-read the entire image over and
over again, thus improves the conversion speed.
For instance, here is the result of performing both method on the same 512px X 480px color image, sampling coordinates (0.1, 0.1), (0.3, 0.2)

| Task                   | Method 1      | Method 2      |
| ---------------------- |-------------- | ------------- |
| Linear Scaling         | 76.54 seconds | 58.86 seconds |
| Histogram Equalization | 71.48 seconds | 59.48 seconds |

As you can see, this is relatively small image, and  my method improves around 10 - 15 seconds
in runtime. The difference in performance will become greater for larger images.
- Even though the program only intends to modify the specified area of the image,
the remaining part of the image may not remain exactly the same due to floating point
truncation during the color space transformation process.
- I use GitHub as version control during development. Check out at: https://github.com/baonguyen96/ImageColor