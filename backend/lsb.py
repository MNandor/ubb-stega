#!/bin/python3

import png

def putTextIntoLSB(fileName, text, bitDepth=1, outputFile = 'res.png'):
	with open(fileName, 'rb') as ifs:
		thePNG = png.Reader(file=ifs).read()

		h = thePNG[1]
		w = thePNG[0]
		planes = thePNG[3]["planes"]
		imgBits = list(thePNG[2]) # list of rows. Each row is 3x width if 3 color channels. 4 with alpha. 1 if grayscale

		print(h, w, planes)

		roomForBytes = h*w*planes*bitDepth
		bitsToStore = len(text)*8
		print(f'Can store {roomForBytes} bytes, got {bitsToStore}.')

		print(len(imgBits), len(imgBits[0]))


		# used to get message bits
		bitMask = 2**bitDepth-1

		for y in range(h):
			for x in range(w):
				for i in range(planes*x, planes*(x+1)):
					imgBits[y][i] = (imgBits[y][i]>>bitDepth<<bitDepth) # set LSB to zero

					# assumptions made here:
					# text is ASCII, 1 byte always
					# bitDepth is 1, 2, or 4
					# not 3 because it doesn't divide 3 bytes. We'd have to combine bits.
					# text fits into file

					charSpreadAcross = 8//bitDepth

					whichChar, offset = divmod((y*(planes*w)+i), charSpreadAcross)

					if whichChar >= len(text):
						char = 0
					else:
						char = ord(text[whichChar])

					bits = (char >> (bitDepth*offset)) & bitMask

					imgBits[y][i] += bits
	
	with open(outputFile, "wb") as ofs:
		writer = None

		if planes == 1:
			writer = png.Writer(w,h, greyscale=True, alpha=False)
		elif planes == 2:
			writer = png.Writer(w,h, greyscale=True, alpha=True)
		elif planes == 3:
			writer = png.Writer(w,h, greyscale=False, alpha=False)
		elif planes == 4:
			writer = png.Writer(w,h, greyscale=False, alpha=True)
		writer.write(ofs, imgBits)


	return 'output-placeholder.png'


def getTextFromLSB(fileName, bitDepth=1):
	with open(fileName, 'rb') as ifs:
		thePNG = png.Reader(file=ifs).read()

		h = thePNG[1]
		w = thePNG[0]
		planes = thePNG[3]["planes"]
		imgBits = list(thePNG[2]) # list of rows. Each row is 3x width if 3 color channels. 4 with alpha. 1 if grayscale

		bitMask = 2**bitDepth-1

		bitsCollected = 0
		bitSoFar = 0

		string = ""
	
		for y in range(h):
			for x in range(w):
				for i in range(planes*x, planes*(x+1)):


					bit = imgBits[y][i] & bitMask

					bitSoFar += bit<<bitsCollected

					bitsCollected += bitDepth

					if bitsCollected == 8:
						if bitSoFar != 0:
							# print(chr(bitSoFar))
							string += chr(bitSoFar)
						else:
							return string
						bitsCollected = 0
						bitSoFar = 0
		return string







if __name__ == '__main__':
	putTextIntoLSB('input-placeholder.png', 'Hello world!', 8)
	print(getTextFromLSB("res.png", 8))
