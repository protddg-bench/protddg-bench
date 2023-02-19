#!/usr/bin/env  python
from __future__ import print_function
import os, sys, subprocess, argparse


def get_options():
	parser = argparse.ArgumentParser(description='Test DDG prediction performance')
	parser.add_argument('filedata', type=str, help='Input file')
	parser.add_argument('-o','--output', type=str, dest='outfile', default='',help='Output file')
	parser.add_argument('-s','--set', type=str, dest='tset', default='all', help='Test sets')
	parser.add_argument('-t','--threshold', type=float, dest='th', default=0.0, help='Threshold')
	args = parser.parse_args()
	filedata = args.filedata
	tset = args.tset
	th = args.th
	outfile = args.outfile
	prog_dir=os.path.abspath(os.path.dirname(__file__))
	data_dir=prog_dir+'/data'
	prog_test=prog_dir+'/scripts/test-ddg-ml.py'
	return filedata,tset.lower(),th,outfile,prog_dir,data_dir,prog_test
	

def run_process(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	if stderr:
		print ('ERROR: '+stderr.decode(), file=sys.stderr)
	return stdout.rstrip()
	

def run_vb1432(filedata,outfile='',th=0.0):
	bcmd=[prog_test]
	if th!=None: bcmd=bcmd+['-t '+str(th)]
	print ('# CV-10 VB1432')
	for i in range(10):
		cmd=bcmd+[filedata,prog_dir+'/VB1432/vb1432-10fold-split-'+str(i)+'.tsv']
		if outfile!='': cmd=cmd+['-o',outfile+'-vb1432-10fold-split'+str(i)+'-out']
		out=run_process(cmd)
		if out: print (out.decode())
	print ("# PREDICT BROOM WITH VB1432")
	cmd=bcmd+['--train',prog_dir+'/BROOM/train-vb1432-test-broom.tsv']
	cmd=cmd+[filedata,prog_dir+'/BROOM/broom-5fold.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-vb1432-broom-out']
	out=run_process(cmd)
	if out: print (out.decode())
	print  ("# PREDICT SSYM WITH VB1432")
	cmd=bcmd+['--sym','--train',prog_dir+'/SSYM/train-vb1432-test-ssym.tsv']
	cmd=cmd+[filedata,prog_dir+'/SSYM/ssym-5fold.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-vb1432-ssym-out']
	out=run_process(cmd)
	if out: print (out.decode())
	print ("# PREDICT MYOGLOBIN WITH VB1432")
	cmd=bcmd+['-n','--train',prog_dir+'/MYOGLOBIN/train-vb1432-test-myoglobin.tsv']
	cmd=cmd+[filedata,prog_dir+'/MYOGLOBIN/myoglobin.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-vb1432-myoglobin-out']
	out=run_process(cmd)
	if out: print (out.decode())
	print ("# PREDICT P53 WITH VB1432")
	cmd=bcmd+['-n','--train',prog_dir+'/P53/train-vb1432-test-p53.tsv']
	cmd=cmd+[filedata,prog_dir+'/P53/p53.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-vb1432-p53-out']
	out=run_process(cmd)
	if out: print (out.decode())


def run_s2648(filedata,outfile='',th=0.0):
	print ("# CV-10 S2648")
	bcmd=[prog_test]
	if th!=None: bcmd=bcmd+['-t '+str(th)]
	for i in range(10):
		cmd=bcmd+[filedata,prog_dir+'/S2648/s2648-10fold-split-'+str(i)+'.tsv']
		if outfile!='': cmd=cmd+['-o',outfile+'-s2648-10fold-split'+str(i)+'-out']
		out=run_process(cmd)
		if out: print (out.decode())
	print ("# PREDICT BROOM WITH S2648")
	cmd=bcmd+['--train',prog_dir+'/BROOM/train-s2648-test-broom.tsv']
	cmd=cmd+[filedata,prog_dir+'/BROOM/broom-5fold.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-s2648-broom-out']
	out=run_process(cmd)
	if out: print (out.decode())
	print ("# PREDICT SSYM WITH S2648")
	cmd=bcmd+['--sym','--train',prog_dir+'/SSYM/train-s2648-test-ssym.tsv']
	cmd=cmd+[filedata,prog_dir+'/SSYM/ssym-5fold.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-s2648-ssym-out']
	out=run_process(cmd)
	if out: print (out.decode())
	print ("# PREDICT MYOGLOBIN WITH S2648")
	cmd=bcmd+['-n','--train',prog_dir+'/MYOGLOBIN/train-s2648-test-myoglobin.tsv']
	cmd=cmd+[filedata,prog_dir+'/MYOGLOBIN/myoglobin.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-s2648-myoglobin-out']
	out=run_process(cmd)
	if out: print (out.decode())
	print ("# PREDICT P53 WITH S2648")
	cmd=bcmd+['-n','--train',prog_dir+'/P53/train-s2648-test-p53.tsv']
	cmd=cmd+[filedata,prog_dir+'/P53/p53.tsv']
	if outfile!='': cmd=cmd+['-o',outfile+'-s2648-p53-out']
	out=run_process(cmd)
	if out: print (out.decode())


def run_korpm(filedata,outfile='',th=0.0):
	print ("# CV-10 KORPM")
	bcmd=[prog_test]
	if th!=None: bcmd=bcmd+['-t '+str(th)]
	for i in range(10):
		cmd=bcmd+[filedata,prog_dir+'/KORPM/korpm-10fold-split-'+str(i)+'.tsv']
		if outfile!='': cmd=cmd+['-o',outfile+'-korpm-10fold-split-'+str(i)+'-out']
                out=run_process(cmd)
                if out: print (out.decode())
	print ("# PREDICT SSYM WITH KORPM")
	cmd=bcmd+['--sym','--train',prog_dir+'/KORPM/train-korpm-test-ssym.tsv']
	cmd=cmd+[filedata,prog_dir+'/KORPM/ssym-korpm.tsv','-n']
	if outfile!='': cmd=cmd+['-o',outfile+'-korpm-ssym-out']
	out=run_process(cmd)
	if out: print (out.decode())
	print ("# PREDICT S461 WITH KORPM")
	cmd=bcmd+['--train',prog_dir+'/KORPM/train-korpm-test-s461.tsv']
	cmd=cmd+[filedata,prog_dir+'/KORPM/s461-korpm.tsv','-n']
	if outfile!='': cmd=cmd+['-o',outfile+'-korpm-s461-out']
	out=run_process(cmd)
	if out: print (out.decode())
	



def test_libs():
	try:
		import numpy, scipy, sklearn
	except:
		print ('ERROR: To run the test install numpy, scipy and sklearn on your machine.', file=sys.stderr)
		sys.exit(1)


if __name__ == '__main__':
	global prog_dir,data_dir,prog_test
	test_libs()
	filedata,tset,th,outfile,prog_dir,data_dir,prog_test=get_options()
	if tset=='all' or tset=='vb1432':
		run_vb1432(filedata,outfile,th)
	if tset=='all' or tset=='s2648':
		run_s2648(filedata,outfile,th)
	if tset=='all' or tset=='korpm':
		run_korpm(filedata,outfile,th)
