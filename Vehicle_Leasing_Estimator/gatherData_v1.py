# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:34:22 2020

@author: hw
"""

import pandas as pd
import os
import datetime
# import numpy as np

financialBigData = pd.read_csv('征信大数据.csv',index_col = 0)
# userInfo = pd.read_csv('客户基本信息.csv',index_col = 0)
payData = pd.read_csv('整理后的还款数据v1.csv',index_col = 0)
# payData = payData.drop(['Unnamed: 0'],axis = 1)
financialBigData = financialBigData.drop(['attribution'],axis = 1)
allData = pd.merge(financialBigData,payData,on = '身份证号码')
# allData.to_csv('用于初步分析的数据.csv')

# 读取GPS数据
filePath = 'C:\\Users\\hw\\Desktop\\GPS整合数据\\'
filename = os.listdir(filePath)
for i in filename:
    var = i.split('.')[0]
    globals()[var] = pd.read_csv(filePath + i)
    # globals()[var] = pd.concat(globals()[var])
    # globals()[var].to_csv(var + '.csv')

# =============================================================================
# 依据时间整合报警数据，以15天为分析周期
# =============================================================================
payData['最后整合时间'] = pd.to_datetime(payData['最后整合时间'])
payData['GPS起始时间'] = payData['最后整合时间'] - datetime.timedelta(days=15)
# 区域报警数据
car_list = list(payData['车架号'])
use = payData.loc[:,['车架号','GPS起始时间','flag']]
# 1.出区域报警数据
area['报警时间'] = pd.to_datetime(area['报警时间'])
finalarea = pd.DataFrame()
for i in car_list:
    tem = area[area['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                finalarea = finalarea.append(tem.iloc[j,:])

# 对区域报警数据进行汇总统计
warning_area = finalarea.groupby(['车架号','报警类型','GPS起始时间'])['行政区域称'].agg(['count','unique']).reset_index()
warning_area['区域数'] = [len(x) for x in list(warning_area['unique'])]
warning_area = warning_area.drop(['unique'],axis = 1)
warning_area_in = warning_area[warning_area['报警类型'] == '入区域']
warning_area_in.rename(columns={'count':'入区域报警次数','区域数':'入区域区域数'},inplace=True)
warning_area_out = warning_area[warning_area['报警类型'] == '出区域']
warning_area_out.rename(columns={'count':'出区域报警次数','区域数':'出区域区域数'},inplace=True)                       
warning_area = pd.merge(warning_area_in, warning_area_out, on = ['车架号','GPS起始时间'], how = 'outer')
# use = payData.loc[:,['车架号','GPS起始时间','flag']]
# areacopy = area.copy()
# areacopy = areacopy.groupby(['车架号','报警类型'])['行政区域称'].agg(['count','unique']).reset_index()
# areacopy = pd.merge(areacopy, use,on = '车架号',how = 'left')
# areacopy = areacopy[areacopy['count'] >= 10]
# area_in = areacopy
# area_id = list(set(areacopy[areacopy['flag'] == 0]['车架号']))

# 在区域报警中，车辆一般只进出同一区域，故出区域数和入区域数的统计无意义，可以进行删除
warning_area = warning_area.drop(['入区域区域数','出区域区域数'],axis = 1)
warning_area = warning_area.drop(['报警类型_x','报警类型_y'],axis = 1)
notarea = pd.merge(warning_area,use,on = ['车架号','GPS起始时间'],how = 'left')
notarea.to_csv('出区域报警初步分析.csv')

# area_id_15 = list(set(notarea[notarea['flag'] == 0]['车架号']))
               
# 2.光感报警数据
isWireless['date'] = pd.to_datetime(isWireless['date'])
finalisWireless = pd.DataFrame()
for i in car_list:
    tem = isWireless[isWireless['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                finalisWireless = finalisWireless.append(tem.iloc[j,:])


# 对光感报警数据进行汇总统计
warning_isWireless = finalisWireless.groupby(['车架号','GPS起始时间']).agg({'报警次数':'sum','不同地点报警次数':'sum'}).reset_index()
warning_isWireless.rename(columns = {'报警次数':'光感报警报警次数','不同地点报警次数':'光感报警不同地点报警次数'},inplace = True)
notfinalisWireless = pd.merge(warning_isWireless,use,on = ['车架号','GPS起始时间'],how = 'left')
notfinalisWireless.to_csv('光感报警初步分析.csv')
# 3.停车超时报警数据
# staytimeout['date'] = pd.to_datetime(staytimeout['date'])
# finalstaytimeout = pd.DataFrame()
# for i in car_list:
#     tem = staytimeout[staytimeout['车架号'] == i]
#     tep = payData[payData['车架号'] == i]
#     for k in range(len(tep)):
#         for j in range(len(tem)):
#             tem = tem.reset_index(drop = True)
#             tem['GPS起始时间'] = None
#             if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
#                 tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
#                 finalstaytimeout = finalstaytimeout.append(tem.iloc[j,:])

'''
# 4.围栏报警数据 
fence['date'] = pd.to_datetime(fence['date'])
fence = fence[~fence['围栏名称'].str.contains('在库围栏')]
finalfence = pd.DataFrame()
for i in car_list:
    tem = fence[fence['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    for j in range(len(tem)):
        tem = tem.reset_index(drop = True)
        if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[0] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[0]:
            finalfence = finalfence.append(tem.iloc[j,:])

# 对光感报警数据进行汇总统计
warning_fence = finalfence.groupby(['车架号','车主'])['围栏名称'].agg(['count','unique']).reset_index()
# 围栏报警数据中与客户是否风险无明显关系，不考虑此报警数据
'''

# 5.风险点报警数据
# 计算每次报警的报警状态
# 如果用户在一段时间内频繁在同一个风险点发生

finalrisk = pd.DataFrame()
for i in car_list:
    tem = risk[risk['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    # tem['时间差'] = None
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            tem['GPS结束时间'] = None
            # tem['时间差'].iloc[j] = tep['最后整合时间'].iloc[k] - pd.to_datetime(tem['date'].iloc[j])
            if pd.to_datetime(tem['报警时间'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['报警时间'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['报警时间'].iloc[j]) + datetime.timedelta(minutes=int(tem['staytime'].iloc[j]))
                finalrisk = finalrisk.append(tem.iloc[j,:])
            elif pd.to_datetime(tem['报警时间'].iloc[j]) < tep['GPS起始时间'].iloc[k] and (pd.to_datetime(tem['报警时间'].iloc[j]) + datetime.timedelta(minutes=int(tem['staytime'].iloc[j]))) >= tep['GPS起始时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['报警时间'].iloc[j]) + datetime.timedelta(minutes=int(tem['staytime'].iloc[j]))
                finalrisk = finalrisk.append(tem.iloc[j,:])
# finalstation['时间差'] = finalstation['时间差'].dt.days
finalrisk['报警时间'] = pd.to_datetime(finalrisk['报警时间'])
finalrisk['时间差'] = None
for i in range(len(finalrisk)):
    if finalrisk['GPS起始时间'].iloc[i] > finalrisk['报警时间'].iloc[i]:
        finalrisk['时间差'].iloc[i] = finalrisk['GPS结束时间'].iloc[i] - finalrisk['GPS起始时间'].iloc[i]
    else:
        finalrisk['时间差'].iloc[i] = finalrisk['GPS结束时间'].iloc[i] - finalrisk['报警时间'].iloc[i]

#最后时间状态修改，如果报警已结束
finalrisk['截至状态'] = None
for i in range(len(finalrisk)):
    if finalrisk['GPS结束时间'].iloc[i] >= finalrisk['GPS起始时间'].iloc[i] + datetime.timedelta(days=15):
        finalrisk['截至状态'].iloc[i] = 1
    else:
        finalrisk['截至状态'].iloc[i] = 0
finalrisk['时间差'] = finalrisk['时间差'].astype(str)
finalrisk['时间差1'] = [(int(x.split(' ')[0])*24 + int(x.split(' ')[2].split(':')[0]) + int(x.split(' ')[2].split(':')[1])/60) for x in list(finalrisk['时间差'])]
finalrisk.loc[finalrisk['时间差1'] >= 15*24,'时间差1'] =15*24
finalrisk.rename(columns={'时间差1':'持续时间修改'},inplace=True) 
finalrisk = finalrisk.drop_duplicates() 

# 对风险点进行汇总统计
warning_risk = finalrisk.groupby(['车架号','GPS起始时间']).agg({'截至状态':'max','持续时间修改':'mean','报警时间':'count','风险点名称':'unique'})
warning_risk.rename(columns = {'截至状态':'风险点截至状态','持续时间修改':'风险点报警平均时间','报警时间':'风险点报警次数'},inplace = True)
warning_risk['风险点个数'] = [len(x) for x in list(warning_risk['风险点名称'])]
warning_risk = warning_risk.drop(['风险点名称'],axis = 1)
notrisk = pd.merge(warning_risk,use,on = ['车架号','GPS起始时间'],how = 'left')

# warning_risk = finalrisk.groupby(['车架号','GPS起始时间']).agg({'date':'count','风险点名称':'unique','持续时间修改':'mean'}).reset_index()

# notrisk = pd.merge(warning_risk,use,on = ['车架号','GPS起始时间'],how = 'left')
notrisk.to_csv('风险点报警初步分析.csv')

'''
risk['date'] = pd.to_datetime(risk['date'])
finalrisk = pd.DataFrame()
for i in car_list:
    tem = risk[risk['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                finalrisk = finalrisk.append(tem.iloc[j,:])
'''

# 6.低电报警和断电报警
remove['date'] = pd.to_datetime(remove['date'])
finalremove = pd.DataFrame()
for i in car_list:
    tem = remove[remove['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                finalremove = finalremove.append(tem.iloc[j,:])
warning_remove = finalremove.groupby(['车架号','GPS起始时间']).agg({'报警次数':'sum','移动次数':'sum'}).reset_index()
warning_remove.rename(columns = {'报警次数':'断电报警次数','移动次数':'断电移动次数'},inplace = True)
notremove = pd.merge(warning_remove,use,on = ['车架号','GPS起始时间'],how = 'left')

notremove.to_csv('断电报警初步分析.csv')
# 对断电报警报警数据进行汇总统计


lowbattery['date'] = pd.to_datetime(lowbattery['date'])
finallowbattery = pd.DataFrame()
for i in car_list:
    tem = lowbattery[lowbattery['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                finallowbattery = finallowbattery.append(tem.iloc[j,:])
                
warning_lowbattery = finallowbattery.groupby(['车架号','GPS起始时间']).agg({'报警次数':'sum','报警位置':'count'}).reset_index()
warning_lowbattery.rename(columns = {'报警次数':'低电总报警次数','报警位置':'低电报警次数（去重后）'},inplace = True)                             
notlowbattery = pd.merge(warning_lowbattery,use,on = ['车架号','GPS起始时间'],how = 'left')
notlowbattery.to_csv('低电报警初步分析.csv')
# 对断电报警报警数据进行汇总统计
# warning_lowbattery = finallowbattery.groupby(['车架号','GPS起始时间'])['staytime'].agg(['count','mean']).reset_index()

# 7.停车超时
finalstaytimeout = pd.DataFrame()
for i in car_list:
    tem = staytimeout[staytimeout['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    # tem['时间差'] = None
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            tem['GPS结束时间'] = None
            # tem['时间差'].iloc[j] = tep['最后整合时间'].iloc[k] - pd.to_datetime(tem['date'].iloc[j])
            if pd.to_datetime(tem['停车时间_x'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['停车时间_x'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['停车时间_x'].iloc[j]) + datetime.timedelta(minutes=int(tem['停车时长'].iloc[j]))
                finalstaytimeout = finalstaytimeout.append(tem.iloc[j,:])
            elif pd.to_datetime(tem['停车时间_x'].iloc[j]) < tep['GPS起始时间'].iloc[k] and (pd.to_datetime(tem['停车时间_x'].iloc[j]) + datetime.timedelta(minutes=int(tem['停车时长'].iloc[j]))) >= tep['GPS起始时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['停车时间_x'].iloc[j]) + datetime.timedelta(minutes=int(tem['停车时长'].iloc[j]))
                finalstaytimeout = finalstaytimeout.append(tem.iloc[j,:])
# finalstation['时间差'] = finalstation['时间差'].dt.days
finalstaytimeout['停车时间_x'] = pd.to_datetime(finalstaytimeout['停车时间_x'])
finalstaytimeout['时间差'] = None
for i in range(len(finalstaytimeout)):
    if finalstaytimeout['GPS起始时间'].iloc[i] > finalstaytimeout['停车时间_x'].iloc[i]:
        finalstaytimeout['时间差'].iloc[i] = finalstaytimeout['GPS结束时间'].iloc[i] - finalstaytimeout['GPS起始时间'].iloc[i]
    else:
        finalstaytimeout['时间差'].iloc[i] = finalstaytimeout['GPS结束时间'].iloc[i] - finalstaytimeout['停车时间_x'].iloc[i]
#最后时间状态修改，如果报警已结束，截至为0，反之为1

finalstaytimeout['截至状态'] = None
for i in range(len(finalstaytimeout)):
    if finalstaytimeout['GPS结束时间'].iloc[i] >= finalstaytimeout['GPS起始时间'].iloc[i] + datetime.timedelta(days=15):
        finalstaytimeout['截至状态'].iloc[i] = 1
    else:
        finalstaytimeout['截至状态'].iloc[i] = 0
        
        
finalstaytimeout['时间差'] = finalstaytimeout['时间差'].astype(str)
finalstaytimeout['时间差1'] = [(int(x.split(' ')[0])*24 + int(x.split(' ')[2].split(':')[0]) + int(x.split(' ')[2].split(':')[1])/60) for x in list(finalstaytimeout['时间差'])]
finalstaytimeout.loc[finalstaytimeout['时间差1'] >= 15*24,'时间差1'] =15*24
finalstaytimeout.rename(columns={'时间差1':'持续时间修改'},inplace=True) 
finalstaytimeout = finalstaytimeout.drop_duplicates() 

warning_staytimeout = finalstaytimeout.groupby(['车架号','GPS起始时间']).agg({'截至状态':'max','持续时间修改':'mean','报警位置':'count'}).reset_index()
warning_staytimeout.rename(columns = {'截至状态':'停车超时截至状态','持续时间修改':'停车超时报警平均时间','报警位置':'停车超时报警次数'},inplace = True)

# warning_staytimeout = finalstaytimeout.groupby(['车架号','GPS起始时间']).agg({'date':'count','风险点名称':'unique','持续天数修改':'mean'}).reset_index()
# warning_risk['风险点个数'] = [len(x) for x in list(warning_risk['风险点名称'])]
notstaytimeout = pd.merge(warning_staytimeout,use,on = ['车架号','GPS起始时间'],how = 'left')


notstaytimeout.to_csv('停车超时初步分析.csv')



# 8.离线超时

finalofflinetimeout = pd.DataFrame()
for i in car_list:
    tem = offlinetimeout[offlinetimeout['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    # tem['时间差'] = None
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            tem['GPS结束时间'] = None
            # tem['时间差'].iloc[j] = tep['最后整合时间'].iloc[k] - pd.to_datetime(tem['date'].iloc[j])
            if pd.to_datetime(tem['离线时间_x'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['离线时间_x'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['离线时间_x'].iloc[j]) + datetime.timedelta(minutes=int(tem['离线时长'].iloc[j]))
                finalofflinetimeout = finalofflinetimeout.append(tem.iloc[j,:])
            elif pd.to_datetime(tem['离线时间_x'].iloc[j]) < tep['GPS起始时间'].iloc[k] and (pd.to_datetime(tem['离线时间_x'].iloc[j]) + datetime.timedelta(minutes=int(tem['离线时长'].iloc[j]))) >= tep['GPS起始时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['离线时间_x'].iloc[j]) + datetime.timedelta(minutes=int(tem['离线时长'].iloc[j]))
                finalofflinetimeout = finalofflinetimeout.append(tem.iloc[j,:])
# finalstation['时间差'] = finalstation['时间差'].dt.days
finalofflinetimeout['离线时间_x'] = pd.to_datetime(finalofflinetimeout['离线时间_x'])
finalofflinetimeout['时间差'] = None
for i in range(len(finalofflinetimeout)):
    if finalofflinetimeout['GPS起始时间'].iloc[i] > finalofflinetimeout['离线时间_x'].iloc[i]:
        finalofflinetimeout['时间差'].iloc[i] = finalofflinetimeout['GPS结束时间'].iloc[i] - finalofflinetimeout['GPS起始时间'].iloc[i]
    else:
        finalofflinetimeout['时间差'].iloc[i] = finalofflinetimeout['GPS结束时间'].iloc[i] - finalofflinetimeout['离线时间_x'].iloc[i]

finalofflinetimeout['截至状态'] = None
for i in range(len(finalofflinetimeout)):
    if finalofflinetimeout['GPS结束时间'].iloc[i] >= finalofflinetimeout['GPS起始时间'].iloc[i] + datetime.timedelta(days=15):
        finalofflinetimeout['截至状态'].iloc[i] = 1
    else:
        finalofflinetimeout['截至状态'].iloc[i] = 0

finalofflinetimeout['时间差'] = finalofflinetimeout['时间差'].astype(str)
finalofflinetimeout['时间差1'] = [(int(x.split(' ')[0])*24 + int(x.split(' ')[2].split(':')[0]) + int(x.split(' ')[2].split(':')[1])/60) for x in list(finalofflinetimeout['时间差'])]
finalofflinetimeout.loc[finalofflinetimeout['时间差1'] >= 15*24,'时间差1'] =15*24
finalofflinetimeout.rename(columns={'时间差1':'持续时间修改'},inplace=True) 
finalofflinetimeout = finalofflinetimeout.drop_duplicates() 

warning_offlinetimeout = finalofflinetimeout.groupby(['车架号','GPS起始时间']).agg({'截至状态':'max','持续时间修改':'mean','报警位置':'count'}).reset_index()
warning_offlinetimeout.rename(columns = {'截至状态':'离线超时截至状态','持续时间修改':'离线超时报警平均时间','报警位置':'离线超时报警次数'},inplace = True)


notofflinetimeout = pd.merge(warning_offlinetimeout,use,on = ['车架号','GPS起始时间'],how = 'left')

# # warning_staytimeout = finalstaytimeout.groupby(['车架号','GPS起始时间']).agg({'date':'count','风险点名称':'unique','持续天数修改':'mean'}).reset_index()
# # warning_risk['风险点个数'] = [len(x) for x in list(warning_risk['风险点名称'])]

warning_offlinetimeout.to_csv('离线超时初步分析.csv')


# 9.常驻地报警
''' '''
finalstation = pd.DataFrame()
for i in car_list:
    tem = station[station['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    # tem['时间差'] = None
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            tem['GPS结束时间'] = None
            # tem['时间差'].iloc[j] = tep['最后整合时间'].iloc[k] - pd.to_datetime(tem['date'].iloc[j])
            if pd.to_datetime(tem['date'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['date'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['date'].iloc[j]) + datetime.timedelta(days=int(tem['异常持续天数'].iloc[j]))
                finalstation = finalstation.append(tem.iloc[j,:])
            elif pd.to_datetime(tem['date'].iloc[j]) < tep['GPS起始时间'].iloc[k] and (pd.to_datetime(tem['date'].iloc[j]) + datetime.timedelta(days=int(tem['异常持续天数'].iloc[j]))) >= tep['GPS起始时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                tem['GPS结束时间'].iloc[j] = pd.to_datetime(tem['date'].iloc[j]) + datetime.timedelta(days=int(tem['异常持续天数'].iloc[j]))
                finalstation = finalstation.append(tem.iloc[j,:])
# finalstation['时间差'] = finalstation['时间差'].dt.daysfinalstation['开始日期_x'] = pd.to_datetime(finalstation['开始日期_x'])
finalstation['开始日期_x'] = pd.to_datetime(finalstation['开始日期_x'])
finalstation['时间差'] = None
for i in range(len(finalstation)):
    if finalstation['GPS起始时间'].iloc[i] > finalstation['开始日期_x'].iloc[i]:
        finalstation['时间差'].iloc[i] = finalstation['GPS结束时间'].iloc[i] - finalstation['GPS起始时间'].iloc[i]
    else:
        finalstation['时间差'].iloc[i] = finalstation['GPS结束时间'].iloc[i] - finalstation['开始日期_x'].iloc[i]

# 常驻地报警状态判定


finalstation['时间差'] = finalstation['时间差'].astype(str)
finalstation['时间差'] = [int(x.split(' ')[0]) for x in list(finalstation['时间差'])]

# deadline = [finalstation['date'] + datetime.timedelta(days = x) for x in list(finalstation['异常持续天数'])]
# finalstation['结束日期'] = finalstation['date'] + pd.Series(deadline)
# finalstation['异常持续天数修改'] = finalstation[['时间差','异常持续天数']].min(axis = 1)
finalstation.loc[finalstation['时间差'] >= 15,'时间差'] =15
finalstation.rename(columns={'时间差':'异常持续天数修改'},inplace=True)  


finalstation = finalstation.drop_duplicates()
# 对区域报警数据进行汇总统计

# 读取常驻地报警中的数据，分为两部分，一部分为5月22号获取数据，一部分为6月15号获取数据（持续）
# 利用数据获取时间来得到常驻地报警的起始时间
ex_station['get_date'] = None
ex_station['get_date'].iloc[:3752] = '2020-05-21' 
ex_station['get_date'].iloc[3752:] = '2020-06-15'
ex_station = ex_station.drop_duplicates()

# 计算开始报警时间，这里分为未回家报警和未上班报警
ex_station['get_date'] = pd.to_datetime(ex_station['get_date'])
# 将重复得报警数据进行删除
# 对于同一车架号，如果存在两条且以上报警记录，且未回家报警相差24天，未上班报警相差16天，则删除5月21那天获取的报警记录
ex_station = ex_station.sort_values(by = ['车架号','get_date'],axis = 0, ascending = False)
ex_car_id = list(set(ex_station['车架号']))
finalstation1 = pd.DataFrame() 
for i in ex_car_id:
    tem = ex_station[ex_station['车架号'] == i]
    tem = tem.reset_index(drop = True)
    if len(tem) == 2 and (tem['连续未上班（工作日）'].iloc[0] - tem['连续未上班（工作日）'].iloc[1] == 16 or tem['连续未回家（天）'].iloc[0] - tem['连续未回家（天）'].iloc[1] == 24):
        tem = tem.drop([1])
    finalstation1 = finalstation1.append(tem)
        
# 获取时间

finalstation1['连续未上班（工作日）'] = finalstation1['连续未上班（工作日）'].astype(int)
finalstation1['连续未回家（天）'] = finalstation1['连续未回家（天）'].astype(int)

home_date = [x-datetime.timedelta(days = y) for x,y in zip(list(finalstation1['get_date']),list(finalstation1['连续未回家（天）']))]
finalstation1['未回家报警开始时间'] = home_date
work_date = [x-datetime.timedelta(days = round(y/5*7,0)) for x,y in zip(list(finalstation1['get_date']),list(finalstation1['连续未上班（工作日）']))]
finalstation1['未上班报警开始时间'] = work_date
# 选取报警时间段内的数据，将未回家报警和未上班报警先分开选取，后合并计算
home = finalstation1.loc[:,['车牌号', '车架号', '车主', '门店','连续未回家（天）','get_date','未回家报警开始时间']]
home['报警类型'] = '未回家'
home.rename(columns = {'连续未回家（天）':'持续报警时间','未回家报警开始时间':'报警时间'},inplace = True)
work = finalstation1.loc[:,['车牌号', '车架号', '车主', '门店','连续未上班（工作日）','get_date','未上班报警开始时间']]
work['报警类型'] = '未上班'
work.rename(columns = {'连续未上班（工作日）':'持续报警时间','未上班报警开始时间':'报警时间'},inplace = True)
work = work.append(home)

finalstation11 = work.copy()
finalstation111 = pd.DataFrame()
for i in car_list:
    tem = finalstation11[finalstation11['车架号'] == i]
    tep = payData[payData['车架号'] == i]
    # tem['时间差'] = None
    for k in range(len(tep)):
        for j in range(len(tem)):
            tem = tem.reset_index(drop = True)
            tem['GPS起始时间'] = None
            # tem['GPS结束时间'] = None
            # tem['时间差'].iloc[j] = tep['最后整合时间'].iloc[k] - pd.to_datetime(tem['date'].iloc[j])
            if pd.to_datetime(tem['报警时间'].iloc[j]) >= tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['报警时间'].iloc[j]) <= tep['最后整合时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                finalstation111 = finalstation111.append(tem.iloc[j,:])
            elif pd.to_datetime(tem['报警时间'].iloc[j]) < tep['GPS起始时间'].iloc[k] and pd.to_datetime(tem['get_date'].iloc[j]) >= tep['GPS起始时间'].iloc[k]:
                tem['GPS起始时间'].iloc[j] = tep['GPS起始时间'].iloc[k]
                finalstation111 = finalstation111.append(tem.iloc[j,:])

# 对实际报警持续时间进行修改
finalstation111['时间差'] = None
for i in range(len(finalstation111)):
    if finalstation111['GPS起始时间'].iloc[i] > finalstation111['报警时间'].iloc[i]:
        finalstation111['时间差'].iloc[i] = finalstation111['get_date'].iloc[i] - finalstation111['GPS起始时间'].iloc[i]
    else:
        finalstation111['时间差'].iloc[i] = finalstation111['get_date'].iloc[i] - finalstation111['报警时间'].iloc[i]
finalstation111['时间差'] = finalstation111['时间差'].astype(str)
finalstation111['时间差'] = [int(x.split(' ')[0]) for x in list(finalstation111['时间差'])]

# deadline = [finalstation['date'] + datetime.timedelta(days = x) for x in list(finalstation['异常持续天数'])]
# finalstation['结束日期'] = finalstation['date'] + pd.Series(deadline)
# finalstation['异常持续天数修改'] = finalstation[['时间差','异常持续天数']].min(axis = 1)
finalstation111.loc[finalstation111['时间差'] >= 15,'时间差'] =15
finalstation111.rename(columns={'时间差':'异常持续天数修改','报警时间':'开始日期_x','持续报警时间':'异常持续天数'},inplace=True) 
finalstation = finalstation.drop(['Unnamed: 0', 'Unnamed: 0.1', 'date', 'hour'],axis = 1)
finalstation111.rename(columns = {'get_date':'GPS结束时间','报警类型':'异常类型'},inplace = True)


# 持续常驻地报警与历史常驻地报警数据进行汇总

finalstation = finalstation.append(finalstation111)


finalstation['截至状态'] = None
for i in range(len(finalstation)):
    if finalstation['GPS结束时间'].iloc[i] >= finalstation['GPS起始时间'].iloc[i] + datetime.timedelta(days=15):
        finalstation['截至状态'].iloc[i] = 1
    else:
        finalstation['截至状态'].iloc[i] = 0
    
        
        
warning_station = finalstation.groupby(['车架号','异常类型','GPS起始时间'])['异常持续天数修改'].agg(['count','sum']).reset_index()
warning_station.rename(columns={'count':'报警次数','sum':'异常持续天数'},inplace=True)

warning_station_home = warning_station[warning_station['异常类型'] == '未回家报警']
warning_station_home.rename(columns={'报警次数':'未回家报警次数','异常持续天数':'未回家异常持续天数'},inplace=True)
warning_station_work = warning_station[warning_station['异常类型'] == '未上班报警']
warning_station_work.rename(columns={'报警次数':'未上班报警次数','异常持续天数':'未上班异常持续天数'},inplace=True)                       
warning_station = pd.merge(warning_station_home, warning_station_work, on = ['车架号','GPS起始时间'], how = 'outer')
warning_station = warning_station.drop(['异常类型_x','异常类型_y'],axis = 1)
notfinalstation = pd.merge(warning_station,use,on = ['车架号','GPS起始时间'],how = 'left')       

notfinalstation.to_csv('常驻地报警初步分析.csv')


warning_gather = [warning_area,warning_isWireless,warning_remove,warning_risk,warning_station,warning_staytimeout,
                  warning_offlinetimeout,warning_lowbattery]
modelData = pd.merge(payData,financialBigData,on = '身份证号码')
for tep in warning_gather:
    modelData = pd.merge(modelData,tep,on=['车架号','GPS起始时间'],how = 'left')
# modelData = modelData.fillna(0)
modelData.to_csv('全部数据汇总.csv')

# 处理一版数据用于分析，即将所有得缺失值全部填补为0
ana = modelData.copy()
ana.iloc[:,23:] = ana.iloc[:,23:].fillna(0)
ana.to_csv('用于分析的全部数据汇总.csv')