#!/bin/python3

import png
import string


def hideTextByEnlarging(inputFile: string, text: string, resultFile: string = 'res.png'):

	def generator_function():
		for c in text:
			yield ord(c)
		while True:
			yield 0
	
	gen = generator_function()

	def processBlock(block, chars, chans):
		mask = 7

		tl = block.copy()
		tr = block.copy()
		bl = block.copy()
		br = block.copy()

		for i, char in enumerate(chars):
			tr[i] = (tr[i]>>3<<3) + (char & mask)  
			bl[i] = (bl[i]>>3<<3) + ((char>>3) & mask)  
			br[i] = (br[i]>>3<<3) + ((char>>6) & mask)  

		return tl+tr, bl+br





	with open(inputFile, 'rb') as ifs:


		rpng = png.Reader(file=ifs).read()

		w, h = rpng[:2] # we're assuming they're the same size


		rl = list(rpng[2])

		rchannels = rpng[3]['planes']


		data = []
		for y in range(h):
			uprow = []
			downrow = []
			for x in range(w):
				block = rl[y][x*rchannels:(x+1)*rchannels]

				chars = [next(gen) for _ in range(rchannels)]


# 				print(x, list(block), chars)
				# input()

				top, bottom = processBlock(block, chars, rchannels)
				uprow += top
				downrow += bottom

			data += [uprow, downrow]

	
	with open(resultFile, "wb") as ofs:
		# output is definitely 3 channels
		writer = png.Writer(w,h, greyscale=False, alpha=False)


		if rchannels == 1:
			writer = png.Writer(w*2,h*2, greyscale=True, alpha=False)
		elif rchannels == 2:
			writer = png.Writer(w*2,h*2, greyscale=True, alpha=True)
		elif rchannels == 3:
			writer = png.Writer(w*2,h*2, greyscale=False, alpha=False)
		elif rchannels == 4:
			writer = png.Writer(w*2,h*2, greyscale=False, alpha=True)
		writer.write(ofs, data)

		writer.write(ofs, data)

	return resultFile

def getTheTextFromEnlarged(fileName):
	with open(fileName, 'rb') as ifs:
		thePNG = png.Reader(file=ifs).read()
		
		h = thePNG[1]
		w = thePNG[0]
		planes = thePNG[3]["planes"]
		imgBits = list(thePNG[2]) # list of rows. Each row is 3x width if 3 color channels. 4 with alpha. 1 if grayscale


		res = ""		
		for y in range(0, h, 2):
			for x in range(0, w, 2):
				topBlock = imgBits[y][x*planes:(x+2)*planes]
				botBlock = imgBits[y+1][x*planes:(x+2)*planes]

				tl = topBlock[:planes]
				tr = topBlock[planes:]
				bl = botBlock[:planes]
				br = botBlock[planes:]


				mask = 7
				for i in range(planes):
					ch = 0
					ch += tr[i] & mask
					ch += (((bl[i]) & mask)<<3)
					ch += (((br[i]) & mask)<<6)

					if ch == 0:
						return res

					res += chr(ch)
	return res








if __name__ == "__main__":
	hideTextByEnlarging('ex1.png', "Hello world")
	getTheTextFromEnlarged('res.png')


