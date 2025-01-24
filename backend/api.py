#!/bin/python3

import string

# Placeholders
# Call these functions from the frontend
# Note that all files, by default, are in the same folder as the code being executed

from magic import magic
from lsb import putTextIntoLSB, getTheTextFromLSB

def hideTextInLSB(fileName: string, text: string, bitDepth: int=1):
	'''
	Given an image and text, hide the text in the Least Significant Bits and save it as another image.

	Parameters:
	fileName (string): The original image file.
	text (string): The text to be hidden.

	Returns:
	newFileName: The path to the modified image.
	'''

	newFileName = putTextIntoLSB(fileName, text, bitDepth)

	return newFileName



def mixTwoImagesMagic(image1Path: string, image2Path: string):
	'''
	Mix two images such that one shows on light background, and the other on black.

	Parameters:
	image1Path (string): The file path of the first image.
	image2Path (string): The file path of the second image.

	Returns:
	newImagePath: The path to the new image with the two images mixed.
	'''
	
	newImagePath = magic(image1Path, image2Path)

	return newImagePath


def getTextFromLSB(fileName: string, bitDepth: int=1):
	'''
	Given an image, extract hidden text from the Least Significant Bits.

	Parameters:
	fileName (string): The file path of the image with hidden text.
	bitDepth (int): The number of Least Significant Bits used for embedding the text. Default is 1.

	Returns:
	extractedText: The text extracted from the image.
	'''


	extractedText  = getTheTextFromLSB(fileName, bitDepth)

	return extractedText


def mixColorChannels(redImagePath: string, greenImagePath: string, blueImagePath: string):
	'''
	Given three images representing red, green, and blue color channels, combine them into a single RGB image.

	Parameters:
	redImagePath (string): The file path of the red channel image.
	greenImagePath (string): The file path of the green channel image.
	blueImagePath (string): The file path of the blue channel image.

	Returns:
	rgbImagePath: The path to the new RGB image.
	'''

	rgbImagePath = '/dev/null'

	return rgbImagePath


def separateColorChannels(rgbImagePath: string):
	'''
	Given an RGB image, separate it into its red, green, and blue color channel images.

	Parameters:
	rgbImagePath (string): The file path of the RGB image.

	Returns:
	redImagePath: The path to the red channel image.
	greenImagePath: The path to the green channel image.
	blueImagePath: The path to the blue channel image.
	'''

	redImagePath = '/dev/null'
	greenImagePath = '/dev/null'
	blueImagePath = '/dev/null'

	return redImagePath, greenImagePath, blueImagePath



def hideTextByMakingImageLarger(fileName: string, text: string):
	'''
	Given an image and text, hide the text in the image by doubling the image's size.

	Parameters:
	fileName (string): The original image file.
	text (string): The text to be hidden.

	Returns:
	newFileName: The path to the modified image.
	'''

	newFileName = '/dev/null'

	return newFileName


def getTextFromLargeImage(fileName: string):
	'''
	Given an image, extract text hidden in the "Make Image Larger" algorithm.

	Parameters:
	fileName (string): The file path of the image with hidden text.

	Returns:
	extractedText: The text extracted from the image.
	'''

	extractedText = ''

	return extractedText
