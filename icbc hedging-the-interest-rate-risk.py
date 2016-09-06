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
y0=0.02
c=0.04
def pv(F,y,n):
    return F/(1+y)**n
def PV(F,y,n):
    return sum(pv(F,y,n))
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
t=icbc1.columns=np.array([0.25,0.5,1,5])
lsum=icbc1.ix[4].sum()
asum=icbc1.ix[0:2].sum().sum()
acf=np.array([icbc1.ix[0:2][i].sum() for i in t])
#计算各期限的久期，最后加权
#1.存款 期末计息，直接期限加权
wl=[icbc1.ix[4][i]/lsum for i in icbc1.columns]
dl=(t*wl).sum()            #0.403
#2.贷款 统一还款方式为年金付息，期末还本
wa=[icbc1.ix[0:3][i].sum()/asum for i in t]
d0=acf[0]*t[0]/asum
d1=acf[1]*t[1]/asum
d2=dur(acf[2],y0,c,1)*acf[2]/asum
d3=dur(acf[3],y0,c,5)*acf[3]/asum
da=sum([d0,d1,d2,d3])            #0.763
#3.duration gap
durgap=da-dl*lsum/asum           #0.358
exposure=(da-dl*lsum/asum)*asum        #5676946.0323 资产净值变化
#4.国债期货 空头套期保值 10年期国债，c=0.03
db=dur(1,y0,0.03,10)                #8.84   F可任意
#需要合同的金额 F0*n  （假设F0=1m，等于合同数量)
n=exposure/db                          #641685   F0*n
q=n*0.03                               #加入杠杆后的资金量19250


#资产负债的重新定价风险
class duration(object):
    def __init__(self,icbc1):
        self.Fl=np.array(icbc1.ix[4])
        self.Fa1=np.array(icbc1.ix[0])
        self.Fa2=np.array(icbc1.ix[1])
        self.Fa3=np.array(icbc1.ix[2])
        self.y=y0
    def dl(self,y):
        wl=[icbc1.ix[4][i]/lsum for i in icbc1.columns]
        return (t*wl).sum()
    def da(self,y):
        wa=[icbc1.ix[0:3][i].sum()/asum for i in t]
        d0=acf[0]*t[0]/asum
        d1=acf[1]*t[1]/asum
        d2=dur(acf[2],self.y,c,1)*acf[2]/asum
        d3=dur(acf[3],self.y,c,5)*acf[3]/asum
        return sum([d0,d1,d2,d3])
        
class immu(duration):
    def pvl(self,y):
        return PV(self.Fl,self.y,t)
    def pva(self,y):
        return sum([PV(self.Fa1,self.y,t),PV(self.Fa2,self.y,t),PV(self.Fa3,self.y,t)])
    def expo(self,y):            #资产净值的变化
        return (self.da(self.y)-self.dl(self.y)*lsum/asum)*asum
    def future(self,y):          #期货合约对冲的价值变化
        return dur(1,self.y,0.03,10)*n    #新的久期乘以F0*n

#情景分析  r=[y0-0.003,y0-0.0015,y0,y0+0.0015,y0+0.003]
r=[y0-0.001,y0-0.0005,y0,y0+0.0005,y0+0.001]  #[0.019, 0.0195, 0.02, 0.0205, 0.021]
s=immu(icbc1)
for i in r:
    s.y=i
    plt.plot(s.y,s.pvl(s.y),'b.')
    plt.plot(s.y,s.pva(s.y),'ko')
    plt.xlabel('level of interest rate')
    plt.ylabel('present value')
    
for i in r:
    s.y=i
    plt.plot(s.y,s.expo(s.y),'yo')       #资产净值变化应加负号
    plt.plot(s.y,s.future(s.y),'k.') 
for i in r:
    s.y=i
    print(np.array([s.future(i)-s.expo(i)])*(s.y-y0)/(1+s.y)) ##利率变动后对冲情况
for i in r:
    s.y=i
    plt.plot(s.y,np.array([s.future(s.y)-s.expo(s.y)])*(s.y-y0)/(1+s.y),'ro')
    plt.xlabel('level of interest rate')
    plt.ylabel('value')



