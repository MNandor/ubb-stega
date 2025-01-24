#!/bin/python3


# required: pypng
import png


def magic(firstFile='a.png', secondFile='b.png', outputFile='res.png'):
	with open(firstFile, 'rb') as ifsa, open(secondFile, 'rb') as ifsb:
		apng = png.Reader(file=ifsa).read()
		bpng = png.Reader(file=ifsb).read()

		# Checks are skipped because I'm lazy, but basically
		# Pictures have to be the same size
		# Both must have 4 channels: RBGA
		# Pictures are assumed to be greyscale (R=G=B)
		w, h = apng[:2]
		
		channels = apng[3]['planes']


		# Actual pixel data
		apng, bpng = list(apng[2]), list(bpng[2])


		# For each pixel
		for y in range(h):
			for x in range(w):
				actX = 4*x
				
				# The rule is that the darkest pixel of b
				# Can't be darker than the lightest pixel of a
				# The simplest solution is to have
				# a be 0-127 and b 128-255
				acolor = apng[y][actX]//2
				bcolor = bpng[y][actX]//2+128

				# math happens here
				opa = 255 + acolor-bcolor
				if opa == 0:
					opa = 1
				lig = 255*acolor//opa

				# Store new lightness value
				for i in range(3):
					apng[y][actX+i]=lig
				
				# Store new opacity value
				apng[y][actX+3]=opa
		
		# Output
		with open(outputFile, 'wb') as ofs:
			png.Writer(w,h,greyscale=False, alpha=True).write(ofs, apng)
	return outputFile

