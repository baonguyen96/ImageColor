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
computed in the specied window. It requires a discretization step, where the real-valued L is discretized
into 101 values.

II. Prerequisites
- Python 3.5+
- OpenCV
- Numpy

III. Execution
-
- When execute, the programs will create a directory called "images"
in the same directory that they are located. All output images will be saved
in this "images" directory.

IV. Special notes
- Even though the program only intends to modify the specified area of the image,
the remaining part of the image may not remain exactly the same due to floating point
truncation during the color space transformation process.