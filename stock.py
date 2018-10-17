
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 20:12:30 2018

@author: Arthur
"""

import realtime_sina as sina
import tkinter as tk
from  tkinter import ttk 
import time
import pandas as pd


class millions(object):	
    def __init__(self, master=None):
        self.root=master
        self.create_frame()
        self.create_table()
        self.show_frame()
        self.init_con()
        self.click_event()
        self.update()
    
    #创建labelframe容器
    def create_frame(self):
        self.fx=tk.LabelFrame(self.root,text='外汇')
        self.inde=tk.LabelFrame(self.root,text='指数')
        self.indus=tk.LabelFrame(self.root,text='行业')
        self.instock=tk.LabelFrame(self.root,text='个股')
        #时间
        self.realtime=time_frame(self.root)
    
    #创建显示表
    def create_table(self):
        self.fx_tb=table_frame(self.fx,show_clm['外汇'])
        self.inde_tb=table_frame(self.inde,show_clm['指数'])
        self.indus_tb=table_frame(self.indus,show_clm['行业'])
        self.instock_tb=table_frame(self.instock,show_clm['个股'])
        
    #容器显示
    def show_frame(self):
        self.fx.grid(row=0, column=0,padx=3, pady=3)
        self.inde.grid(row=0, column=1, padx=3, pady=3)
        self.indus.grid(row=0, column=2, padx=3, pady=3)
        self.instock.grid(row=0, column=3, padx=3, pady=3)
        #时间
        self.realtime.grid(row=1,column=0,columnspan=4,sticky=tk.E)
        
    def init_con(self):
        #行业个股展示初始化
        self.indus_chg='银行'
    
    def click_event(self):
        self.indus_tb.bind("<ButtonRelease-1>",self.tree_select)
        
    def tree_select(self,event):
        try:
            ite=self.indus_tb.selection()[0]
            self.indus_chg=self.indus_tb.item(ite,'values')[0]
        except:
            pass
        else:
            #更新频率降低时，需要此句
            self.instock_tb.insert_tree(self.instock_info.loc[self.indus_chg,:])
    
        
    def update(self):
        #获取数据
        self.get_data()
#        #插入数据
        self.fx_tb.insert_tree(self.fx_info)
        self.inde_tb.insert_tree(self.inde_info)
        self.indus_tb.insert_tree(self.indus_info)
        self.instock_tb.insert_tree(self.instock_info.loc[self.indus_chg,:])
        #循环更新
        self.root.after(1000*15, self.update)
    
    def get_data(self):
        data=get_show()    #获取需要展示的数据，放入update中
        self.fx_info=data.fx_out()   
        self.inde_info=data.index_out()  
        industry_info=data.industry_out()
        self.indus_info=industry_info[0]
        self.instock_info=industry_info[1]
        

show_clm={  '外汇':["名称","汇率","涨跌(基点)"],
            '指数':['代码','名称','涨跌(%)','最新价','成交量(亿)'],
            '行业':['行业','涨跌(%)','标准差(%)','成交量(亿)'],
            '个股':['代码','名称','涨跌(%)','最新价','成交量(亿)',],
           }

        

class table_frame(ttk.Treeview):        # 继承Treeview类
    def __init__(self, master=None,col_name =None,data=None):
        ttk.Treeview.__init__(self,master,columns=col_name,show='headings')
        self.make_tree(col_name)
#        self.insert_tree(data)
        self.pack()
        
    def make_tree(self,f_name):
        for i in f_name:
            self.column(i,width=70)
            self.heading(i,text=i)
            
    def insert_tree(self,data):
        for _ in map(self.delete, self.get_children("")):
            pass 
        le=len(data)
        for i in range(le):   
            self.insert('',i,values=data.iloc[i,:].tolist())
    


class time_frame(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self,parent)
        self.c_time = tk.StringVar()
        tk.Label(self,textvariable=self.c_time).pack()
        self.set_time()
        
    def set_time(self):
        self.c_time.set(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        self.after(1000, self.set_time)



hold_trade_col=['代码','名称','涨跌(%)','最新价','时间','交易方向','交易数量','最新持仓','现金','比率','初始投入']


index_list=['000001','000016','000300','399006']

class get_show():
    def __init__(self):
        self.fx_pd=pd.read_csv('C:/Users/Administrator/Desktop/mill/fx.csv',sep=',',converters={'code':str})
        self.industry_pd=pd.read_csv('C:/Users/Administrator/Desktop/mill/stock.csv',sep=',',converters={'code':str})

        
        
    def fx_out(self):
        new=sina.fx(self.fx_pd['code'])
        new=pd.merge(new,self.fx_pd,how='inner',on=None)
        new['nchg']=((pd.to_numeric(new['price'])-pd.to_numeric(new['pre_close']))*10000).astype(int)
        return new[['name','price','nchg']]
    
    def index_out(self):
        new=sina.index(index_list)
        new['%chg']=((pd.to_numeric(new['price'])/pd.to_numeric(new['pre_close'])-1)*100).round(2)
        new['amount']=(pd.to_numeric(new['amount'])/100000000).round(2)
        return new[['code','name','%chg','price','amount']]
        
    def industry_out(self):
        new=sina.stock(self.industry_pd['code'])
        new=pd.merge(new,self.industry_pd,how='inner',on=None)
        new['%chg']=((pd.to_numeric(new['price'])/pd.to_numeric(new['pre_close'])-1)*100).round(2)
        new['amount']=(pd.to_numeric(new['amount'])/100000000).round(2)
        indus_list=set(new['industry'])
        new.set_index(['industry'], inplace=True)
        j=0
        indus_out=pd.DataFrame(columns=show_clm['行业'])
        for i in indus_list:
            indus_out.loc[j,:]=(i,round(pd.to_numeric(new.loc[i,'%chg']).mean(),2),round(pd.to_numeric(new.loc[i,'%chg']).std(),2),round(pd.to_numeric(new.loc[i,'amount']).sum(),2))
            j+=1
        return [indus_out,new[['code','name','%chg','price','amount']]]
        


if __name__ == '__main__':
    root=tk.Tk()
    m=millions(root)
    root.mainloop()
