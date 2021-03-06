# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:16:42 2020

@author: hw
"""


# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 14:24:16 2020

@author: hw
"""
'''
数据情况说明：
1.数据分为正常客户和风险客户
（1）正常客户---正常划扣；
（2）风险客户：逾期、二押、骗贷等风险；这些风险分别在风险类型、收车/退车时间、车辆状态
等字段体现；
2.存在逾期客户将车辆收回后又赎回的情况，该客户后正常用车、正常划扣，归为正常客户
3.客户的还款数据需要进行进一步的换算
4.客户还款状态有逾期、提前还款、正常还款
'''
import pandas as pd
import numpy as np
import math
import datetime

'''对还款数据进行整理 '''
data = pd.read_excel('C:/Users/hw/Desktop/风控还款数据.xlsx','万位用户-GPS分析')
data = data.drop_duplicates(subset = ['身份证号码','车架号'])
dataPay = pd.read_excel('C:/Users/hw/Desktop/风控还款数据.xlsx','更新还款数据')
dataPay['身份证号码'] = ["'"+'%s' % i for i in dataPay['身份证号码']]
dataPay = dataPay.drop_duplicates(subset = ['身份证号码','车架号'])
# from collections import Counter
# z =  Counter(dataPay['身份证号码'])
dataPay = dataPay.drop([0])
# dataPay = dataPay[dataPay['身份证号码'].isin(list(set(data['身份证号码'])))]
df = pd.merge(data,dataPay,on = '身份证号码')
df.to_csv('还款数据v3.csv')

# =============================================================================
# 处理正常客户和风险客户
# =============================================================================

data = pd.read_csv('C:/Users/hw/Desktop/car_risk/还款数据v3.csv')
second = pd.read_excel('C:/Users/hw/Desktop/二次租赁车架号.xlsx',header = None)
# second.columns = ['车架号']
# tem = data[data['车架号'].isin(list(second['车架号']))]
data = data.drop_duplicates(subset = ['身份证号码'])
data = data.drop(['Unnamed: 0', 'Unnamed: 0.1','车架号_y'], axis = 1)

# =============================================================================
# 区分正常客户与风险客户，分别进行分析
# 增加标签列，flag=0或者flag=1，0为坏客户，1为正常客户
# =============================================================================
'''
这里筛选的客户中还包含了部分逾期（恶意逾期/无偿还能力）的客户，公司将他们的车辆进行了回收，将这些也归结为风险客户
收车的客户中还包含部分赎车的客户，这些分为两个阶段 逾期---收车---客户赎回（正常划扣）
将客户去世、车辆大事故以及车辆被警察扣留这三种情况下的客户用车归结为正常用车
'''
nomalsign = [np.NaN, '正常', '客去世', '车辆大事故', '车辆被警察扣留','定位丢失']
nomal_tem = data[data['风险类型'].isin(nomalsign)]


# =============================================================================
# 为进行进一步分析（观察GPS数据在不同的风险下的分布），将风险类型进行细分
# 1.正常客户；2.骗贷等风险客户；3.收车/退车风险客户
# =============================================================================

nomalData = nomal_tem[nomal_tem['收车/退车时间'].isnull()]
# risk_tem = nomal_tem[~nomal_tem['收车/退车时间'].isnull()]
carback =  nomal_tem[~nomal_tem['收车/退车时间'].isnull()]



riskData = data[~data['风险类型'].isin(nomalsign)]
# riskData = riskData.append(risk_tem)

# 删除风险客户中被错误标记的，二次租赁正常客户被错误标记了上一次客户的收车退车时间
# 同时将二次租赁中有风险判断时间的提取出来，归为风险客户

# 筛选收车退车时间小于交车时间
carback1 = carback[carback['交车日期'] < carback['收车/退车时间']]
nomal_tem1 = carback[carback['交车日期'] > carback['收车/退车时间']]


# riskData = riskData.append(nomal_tem1)
# riskData = riskData.drop_duplicates(keep = False)


# nomal_tem1 = riskData[riskData['贷款总额'].isin(['－','二次租赁','二次租赁，无'])]
# riskData = riskData[~riskData['贷款总额'].isin(['－','二次租赁','二次租赁，无'])]


# risk_tem1 = nomal_tem1[nomal_tem1['风险类型'].isin(['二押','欲二押','骗贷','代购'])]
# nomal_tem2 = nomal_tem1[~nomal_tem1['风险类型'].isin(['二押','欲二押','骗贷','代购'])]
nomalData = nomalData.append(nomal_tem1)


nomalData['flag'] = 2
riskData['flag'] = 0
carback1['flag'] = 1

riskData = riskData.append(carback1)







# =============================================================================
# 1.正常客户：（1）目前时间节点
#             (2)客去世、车辆大事故、车辆被警察扣留：风险发生时间点
# 2.风险客户：（1）风险发生时间节点
#            （2）收车/退车：收车、退车时间向前推一周，
# =============================================================================

# 将风险客户中的风险判定时间统一
riskData['风险判定时间'] = pd.to_datetime(riskData['风险判定时间'])
riskData['收车/退车时间'] = pd.to_datetime(riskData['收车/退车时间'])
info_risk = ['二押','代购','骗贷','欲二押']
riskData['最后整合时间'] = None
for i in range(len(riskData)):
    if riskData['风险类型'].iloc[i] in info_risk:
        riskData['最后整合时间'].iloc[i] = riskData['风险判定时间'].iloc[i]
    else:
        riskData['最后整合时间'].iloc[i] = riskData['收车/退车时间'].iloc[i] - datetime.timedelta(days = 3)
        
# 将正常客户中的时间进行统一
nomalData['风险判定时间'] = pd.to_datetime(nomalData['风险判定时间'])
info_nomal = ['客去世', '车辆大事故', '车辆被警察扣留']
nomalData['最后整合时间'] = None
for i in range(len(nomalData)):
    if nomalData['风险类型'].iloc[i] in info_nomal:
        nomalData['最后整合时间'].iloc[i] = nomalData['风险判定时间'].iloc[i]
    else:
        nomalData['最后整合时间'].iloc[i] = pd.to_datetime('2020-06-15')

# =============================================================================
# 计算相关时间参数    
# =============================================================================

# 将风险客户和正常客户进行整合
        
# 添加正常客户中交车日期在3月15号之前的车辆，其最后整合时间设置位2020-03-15
ex_nomalData = nomalData[nomalData['交车日期'] <= '2020-03-15']
ex_nomalData['最后整合时间'] = '2020-03-15'       
            
payData = pd.concat([nomalData,riskData])
payData = pd.concat([payData,ex_nomalData])

payData = payData.reset_index(drop = True)

payData['交车日期'] = pd.to_datetime(payData['交车日期'])
payData['起始划扣日期'] = pd.to_datetime(payData['起始划扣日期'])
payData['最后整合时间'] = pd.to_datetime(payData['最后整合时间'])
payData['duringDay'] = payData['最后整合时间'] - payData['交车日期']
payData['duringDay'] = payData['duringDay'].dt.days
payData['时间差'] = payData['最后整合时间'] - payData['起始划扣日期']
payData['时间差']  = payData['时间差'].dt.days

# =============================================================================
# 修改风险客户的应还期数、未还期数、已还期数
# =============================================================================
payData['实际应还期数'] = payData['应还期数']

paylist1 = payData[payData['flag'] == 0].index
paylist2 = payData[payData['flag'] == 1].index
paylist3 = payData[(payData['最后整合时间'] == '2020-03-15') & (payData['flag'] == 2)].index

paylist = paylist1.append(paylist2)
paylist = paylist.append(paylist3)



for i in list(paylist): 
    if payData['时间差'][i] >= 0:
        payData['实际应还期数'][i] = math.floor(payData['时间差'][i]/30) + 1
    else:
        payData['实际应还期数'][i] = math.floor(payData['时间差'][i]/30)
payData['实际应还期数'] = payData['实际应还期数'].replace(-1,0)
              
payData['实际已还期数'] = payData['已还期数']
for i in list(paylist):
    if payData['实际已还期数'][i] > payData['实际应还期数'][i]:
        payData['实际已还期数'][i] = payData['实际应还期数'][i]
payData['实际未还期数'] = payData['实际应还期数'] - payData['实际已还期数']        
        
# =============================================================================
# 是否针对每一客户计算期状态，逾期率，结清率等，这里逾期状态是截至风险时间点/正常时间点
# 该客户前一期是否正常还款，逾期状态可分为逾期、未逾期、未到还款日期三个状态
# =============================================================================
station = []
payData = payData.reset_index(drop = True)
payData['实际应还期数'] = payData['实际应还期数'].astype(int)
for i in range(len(payData)):
    tem = int(payData['实际应还期数'][i])
    if tem == 0:
        values = 2 #未到还款日期
    elif tem > 0 and int(payData['第'+ str(tem) +'期逾期天数'][i]) <= 0:
        values = 1 #未逾期
    else:
        values = 0 #逾期
    station.append(values)
payData['逾期状态'] = station
# =============================================================================
# 距离最近日期的连续逾期期数
# 计算逾期率
# =============================================================================

# 统计逾期的次数
payData['逾期次数'] = None
for i in range(len(payData)):
    tem = int(payData['实际应还期数'][i])
    if tem == 0:
        payData['逾期次数'][i] = 0
    else:
        overdue = []
        for j in range(1,tem+1):
            overdue.append(int(payData['第'+ str(j) +'期逾期天数'][i]))
        payData['逾期次数'][i] = np.sum(list(map(lambda od:od>0,overdue))) 

# 距离最近还款日期的连续逾期期数
payData['连续逾期期数'] = None
for i in range(len(payData)):
    tem = int(payData['实际应还期数'][i])
    if tem == 0:
        payData['连续逾期期数'][i] = 0
    else:
        con_overdue = 0
        for j in range(tem,0,-1):
            if int(payData['第'+ str(j) +'期逾期天数'][i]) > 0:
                con_overdue += 1
            else:
                break
        payData['连续逾期期数'][i] = con_overdue
payData['逾期率'] = None        
for i in range(len(payData)):
    if payData['实际应还期数'][i] == 0:
        payData['逾期率'][i] = 0
    else:
        payData['逾期率'][i] = round(payData['逾期次数'][i]/payData['实际应还期数'][i],2)
zpayData = payData.drop(['关注时间', '风险判定时间', '风险类型', '风险等级', '收车/退车时间', 
                        '车辆状态', '应还期数', '已还期数','未还期数', '当前状态', '第1期逾期天数',
                        '第2期逾期天数', '第3期逾期天数', '第4期逾期天数', '第5期逾期天数',
                        '第6期逾期天数', '第7期逾期天数', '第8期逾期天数', '第9期逾期天数', 
                        '第10期逾期天数', '第11期逾期天数','第12期逾期天数',
                        '时间差','交车日期','起始划扣日期'],axis = 1)
zpayData['贷款总额'] = zpayData['贷款总额'].replace(['－','二次租赁，无','二次租赁'],np.NaN)
zpayData['贷款总额'] = zpayData['贷款总额'].astype(float)
zpayData.rename(columns={'车架号_x':'车架号'},inplace=True)
zpayData['首付金额'] = zpayData['首付金额'].str.split('=')
# 首付金额数值化
for i in range(len(zpayData)):
    zpayData['首付金额'][i] = int(zpayData['首付金额'][i][0])


df_amount = zpayData.groupby(['车架号'])['贷款总额'].max()
df_number = zpayData.groupby(['车架号'])['贷款总额'].count()
df_zz = pd.merge(df_amount, df_number,on = '车架号')
df_na = zpayData['贷款总额'].isna()
na_series = df_na
names = list(zpayData.loc[na_series,'车架号'])   
t = df_amount.loc[names]
t.index = zpayData.loc[na_series,'贷款总额'].index
zpayData.loc[na_series,'贷款总额'] = t

# 二次租赁的客户的贷款总额需要补齐，根据讨论，可将贷款额度进行0.9-0.95倍处理

# 读取直租业务扣款列表
# data_tem = pd.read_excel('C:/Users/hw/Desktop/car_risk/直租业务扣款表.xlsx')
# data_tem = data_tem.loc[:,['身份证号码','车架号','贷款总额']]
# data_tem['贷款总额'] = data_tem['贷款总额'].replace(['－','二次租赁'],np.NaN)
# data_tem['贷款总额'] = data_tem['贷款总额'].astype(float)
# data_tem['身份证号码']=["'"+'%s' % i for i in data_tem['身份证号码']]
# data_amount = data_tem.groupby(['车架号'])['贷款总额'].max()
# df_na = data_tem['贷款总额'].isna()
# na_series = df_na
# names = list(data_tem.loc[na_series,'车架号'])   
# t = data_amount.loc[names]
# t.index = data_tem.loc[na_series,'贷款总额'].index
# data_tem.loc[na_series,'贷款总额'] = t
# df_full = pd.merge(zpayData,data_tem,on = ['身份证号码','车架号'])

# 将其进行填补

zpayData.to_csv('整理后的还款数据v1.csv')


'''
# =============================================================================
# 将根据最后整合时间来提取GPS数据
# =============================================================================

import datetime
riskData['GPS起始时间'] = riskData['风险判定时间']-datetime.timedelta(days=15)
# 区域报警数据
area = pd.read_csv('C:/Users/hw/Desktop/area_去重.csv')
car_list = list(riskData['车架号'])
area['报警时间'] = pd.to_datetime(area['报警时间'])
finalarea = pd.DataFrame()
for i in car_list:
    tem = area[area['车架号'] == i]
    tep = riskData[riskData['车架号'] == i]
    for j in range(len(tem)):
        tem = tem.reset_index(drop = True)
        if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[0] and pd.to_datetime(tem['date'].iloc[j]) <= tep['风险判定时间'].iloc[0]:
            finalarea = finalarea.append(pd.DataFrame([i,tem['报警时间'].iloc[j]]).T)
'''     