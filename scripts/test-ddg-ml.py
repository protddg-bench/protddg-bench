#!/usr/bin/env python

from __future__ import print_function
import os, sys, tempfile, argparse, subprocess
from scipy import stats



def get_options():
	parser = argparse.ArgumentParser(description='Test DDG rediction performance')
	parser.add_argument('filedata', type=str, help='Input file')
	parser.add_argument('dataset', type=str, help='Dataset file')
	parser.add_argument('--train', type=str, dest='train', default='', help='Training file')
	parser.add_argument('-o','--output', type=str, dest='outfile', default='', help='Output file')
	parser.add_argument('-n','--no-check', dest='nocheck', action='store_true', help='No check datasets')
	parser.add_argument('-v','--validation', dest='valt', action='store_true', help='Validation test')
	parser.add_argument('--sym', dest='sym', action='store_true', help='Test symmetry')
	parser.add_argument('-t', '--threshold' , type=float, dest='th', default=None, help='Classification threshold')
	parser.add_argument('--pi', '--pos-id' , type=int, dest='pi', default=3, help='Position identifiers')
	parser.add_argument('--pd', '--pos-data' , type=int, dest='pd', default=3, help='Position data')
	parser.add_argument('--ps', '--pos-set' , type=int, dest='ps', default=1, help='Position set')
	parser.add_argument('--pe', '--pos-exp' , type=int, dest='pe', default=5, help='Position measure')
	parser.add_argument('--pks', '--pos-ks' , type=int, dest='pks', default=3, help='Position key start')
	parser.add_argument('--pke', '--pos-ke' , type=int, dest='pke', default=4, help='Position key end')
	args = parser.parse_args()	
	filedata=args.filedata
	dataset=args.dataset
	th=args.th
	nocheck=args.nocheck
	train=args.train
	outfile=args.outfile
	pi=args.pi-1
	pd=args.pd-1
	ps=args.ps-1
	pe=args.pe-1
	sym=args.sym
	valt=args.valt
	vpos=range(args.pks-1,args.pke)
	tmp_dir=tempfile.mkdtemp()
	prog_dir=os.path.abspath(os.path.dirname(__file__))
	ml_prog=prog_dir+'/predict-ddg-value.py'
	sc_prog=prog_dir+'/eva-preds.py'
	return filedata,dataset,train,valt,nocheck,outfile,th,sym,(pi,pd),(ps,vpos,pe),tmp_dir,ml_prog,sc_prog 


def getstatusoutput(cmd):
	cmd=cmd.split()
	p = subprocess.Popen(cmd)
	stdout, stderr = p.communicate()
	stderr=subprocess.STDOUT
	return p.returncode, stderr


def run_ml(test_file,train_file):
	vout=[[],[]]
	cmd=[ml_prog,test_file,train_file]
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	if stdout.rstrip():
		lines=stdout.decode().split('\n')
		for line in lines:
			if len(line)==0: continue
			v=line.split()
			try:
				y_real=float(v[0])
				y_pred=float(v[1])
				vout[0].append(y_real)
				vout[1].append(y_pred)
			except:
				print ('WARNING: Incorrect prediction '+line, file=sys.stderr)
		#getstatusoutput('rm '+test_file+' '+train_file)
	else:
		print ('ERROR: '+stderr.decode(), file=sys.stderr)
	return vout
	
	
def get_data(filedata,pos_ids=2,pos_data=2):
	n=0
	c=0
	data={}
	f=open(filedata)
	for line in f:
		v=line.rstrip().split()
		c=c+1
		if line[0]=='#':
			n=len(v)
			continue
		if len(v)==n:
			data[tuple(v[:pos_ids])]=v[pos_data:]
		else:
			print ('ERROR: Line '+str(c)+' contains different elements than header.', file=sys.stderr)
	return data
	

def match_set(fileset,data,pos_set=0,vpos=[2,3],pos_ddg=4):
	dsplit={}
	f=open(fileset)
	for line in f:
		if line[0]=='#': continue
		v=line.rstrip().split()
		nset=v[pos_set]
		dsplit[nset]=dsplit.get(nset,[])
		#ituple=tuple([v[pos_pdb],v[pos_mut],v[pos_ddg]])
		ituple=tuple([v[i] for i in vpos])
		if data.get(ituple,None):
			dsplit[nset].append([ituple,v[pos_ddg]]+data[ituple])
		else:
			print ('WARNING: Data of '+str(ituple)+' not avalible',  file=sys.stderr)
	return dsplit
	


def test_perfromance(filedata,filetest,filetrain,pdata=(2,2),pset=(0,[2,3],4)):
	all_out=[[],[],[]]
	data=get_data(filedata,pdata[0],pdata[1])
	dtest=match_set(filetest,data,pset[0],pset[1],pset[2])
	dtrain=match_set(filetrain,data,pset[0],pset[1],pset[2])
	vals=list(dtest.values())
	if len(vals[0])>0 and len(vals[0])>0:
		text_test='\n'.join(['\t'.join(vs[1:]) for vs in vals[0]])
		idat=['\t'.join(list(vs[0])) for vs in vals[0]]
		tvals=list(dtrain.values())
		text_train='\n'.join(['\t'.join(vs[1:]) for vs in tvals[0]])
		name_test=tmp_dir+'/'+os.path.basename(filetest)+'.test'
		ftest=open(name_test,'w')
		ftest.write(text_test)
		ftest.close()
		name_train=tmp_dir+'/'+os.path.basename(filetrain)+'.train'
		ftrain=open(name_train,'w')
		ftrain.write(text_train)
		ftrain.close()
		set_out=run_ml(name_test,name_train)
		all_out=[idat]+set_out
	return all_out
	


def cross_validation_sets(filedata,filetest,filetrain,pdata=(2,2),pset=(0,[2,3],4)):
	all_out=[[],[],[]]
	text_test={}
	text_train={}
	data=get_data(filedata,pdata[0],pdata[1])
	dtest=match_set(filetest,data,pset[0],pset[1],pset[2])
	dtrain=match_set(filetrain,data,pset[0],pset[1],pset[2])
	ks=list(dtest.keys())
	ks.sort()
	for ki in ks:
		text_test[ki]='\n'.join(['\t'.join(vs[1:]) for vs in dtest[ki]])
		text_train[ki]='\n'.join(['\t'.join(vs[1:]) for vs in dtrain.get(ki,[])])
		idat=['\t'.join(list(vs[0])) for vs in dtest[ki]]
		all_out[0]=all_out[0]+idat
	for ki in ks:
		name_test=tmp_dir+'/'+os.path.basename(filetest)+'.test.'+ki
		ftest=open(name_test,'w')
		ftest.write(text_test[ki])
		ftest.close()
		vtrain=[]
		for kj in ks:
			if kj!=ki and len(text_train[kj])>0: vtrain.append(text_train[kj])
		if len(vtrain)==0: continue
		name_train=tmp_dir+'/'+os.path.basename(filetrain)+'.train.'+ki
		ftrain=open(name_train,'w')
		ftrain.write('\n'.join(vtrain))
		ftrain.close()
		set_out=run_ml(name_test,name_train)
		all_out[1]=all_out[1]+set_out[0]
		all_out[2]=all_out[2]+set_out[1]	
	return all_out
	

def cross_validation(filedata,fileset,pdata=(2,2),pset=(0,[2,3],4)):
	all_out=[[],[],[]]
	dtext={}
	data=get_data(filedata,pdata[0],pdata[1])
	dsplit=match_set(fileset,data,pset[0],pset[1],pset[2])
	ks=list(dsplit.keys())
	ks.sort()
	for ki in ks:
		dtext[ki]='\n'.join(['\t'.join(vs[1:]) for vs in dsplit[ki]])
		idat=['\t'.join(list(vs[0])) for vs in dsplit[ki]]
		all_out[0]=all_out[0]+idat
	for ki in ks:
		name_test=tmp_dir+'/'+os.path.basename(filedata)+'.test.'+ki
		ftest=open(name_test,'w')
		ftest.write(dtext[ki])
		ftest.close()
		vtrain=[]
		for kj in ks:
			if kj!=ki and len(dtext[kj])>0: vtrain.append(dtext[kj])
		if len(vtrain)==0: continue
		name_train=tmp_dir+'/'+os.path.basename(filedata)+'.train.'+ki
		ftrain=open(name_train,'w')
		ftrain.write('\n'.join(vtrain))
		ftrain.close()
		set_out=run_ml(name_test,name_train)
		all_out[1]=all_out[1]+set_out[0]
		all_out[2]=all_out[2]+set_out[1]
	return all_out


def cross_validation_tv(filedata,fileset,pdata=(2,2),pset=(0,[2,3],4)):
	test_out=[[],[],[]]
	val_out=[[],[],[]]
	dtext={}
	data=get_data(filedata,pdata[0],pdata[1])
	dsplit=match_set(fileset,data,pset[0],pset[1],pset[2])
	ks=list(dsplit.keys())
	ks.sort()
	n=len(ks)
	for i in range(n):
		j=(i+1)%n
		ki=ks[i]
		kj=ks[j]
		dtext[ki]='\n'.join(['\t'.join(vs[1:]) for vs in dsplit[ki]])
		idat=['\t'.join(list(vs[0])) for vs in dsplit[ki]]
		idatv=['\t'.join(list(vs[0])) for vs in dsplit[kj]]
		test_out[0]=test_out[0]+idat
		val_out[0]=val_out[0]+idatv
	for i in range(n):
		ki=ks[i]
		name_test=tmp_dir+'/'+os.path.basename(filedata)+'.test.'+ki
		ftest=open(name_test,'w')
		ftest.write(dtext[ki])
		ftest.close()
	for i in range(n):
		j=(i+1)%n
		ki=ks[i]
		kj=ks[j]
		name_test=tmp_dir+'/'+os.path.basename(filedata)+'.test.'+ki
		name_val=tmp_dir+'/'+os.path.basename(filedata)+'.test.'+kj
		vtrain=[]
		for kl in ks:
			if kl!=ki and kl!=kj and len(dtext[kl])>0: vtrain.append(dtext[kl])
		if len(vtrain)==0: continue
		name_train=tmp_dir+'/'+os.path.basename(filedata)+'.train.'+ki
		ftrain=open(name_train,'w')
		ftrain.write('\n'.join(vtrain))
		ftrain.close()
		set_test=run_ml(name_test,name_train)
		set_val=run_ml(name_val,name_train)
		test_out[1]=test_out[1]+set_test[0]
		test_out[2]=test_out[2]+set_test[1]
		val_out[1]=val_out[1]+set_val[0]
		val_out[2]=val_out[2]+set_val[1]
	return test_out,val_out
		
	


def write_output(filename,all_out):
	f=open(filename,'w')
	n=len(all_out[1])
	for i in range(n):
		f.write(all_out[0][i]+'\t'+str(all_out[1][i])+'\t'+str(all_out[2][i])+'\n')
	f.close()
	

def run_eva(outfile,sym,dataset,th):
	cmd=[sc_prog,'--px','0','--py','-1']
	if sym:
		cmd=cmd+['--sym',dataset]
	if th!=None:
		cmd=cmd+['-t',str(th)]
	cmd=cmd+[outfile]
	#print (cmd)
	proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr = proc.communicate()
	if stderr:
		print ('ERROR: '+stderr.decode(),  file=sys.stderr)
	return stdout.rstrip()
	


if __name__ == '__main__':
	global tmp_dir,ml_prog,sc_prog
	all_data,dataset,train,valt,nocheck,doutfile,th,sym,pdata,pset,tmp_dir,ml_prog,sc_prog=get_options()
	if train and nocheck: 
		all_out=test_perfromance(all_data,dataset,train)
		out_text=os.path.basename(dataset)+' '+os.path.basename(train)
	elif train and not nocheck:
		all_out=cross_validation_sets(all_data,dataset,train)
		out_text=os.path.basename(dataset)+' '+os.path.basename(train)
	else:
		if valt:
			all_out,val_out=cross_validation_tv(all_data,dataset)
			out_text='CV-TEST '+os.path.basename(dataset)
			val_text='CV-VAL  '+os.path.basename(dataset)
		else:
			all_out=cross_validation(all_data,dataset)
			out_text='CV '+os.path.basename(dataset)
	if len(all_out[1])>0:
		if not doutfile: 
			outfile=tmp_dir+'/'+os.path.basename(dataset)+'.test'
		else:
			outfile=doutfile+'.test'
		write_output(outfile,all_out)
		out=run_eva(outfile,sym,dataset,th)
		for line in out.decode().split('\n'):
			print (out_text+' '+line)
		if valt and  len(val_out[1])>0:
			if not doutfile: 
				outfile=tmp_dir+'/'+os.path.basename(dataset)+'.val'
			else:
				outfile=doutfile+'.val'
			write_output(outfile,val_out)
			out=run_eva(outfile,sym,dataset,th)
			for line in out.split('\n'):
				print (val_text+' '+line)
	else:
		print ('ERROR: No prediction found check your testing and training sets.', file=sys.stderr)
	#print (tmp_dir)
	getstatusoutput('rm -r '+tmp_dir)

	
