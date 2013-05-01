#!/usr/bin/env python

import sys
import os
from os.path import join
import ast
import shutil
import argparse
import pystache
#from pystache import Renderer

PARSE_EXTENTION = 'html'

def parse_args():                                                          
    p = argparse.ArgumentParser(description='stashtml')
    p.add_argument('-v', dest='verbose', action='store_true')
    p.add_argument('-s', dest='write_safe', action='store_true', 
                    help='will not overwrite files in output directory')
    p.add_argument('--ext', dest='ext', default='html')
    p.add_argument('src', help='input file or directory')
    p.add_argument('dst', help='output file or directory', )
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
    #outfile.write(renderer.render_path(tpl, context))
    outfile.write(pystache.render(tpl, context))

def recursly_parse_files(srcdir, context={}, dstdir):
    if PARSE_EXTENTION == 'mustache':
            sys.exit('refusing to recursively parse on extension mustache')
    if args.verbose:
        print 'recursively processing %s into %s' % (srcdir, dstdir)
        
    for dirpath, dirnames, filenames in os.walk(srcdir):
        dst_dirpath = join(args.dst,os.path.basename(dirpath))
        
        if not os.path.isdir(dst_dirpath):
            os.makedirs(dst_dirpath)
        print 'output : %s' % dst_dirpath

        for filename in filenames:
            abs_filepath = join(dirpath, filename)
            name, ext = os.path.splitext(abs_filepath)
            print name, ext
            if ext == PARSE_EXTENTION:
                print 'parsing %s' % filename
                parse_file(abs_filepath, context, 
                    join(dst_dirpath, filename))
            elif ext == '.mustache':
                print 'skipping mustache file %s' % filename
            else:
                print 'copying without modification %s' % filename
                shutil.copy(abs_filepath, join(dst_dirpath, filename))

def main():                                                                     
    args = parse_args()
    
    if args.context and os.path.isfile(args.context):
        context_text = open(args.context, 'r').read()
        context = ast.literal_eval(context_text)
    elif args.context:
        context = ast.literal_eval(args.context)
    else:
        context = {}
        
    if os.path.isdir(args.src) and os.path.isdir(args.dst):
        recursly_parse_files(args.src, context, args.dst)
    elif os.path.isfile(args.src) and os.path.isfile(args.dst):
        parse_file(args.src, context, args.dst)
    elif os.path.isfile(args.src) and os.path.isdir(args.dst):
        filename = os.path.basename(args.src)
        dst = join(dirpath, filename)
        parse_file(args.src, context, dst)
    elif os.path.isdir(args.src) and os.path.isfile(args.dst):        
        sys.exit("cannot parse a directory into a file")
    else:
        sys.exit("Could not understand options")
        

if __name__ == '__main__':
    main()

