#!/bin/python3

import png
import string


def combineColorChannels(redImagePath: string, greenImagePath: string, blueImagePath: string, resultFile: string = 'res.png'):


	with open(redImagePath, 'rb') as ifsr, open(greenImagePath, 'rb') as ifsg, open(blueImagePath, 'rb') as ifsb:


		rpng = png.Reader(file=ifsr).read()
		gpng = png.Reader(file=ifsg).read()
		bpng = png.Reader(file=ifsb).read()

		w, h = rpng[:2] # we're assuming they're the same size


		rl = list(rpng[2])
		gl = list(gpng[2])
		bl = list(bpng[2])

		rchannels = rpng[3]['planes']
		gchannels = gpng[3]['planes']
		bchannels = bpng[3]['planes']


		data = []
		for y in range(h):
			datarow = []
			for x in range(w):
				for i in range(3):

					channels, bits = None, None

					if i % 3 == 0:
						channels = rchannels
						bits = rl[y]
					elif i % 3 == 1:
						channels = gchannels
						bits = gl[y]
					elif i % 3 == 2:
						channels = bchannels
						bits = bl[y]

					if channels == 1:
						datarow += [bits[x]]
					elif channels == 2:
						datarow += [bits[2*x]]
					elif channels == 3:
						s = sum(bits[3*x:3*x+3])//3
						datarow += [s]
					elif channels == 4:
						s = sum(bits[4*x:4*x+3])//3
						datarow += [s]

			data += [datarow]
			datarow = []

	
	with open(resultFile, "wb") as ofs:
		# output is definitely 3 channels
		writer = png.Writer(w,h, greyscale=False, alpha=False)
		writer.write(ofs, data)


	return resultFile

if __name__ == "__main__":
	combineColorChannels("input-placeholder.png", "output-placeholder.png", "output-placeholder.png")
