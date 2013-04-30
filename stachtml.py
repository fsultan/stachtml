#!/usr/bin/env python

import sys
import os
from os.path import join
import shutil
import argparse
import pystache
#from pystache import Renderer

def parse_args():                                                          
	p = argparse.ArgumentParser(description='stashtml')
	p.add_argument('-v', dest='verbose', action='store_true')
	p.add_argument('-s', dest='write_safe', action='store_true', 
					help='will not overwrite files in output directory')
	p.add_argument('--ext', dest='ext', nargs='+', default=['html'])
	p.add_argument('--src', help='input file or directory')
	p.add_argument('--dst', help='output file or directory', )
	p.add_argument('--context', help='default context')
	return p.parse_args()

def parse_file(src, context={}, dst=None):
	tpl = open(src, 'r').read()
	if dst and os.path.isdir(dst):
		sys.exit('output destination exits as a directory')
	elif dst:
		outfile = open(dst, 'w')
	else:
		outfile = sys.stdout
	#renderer = pystache.Renderer()
	#context = {'last_word': 'tohtho tho t'}
	#outfile.write(renderer.render_path(tpl, context))
	outfile.write(pystache.render(tpl, context))

def main():                                                                     
	args = parse_args()
	if args.src and os.path.isdir(args.src):
		if os.path.isdir and not os.path.isdir(args.dst):
			sys.exit("src and dst type must match")
	if args.verbose:
		print 'starting recursive processing of %s into %s' % (
			args.src, args.dst)

	parse_exts = [".%s" % ext for ext in args.ext]
	print parse_exts

	if args.context and os.path.isfile(args.context):
		context = open(args.context, 'r').read()
	elif args.context:
		context = args.context
	else:
		context = {}

	if args.src and os.path.isdir(args.src):
		if args.ext == 'mustache':
			sys.exit('refusing to recursively parse on extension mustache')
		for dirpath, dirnames, filenames in os.walk(args.src):
			
			dst_dirpath = join(args.dst,os.path.basename(dirpath))
			if not os.path.isdir(dst_dirpath):
				os.makedirs(dst_dirpath)
			print 'output : %s' % dst_dirpath

			for filename in filenames:
				abs_filepath = join(dirpath, filename)
				name, ext = os.path.splitext(abs_filepath)
				print name, ext
				if ext in parse_exts:
					print 'parsing %s' % filename
					parse_file(abs_filepath, context, 
						join(dst_dirpath, filename))
				elif ext == '.mustache':
					print 'skipping mustache file %s' % filename
				else:
					print 'copying without modification %s' % filename
					shutil.copy(abs_filepath, join(dst_dirpath, filename))
	elif args.src and os.path.isfile(args.src):
		parse_file(args.src, context, args.dst)
	else:
		parse_file(sys.stdin, context, args.dst)


if __name__ == '__main__':
	main()

