#!/usr/bin/env  python
import os, sys, subprocess


def get_options():
	prog_dir=os.path.abspath(os.path.dirname(__file__))
	data_dir=prog_dir+'/data'
	prog_test=prog_dir+'/scripts/test-ddg-ml.py'
	return prog_dir,data_dir,prog_test
	

def run_process(cmd):
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	if stderr:
		print >>sys.stderr,'ERROR:',stderr
	return stdout.rstrip()
	

def run_vb1432(filedata,th=0.0):
	bcmd=[prog_test]
	if th!=None: bcmd=bcmd+['-t'+str(th)]
	print '# CV-10 VB1432'
	for i in range(1):
		cmd=bcmd+[filedata,prog_dir+'/VB1432/vb1432-10fold-split-'+str(i)+'.tsv']
		out=run_process(cmd)
		if out: print out
	print "# PREDICT BROOM WITH VB1432"
	cmd=bcmd+['--train',prog_dir+'/BROOM/train-vb1432-test-broom.tsv']
	cmd=cmd+[filedata,prog_dir+'/BROOM/broom-5fold.tsv']
	out=run_process(cmd)
	if out: print out
	print  "# PREDICT SSYM WITH VB1432"
	cmd=bcmd+['--sym','--train',prog_dir+'/SSYM/train-vb1432-test-ssym.tsv']
	cmd=cmd+[filedata,prog_dir+'/SSYM/ssym-5fold.tsv']	
	out=run_process(cmd)
	if out: print out
	print "# PREDICT MYOGLOBIN WITH VB1432"
	cmd=bcmd+['-n','--train',prog_dir+'/MYOGLOBIN/train-vb1432-test-myoglobin.tsv']
	cmd=cmd+[filedata,prog_dir+'/MYOGLOBIN/myoglobin.tsv']
	out=run_process(cmd)
	if out: print out
	print "# PREDICT P53 WITH VB1432"
	cmd=bcmd+['-n','--train',prog_dir+'/P53/train-vb1432-test-p53.tsv']
	cmd=cmd+[filedata,prog_dir+'/P53/p53.tsv']
	out=run_process(cmd)
	if out: print out


def run_s2648(filedata,th=0.0):
	print "# CV-10 S2648"
	bcmd=[prog_test]
	if th!=None: bcmd=bcmd+['-t'+str(th)]
	for i in range(10):
		cmd=bcmd+[filedata,prog_dir+'/S2648/s2648-10fold-split-'+str(i)+'.tsv']
		out=run_process(cmd)
		if out: print out
	print "# PREDICT BROOM WITH S2648"
	cmd=bcmd+['--train',prog_dir+'/BROOM/train-s2648-test-broom.tsv']
	cmd=cmd+[filedata,prog_dir+'/BROOM/broom-5fold.tsv']
	out=run_process(cmd)
	if out: print out
	print "# PREDICT SSYM WITH S2648"
	cmd=bcmd+['--sym','--train',prog_dir+'/SSYM/train-s2648-test-ssym.tsv']
	cmd=cmd+[filedata,prog_dir+'/SSYM/ssym-5fold.tsv']
	out=run_process(cmd)
	if out: print out
	print "# PREDICT MYOGLOBIN WITH S2648"
	cmd=bcmd+['-n','--train',prog_dir+'/MYOGLOBIN/train-s2648-test-myoglobin.tsv']
	cmd=cmd+[filedata,prog_dir+'/MYOGLOBIN/myoglobin.tsv']
	out=run_process(cmd)
	if out: print out
	print "# PREDICT P53 WITH S2648"
	cmd=bcmd+['-n','--train',prog_dir+'/P53/train-s2648-test-p53.tsv']
	cmd=cmd+[filedata,prog_dir+'/P53/p53.tsv']
	out=run_process(cmd)
	if out: print out


def test_libs():
	try:
		import numpy, scipy, sklearn
	except:
		print >> sys.stderr,'ERROR: To run the test install numpy, scipy and sklearn on your machine.'
		sys.exit(1)


if __name__ == '__main__':
	global prog_dir,data_dir,prog_test
	test_libs()
	filedata=sys.argv[1]
	prog_dir,data_dir,prog_test=get_options()
	run_vb1432(filedata)
	run_s2648(filedata)
