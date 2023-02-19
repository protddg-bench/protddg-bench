#!/usr/bin/env python2.7
import sys, argparse
import numpy as np
from sklearn.linear_model import LinearRegression


def get_options():
	parser = argparse.ArgumentParser(description='Test DDG rediction performance')
	parser.add_argument('filetest', type=str, help='Testing file')
	parser.add_argument('filetrain', type=str, help='Training file')
	parser.add_argument('-v', '--pos-kv' , type=int, dest='pe', default=1, help='Position measure')
	parser.add_argument('-s', '--pos-ks' , type=int, dest='pks', default=2, help='Position key start')
	parser.add_argument('-e', '--pos-ke' , type=int, dest='pke', default=None, help='Position key end')
	args = parser.parse_args()
	filetest=args.filetest
	filetrain=args.filetrain
	pe=args.pe-1
	pks=args.pks-1
	if args.pke!=None:
		pke=args.pke
	else:
		pke=None
	return filetest,filetrain,pe,pks,pke
	



def run_regression(X_test,X_train,y_test,y_train):
	lm = LinearRegression()
	lm.fit(X_train, y_train)
	y_pred = lm.predict(X_test)
	coef=lm.coef_
	intercept=lm.intercept_
	#print coef,intercept
        return lm,y_pred


def read_input_file(namefile,pe=0,pks=1,pke=None):
	y=[]
	X=[]
	f=open(namefile,'r')
	for line in f:
		if line.find('#')==0: continue
		v=line.rstrip().split()
		if pke==None: pke=len(v)
		y.append(float(v[pe]))
		X.append([float(i.split(':')[-1]) for i in v[pks:pke]])
	return np.array(X),np.array(y)


def print_output(y,y_pred):
	assert len(y)==len(y_pred)
	for i in range(len(y)):
		print str(y[i])+'\t'+str(y_pred[i])



if __name__ == "__main__":
	testfile,trainfile,pe,pks,pke=get_options()
	X_test,y_test=read_input_file(testfile,pe,pks,pke)
	X_train,y_train=read_input_file(trainfile,pe,pks,pke)
	model,y_pred=run_regression(X_test,X_train,y_test,y_train)
	print_output(y_test,y_pred)
	
	

