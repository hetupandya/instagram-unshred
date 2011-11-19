## Usage: ./unshred.py source destination [shreds=20]
## This solution uses rms to match two columns. 
## If there's a conflict in that then it applies 
## some tricks to determine correct order

import sys
from PIL import Image
from math import sqrt

__author__ = "hetu"
__license__ = "GPL"

class ColImage(object):           
	def __init__(self, img):
		self.image = img
		self.data = img.getdata()
		self.w = img.size[0]
	def getpixel(self, x, y):
		return self.data[self.w * y + x]
		
def rgb_diff(c1, c2):
    return tuple([x-y for x, y in zip(c1, c2)])

def rms(cdiff):
    return sqrt(sum((x*x for x in cdiff)))

def col_diff(s1, s2):
	w, h = s1.image.size
	
	s1_right = [s1.getpixel(w-1, i) for i in xrange(h)]
	s2_left = [s2.getpixel(0, i) for i in xrange(h)]	
		
	diffs = [rgb_diff(c1, c2) for c1, c2 in zip(s1_right, s2_left)]
	diff = sum([rms(diff) for diff in diffs])
	return diff

def unshred(src_image, output_image, shred_count):
	image = Image.open(src_image)
	result = Image.new("RGBA", image.size)
	
	width, height = image.size
	shred_width = width/shred_count

	cols = [ColImage(image.crop((i*shred_width, 0, (i+1)*shred_width, height))) for i in xrange(shred_count)]
	idxs = range(shred_count)

	follows = []
	unmatched = range(shred_count)

	beyond_threshhold_columns = []

	for k in idxs:	
		li = [float(col_diff(cols[k], cols[j])) for j in idxs]
		minval = min(li)
		matched_col = [i for i, v in enumerate(li) if v == minval][0]
		
		#if diff is beyond threshhold that means it can be first col
		if (minval>25000):
			beyond_threshhold_columns.append((matched_col,minval))
		
		#print k,matched_col,'min:' + str(minval)
		follows.append((k,matched_col))
		try:
			unmatched.remove(matched_col)		
		except ValueError:
			pass		
	
	if (len(unmatched)>0):
		first_col = unmatched[0]        
		#print 'unmatched, set as first col:', first_col
	elif (len(beyond_threshhold_columns)>0):
		max_min = max([v for t,v in beyond_threshhold_columns])
		first_col = [i for i, v in beyond_threshhold_columns if v == max_min][0]
		#print 'beyond threshhold, set as first col:', first_col
			
	out_seq = []
	current_col = first_col
	for count,k in enumerate(follows):
		result.paste(cols[follows[current_col][0]].image, (count*shred_width, 0))
		current_col = follows[current_col][1]
		out_seq.append(current_col)
		count+=1

	#print out_seq
	result.save(output_image)
	
def main(argv):
    try:
        src_image = argv[1]
        output_image = argv[2]
        SHREDS = 20 if len(argv) <= 3 else int(argv[3])
    except IndexError:
        print >> sys.stderr, ('Usage: %s [source] [dest] [shreds=20]' % argv[0])
        exit(1)

    try:        
        unshred(src_image, output_image, SHREDS)        
    except IOError, e:
        print >> sys.stderr, e
        exit(2)

if __name__ == '__main__':
    main(sys.argv)	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	

	
	
	
	

		