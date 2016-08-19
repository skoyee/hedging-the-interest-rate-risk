# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 09:47:26 2016

@author: skoyee
"""
import pandas as pd
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
#初设贴现率2%，贷款利息率4%
y=0.02
c=0.04
def pv(F,y,n):
    return F/(1+y)**n
def dur(F,y,c,n):
    t=np.array([i for i in range(1,n+1)])
    a=pv(F*c,y,t)
    b=pv(F,y,n)
    p=sum(a,b)
    g=t*a
    h=n*b
    p1=sum(g,h)
    return p1/p

icbc1=pd.read_csv('D:\My Documents\program\DATA\icbc\icbc1.csv')
icbc1.columns=[0.25,0.5,1,5]
lsum=icbc1.ix[4].sum()
asum=icbc1.ix[0:2].sum().sum()
acf=np.array([icbc1.ix[0:2][i].sum() for i in icbc1.columns])

#计算各期限的久期，最后加权
#1.存款 期末计息，直接期限加权
wl=[icbc1.ix[4][i]/lsum for i in icbc1.columns]
dl=(np.array(icbc1.columns)*wl).sum()            #0.403
#2.贷款 统一还款方式为年金付息，期末还本
wa=[icbc1.ix[0:3][i].sum()/asum for i in icbc1.columns]
d0=acf[0]*icbc1.columns[0]/asum
d1=acf[1]*icbc1.columns[1]/asum
d2=dur(acf[2],y,c,1)*acf[2]/asum
d3=dur(acf[3],y,c,5)*acf[3]/asum
da=sum([d0,d1,d2,d3])            #0.76
#3.duration gap
durgap=da-dl*lsum/asum           #0.358
nw=(da-dl*lsum/asum)*asum        #5676946.0323

#国债期货 空头套期保值 10年期国债，c=0.03
db=dur(1,y,0.03,10)                #8.84   F可任意
#需要合同的金额 F0*n  （F0=1m，等于合同数量)
n=nw/db                          #641685
x=n*0.03                         #19250
#利率变动后的对冲情况    y=0.02 
i=0.05;di=i-y
-(da-dl*lsum/asum)*asum*di/(1+i)  #净资产市场价值的变化 -162198=-db*n*di/(1+i)

#1，再把收益率曲线加进来，在第40行改。2，情景分析


