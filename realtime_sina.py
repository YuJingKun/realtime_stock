# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:18:09 2018
@author: Arthur
"""

import pandas as pd
import re
import urllib         

# =============================================================================
#
#     获取指数实时交易数据
# 
# Parameters
# ------
#     symbols : 股票代码，list、tuple、Series格式
#     
# return
# -------
#     DataFrame 实时交易数据
#     0：name，股票名字
#     1：open，今日开盘价
#     2：pre_close，昨日收盘价
#     3：price，当前价格
#     4：high，今日最高价
#     5：low，今日最低价
#     6：bid，0
#     7：ask，0
#     8：volumn，成交量 maybe you need do volumn/100
#     9：amount，成交金额（元 CNY）
#     10：b1_v，0
#     11：b1_p，0
#     12：b2_v，0
#     13：b2_p，0
#     14：b3_v，0
#     15：b3_p，0
#     16：b4_v，0
#     17：b4_p，0
#     18：b5_v，0
#     19：b5_p，0
#     20：a1_v，0
#     21：a1_p，0
#     ...
#     30：date，日期；
#     31：time，时间；
# =============================================================================

def index(symbols=None):
    symbols_str = ''
    for code in symbols:
        symbols_str+=('sh%s'%code if code[0] in ['0'] or code[:2] in ['399'] else 'sz%s'%code) + ','
    symbols_str = symbols_str[:-1] if len(symbols_str) > 8 else symbols_str
    url="http://hq.sinajs.cn/list=%s"%symbols_str
    response=urllib.request.urlopen(url,timeout=10)
    text = response.read().decode('GBK')
    reg = re.compile(r'\="(.*?)\";')
    data = reg.findall(text)
    regSym = re.compile(r'(?:sh|sz)(.*?)\=')
    syms = regSym.findall(text)
    data_list = []
    syms_list = []
    for index, row in enumerate(data):
        if len(row)>1:
            data_list.append([astr for astr in row.split(',')])
            syms_list.append(syms[index])
    out = pd.DataFrame(data_list, columns=['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount',
                                           'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p',
                                           'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p', 'date', 'time', 's'])
    out = out.drop('s', axis=1)
    out['code'] = syms_list
    return out


# =============================================================================
#
#     获取股票实时交易数据
# 
# Parameters
# ------
#     symbols : 股票代码，list、tuple、Series格式
#     
# return
# -------
#     DataFrame 实时交易数据
#     0：name，股票名字
#     1：open，今日开盘价
#     2：pre_close，昨日收盘价
#     3：price，当前价格
#     4：high，今日最高价
#     5：low，今日最低价
#     6：bid，竞买价，即“买一”报价
#     7：ask，竞卖价，即“卖一”报价
#     8：volumn，成交量 maybe you need do volumn/100
#     9：amount，成交金额（元 CNY）
#     10：b1_v，委买一（笔数 bid volume）
#     11：b1_p，委买一（价格 bid price）
#     12：b2_v，“买二”
#     13：b2_p，“买二”
#     14：b3_v，“买三”
#     15：b3_p，“买三”
#     16：b4_v，“买四”
#     17：b4_p，“买四”
#     18：b5_v，“买五”
#     19：b5_p，“买五”
#     20：a1_v，委卖一（笔数 ask volume）
#     21：a1_p，委卖一（价格 ask price）
#     ...
#     30：date，日期；
#     31：time，时间；
# =============================================================================

def stock(symbols=None):
    symbols_str = ''
    for code in symbols:
        symbols_str+=('sh%s'%code if code[:1] in ['5', '6', '9'] or code[:2] in ['11', '13'] else 'sz%s'%code) + ','
    symbols_str = symbols_str[:-1] if len(symbols_str) > 8 else symbols_str
    url="http://hq.sinajs.cn/list=%s"%symbols_str
    response=urllib.request.urlopen(url,timeout=10)
    text = response.read().decode('GBK')
    reg = re.compile(r'\="(.*?)\";')
    data = reg.findall(text)
    regSym = re.compile(r'(?:sh|sz)(.*?)\=')
    syms = regSym.findall(text)
    data_list = []
    syms_list = []
    for index, row in enumerate(data):
        if len(row)>1:
            data_list.append([astr for astr in row.split(',')])
            syms_list.append(syms[index])
    out = pd.DataFrame(data_list, columns=['name', 'open', 'pre_close', 'price', 'high', 'low', 'bid', 'ask', 'volume', 'amount',
                                           'b1_v', 'b1_p', 'b2_v', 'b2_p', 'b3_v', 'b3_p', 'b4_v', 'b4_p', 'b5_v', 'b5_p',
                                           'a1_v', 'a1_p', 'a2_v', 'a2_p', 'a3_v', 'a3_p', 'a4_v', 'a4_p', 'a5_v', 'a5_p', 'date', 'time', 's'])
    out = out.drop('s', axis=1)
    out['code'] = syms_list
#    将成交量转换成手
#    ls = [cls for cls in df.columns if '_v' in cls]
#    for txt in ls:
#        df[txt] = df[txt].map(lambda x : x[:-2])
    return out

        
def fx(symbols):
    code=",".join(symbols)
    url = "http://hq.sinajs.cn/list="  + code
    response = urllib.request.urlopen(url)
    text = response.read().decode('GBK') 
    reg = re.compile(r'\="(.*?)\";')
    data = reg.findall(text)  
    regSym = re.compile(r'(?:str_)(.*?)\=')
    syms = regSym.findall(text)
    data_list = []
    syms_list = []
    for index, row in enumerate(data):
        if len(row)>1:
            data_list.append([astr for astr in row.split(',')])
            syms_list.append(syms[index])
    out = pd.DataFrame(data_list, columns=['time',  'price1', 'price2','pre_close','volatility','open','high','low', 'price','l_name','r','r1',
                                           'amplitude','provider','unknown1','unknown2','unknown3','date'])
    out['code'] = syms_list
    return out
