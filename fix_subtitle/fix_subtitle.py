#!/usr/bin/env python
"""
	Fix subtitle encoding - convert from ISO8859-16 to UTF-8
"""
import sys
import shutil

BAD_CRITICS = ('\xfe', '\xe3', '\xba')

def fix_file(subfile):
	move = False
	with open(subfile, 'r') as f:
		data = f.read()
		for c in BAD_CRITICS:
			if c in data:
				data = data.decode("iso8859-16").encode("utf-8")
				with open(subfile + '-utf', 'w') as fo:
					fo.write(data)
				print "DONE"
				move = True
				break
		else:
			print "Not found"
	if move:
		shutil.move(subfile, subfile + '-original')
		shutil.move(subfile + '-utf', subfile)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: %s <file.srt>" % sys.argv[0]
		sys.exit(1)
	fix_file(sys.argv[1])
