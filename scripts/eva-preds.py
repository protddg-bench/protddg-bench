#!/usr/bin/env python2.7

import sys, argparse, warnings
import numpy as np
from scipy import stats
from sklearn import metrics
warnings.filterwarnings('ignore')

def get_options():
        parser = argparse.ArgumentParser(description='Calculate prediction performances')
        parser.add_argument('filename', type=str, help='Prediction file')
        parser.add_argument('--py','--pos-real', type=int, dest='py', default=-1, help='Column real values')
        parser.add_argument('--px','--pos-pred', type=int, dest='px', default=0, help='Column prediction values')
	parser.add_argument('-t', '--threshold' , type=float, dest='th', default=None, help='Classification threshold')
	parser.add_argument('--sym', type=str, dest='idata', default='', help='Prediction file')
	args = parser.parse_args()
	filename=args.filename
        i_real=args.py-1
        i_pred=args.px-1
        th=args.th
	idata=args.idata
	return filename,i_real,i_pred,th,idata


def get_reg_scores(y_real,y_pred):
	scores=None
	if len(y_pred)==len(y_real) and len(y_real)>2:
		n=len(y_real)
		y=y_real
		x_i=y_pred
		rkt=stats.kendalltau(y,x_i)
		rsp=stats.spearmanr(y,x_i)
		rpe=stats.pearsonr(y,x_i)
		rmse=np.sqrt(np.mean((y - x_i)**2))
		mae=np.mean(np.absolute(y - x_i))
		scores=(rpe[0],rsp[0],rkt[0],rmse,mae,n)
	else:
		print >> sys.stderr,'ERROR: Incorrect predictions.'
	return scores



def get_class_scores(y_pred,y_real,th,h=True):
	scores=None
	if len(y_pred)==len(y_real) and len(y_real)>2:
		n=len(y_pred)
		if h:
			y=1*( y_real > th )
			x_i=1*( y_pred > th )
		else:
			y=1*( y_real < th )
			x_i=1*( y_pred < th )
		acc=metrics.recall_score(y, x_i,average='macro')
		f1=metrics.f1_score(y, x_i,average='macro')
		mc=metrics.matthews_corrcoef(y, x_i)
		try:
			auc=metrics.roc_auc_score(y, x_i)
		except:
			auc=0.0
		scores=(acc,mc,f1,auc,n)
	else:
		print >> sys.stderr,'ERROR: Incorrect predictions.'
	return scores


def read_output(fileout,pos_real=0,pos_pred=1):
	vy=[]
	vx=[]
	f=open(fileout)
	for line in f:
		v=line.rstrip().split()
		try:
			y=float(v[pos_real])
			x=float(v[pos_pred])
			vx.append(x)
			vy.append(y)
		except:
			print >> sys.stderr,'ERROR: Incorrect line',line.rstrip()
	return np.array(vx),np.array(vy)



def get_sym_scores(fileout,idata,ids1=[0,1],ids2=[2,3]):
	scores=None
	d1={}
	d2={}
	dm={}
	v1=[]
	v2=[]
	f=open(fileout)	
	for line in f:
		v=line.rstrip().split()
		d1[tuple([v[i] for i in ids1])]=[float(v[-2]),float(v[-1])]
	f.close()
	f=open(idata)
	for line in f:
		v=line.rstrip().split()
		d2[tuple([v[i] for i in ids2])]=(v[-2],v[-1])
	f.close()
	for k in d1.keys():
		if d2.get(k,None):
			n=d2[k]
			dm[n]=dm.get(n,[])
			dm[n].append(list(k)+d1[k])
	ks=list(set([i for i,j in dm.keys()]))
	if len(ks)==0: return scores
	delta=0.0
	adelta=0.0
	for k in ks:
		vs1=dm.get((k,'DIR'),None)
		vs2=dm.get((k,'INV'),None)
		if vs1 and vs2:
			v1.append(vs1[0][-1])
			v2.append(vs2[0][-1])
			delta=delta+vs1[0][-1]+vs2[0][-1]
			adelta=adelta+np.abs(vs1[0][-1]+vs2[0][-1])
		else:
			print >> sys.stderr,'WARNING: No direct/inverse label for mutation ID.'
	rpe=stats.pearsonr(v1,v2)[0]
	if len(v1)>0: 
		scores=(rpe,delta/(2*len(v1)),len(v1))
	return scores	



if __name__ == '__main__':
	fileout,i_real,i_pred,th,idata=get_options()
	vx,vy=read_output(fileout,i_real,i_pred)
	reg_scores=get_reg_scores(vy,vx)
	if reg_scores: 
		print 'PEARSONR: %.3f SPEARMANR: %.3f KENDALLTAU: %.3f RMSE: %.2f MAE: %.2f' %reg_scores[:5],
	if th!=None:
		class_scores=get_class_scores(vy,vx,th)
		if class_scores: 
			print  'TH: %.2f' %th+' Q2: %.2f MCC: %.2f F1: %.2f AUC: %.2f' %class_scores[:4],
	if reg_scores: print 'N: %d' %reg_scores[-1]
	if idata:	
		scores=get_sym_scores(fileout,idata)
		if scores:
			print 'SYMMETRY-SCORES  R-DIR/ENV: %.2f BIAS: %.2f N: %d' %scores
		else:
			print >> sys.stderr,'ERROR: Check for ID and DIR/INV annotation your input data.'
	

	
