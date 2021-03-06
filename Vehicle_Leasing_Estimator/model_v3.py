# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:58:10 2020

@author: hw
"""

'''
运用boosting算法中的gbdt算法进行识别分类
'''

import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve, auc
from scipy import interp
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")


alldata = pd.read_csv('C:/Users/hw/Desktop/model_v1/全部数据汇总.csv',index_col=0)
alldata.iloc[:,23:] = alldata.iloc[:,23:].fillna(0)

alldata = alldata.sort_values(by = ['最后整合时间'],axis = 0, ascending = False)
alldata = alldata.drop_duplicates(subset = ['身份证号码'],keep = 'last')

alldata_copy = alldata.copy()


# alldata = alldata.reindex(np.random.permutation(alldata.index))
# alldata = alldata.drop_duplicates(subset = ['身份证号码'])
alldata.index = alldata['身份证号码']
alldata = alldata.drop(['最后整合时间','GPS起始时间','dataSource','车架号','身份证号码'],axis = 1)

# 计算数据之间的相关性（这里使用皮尔森相关系数进行衡量）
df = alldata.corr()
# 分析字段缺失情况，对缺失数据进行补齐
# 在所有字段中，贷款总额、手机消费水平、手机号-身份证号是否一致、入网时长存在缺失值
# 其中贷款总额的缺失值最少，缺失比例为1.95%，利用平均值对贷款总额进行填补
missing = alldata.isnull().sum().reset_index().rename(columns={0:'missNum'})
missing['缺失比例'] = missing['missNum']/len(alldata)
# costLevel字段缺失值数量为396，缺失率为43%，故暂时将这一字段进行删除
alldata = alldata.drop(['costLevel'], axis = 1)
alldata['贷款总额'] = alldata['贷款总额'].fillna(alldata['贷款总额'].mean())
# isSame、netTime字段缺失值利用众数进行补齐
'''后期可以利用年龄、性别、工作年限等客户基本信息字段对客户进行简单聚类，然后利用同类别中
字段的众数对缺失值进行补齐'''
alldata['isSame'] = alldata['isSame'].fillna(alldata['isSame'].mode()[0])
alldata['netTime'] = alldata['netTime'].fillna(alldata['netTime'].mode()[0])

# 分组进行描述统计
des = alldata.groupby(['flag']).describe()


# 从描述性统计以及相关性分析中，duringdays与客户的风向类型（flag)有较强的相关性
# 对于正常客户来说，由于后期万位GPS系统不再继续使用，故获得的正常客户的数据的duringdays的值都较大
# 针对这一问题，可采用的解决方案有三种，具体见分析文档

to_flag = alldata['flag'].copy()
# to_flag.set_index(['身份证号码'],inplace = True)
# 将类别压缩为两类，即将骗贷、二押和退车/收车合并
alldata.loc[alldata['flag'] == 1,'flag'] = 0
alldata.loc[alldata['flag'] == 2,'flag'] = 1
# 对字符型变量，如issame等进行独热编码，将其数值化
from sklearn.preprocessing import LabelEncoder
Le = LabelEncoder()
alldata['isSame'] = Le.fit_transform(alldata['isSame'])
alldata['netTime'] = Le.fit_transform(alldata['netTime'])



# 特征工程：贷款总额、首付金额、提车时间（duringdays）---数据分桶、WOE分析
# 在二分类中，可以将数据分箱和woe分析结合使用
# 1.数据分箱
# 2.woe变换（注：woe变换の相关概念）
alldata = alldata.rename(columns = {'flag':'target'})
# data_woe = alldata.copy()
import woe.feature_process as fp
import woe.eval as eval
civ_list = []
# woe_index = ['贷款总额','首付金额','duringDay']

woe_index = ['贷款总额','首付金额','duringDay','停车超时报警平均时间','离线超时报警平均时间','风险点报警平均时间']
# 如果将分箱放入到交叉验证流程中，结果如何?
n_positive = sum(alldata['target'])
n_negtive = len(alldata) - n_positive
for i in woe_index: 
    if alldata[i].dtypes == 'object':
        civ = fp.proc_woe_discrete(alldata, i, n_positive, n_negtive, 0.05*len(alldata),alpha=0.05)
    else:            
        civ = fp.proc_woe_continuous(alldata, i, n_positive, n_negtive, 0.05*len(alldata), alpha=0.05)
    civ_list.append(civ)
    alldata[i] = fp.woe_trans(alldata[i], civ)
    civ_df = eval.eval_feature_detail(civ_list)
    iv_thre = 0.001
    iv = civ_df[['var_name','iv']].drop_duplicates() # 计算特征的iv值，查看特征的重要性
    
'''

# 3.组合特征
# 根据风控部门提供的风险判断规则，构建报警数据的组合特征
# 思路：在15天内，是否出现多种报警记录
# 1.是否在一段时间内同时发生了低电、断电、离线报警，增加新字段 combineWarn1
alldata['combineWarn1'] = None
for k in range(len(alldata)):
    if alldata['低电总报警次数'][k] != 0 and alldata['断电报警次数'][k] != 0 and alldata['离线超时报警次数'][k] != 0:
        alldata['combineWarn1'][k] = 1
    else:
        alldata['combineWarn1'][k] = 0

# 2.是否在一段时间内同时发生了风险点报警、光感报警、停车超时报警
alldata['combineWarn2'] = None
for k in range(len(alldata)):
    if alldata['风险点报警次数'][k] != 0 and alldata['停车超时报警次数'][k] != 0 and alldata['光感报警报警次数'][k] != 0:
        alldata['combineWarn2'][k] = 1
    else:
        alldata['combineWarn2'][k] = 0        
        
# 3.是否在一段时间内同时发生了风险点报警、区域报警、光感报警
alldata['combineWarn3'] = None
for k in range(len(alldata)):
    if (alldata['入区域报警次数'][k] != 0 or alldata['出区域报警次数'][k] != 0)  and alldata['风险点报警次数'][k] != 0 and alldata['光感报警报警次数'][k] != 0:
        alldata['combineWarn3'][k] = 1
    else:
        alldata['combineWarn3'][k] = 0          
'''

# 4.特征选取
# 查看所有特征中是否有一个值的个数占比超过90%
tmp_list = []
not_col = []
for x in alldata.drop(['target'],axis=1).columns:
    if alldata[x].value_counts(normalize=True).iloc[0] >= 0.9:
        tmp_list.append((x, alldata[x].value_counts(normalize=True).iloc[0]))
        not_col.append(x)
print(not_col)
alldata = alldata.drop(not_col,axis = 1)

# 对数据进行主成分分析或者删除部分相关特征

# alldata = alldata.drop(['实际未还期数','逾期次数','首付比列','duringDay','实际应还期数'],axis = 1)




# 切分数据与标签
xdata = alldata.drop(['target'],axis = 1)
ydata = alldata['target']



from sklearn.model_selection import StratifiedKFold
# from sklearn.preprocessing import MinMaxScaler


hcomp = pd.DataFrame()


sfolder = StratifiedKFold(n_splits=3,random_state=10,shuffle = True)
# 选择2折交叉验证，一半一半划分训练集和测试集
# 将训练集打乱，然后对模型进行训练
from sklearn.ensemble import GradientBoostingClassifier
from imblearn.over_sampling import BorderlineSMOTE
# from sklearn.model_selection import GridSearchCV
gbdt = GradientBoostingClassifier(subsample = 0.8,learning_rate=0.1,n_estimators=100,max_depth = 8,
                                  min_samples_leaf = 5)
smo = BorderlineSMOTE(k_neighbors = 10)

score = []
hcomp = pd.DataFrame()
tprs = []
aucs = []
mean_fpr = np.linspace(0, 1, 100)
kss = []
i = 0



# param = {'n_estimators':range(10,100,10),'learning_rate':[0.01,0.1,0.2,0.5,0.8,0.9],'max_depth':range(2,10,1)}
# # gv = GridSearchCV(estimator = GradientBoostingClassifier(subsample = 0.8), param_grid = param, scoring='roc_auc',iid=False,cv=2)
# for train_index,test_index in sfolder.split(xdata,ydata):
#     train_data = xdata.iloc[train_index,:]
#     train_label = ydata[train_index]
#     test_data = xdata.iloc[test_index,:]
#     test_label = ydata[test_index]
#     x_smo,y_smo = smo.fit_sample(train_data, train_label)
#     gv = GridSearchCV(estimator = GradientBoostingClassifier(subsample = 0.8), param_grid = param, scoring='roc_auc',iid=False,cv=5)
#     gv.fit(x_smo,y_smo)
#     print(gv.best_score_,gv.best_params_)
#     ypre = pd.Series(gv.predict(test_data), name= 'ypre',index = test_data.index)
#     prob = pd.DataFrame(gv.predict_proba(test_data),index = test_data.index)
#     comp = pd.DataFrame([test_label,ypre]).T
#     comp.index = test_label.index
#     comp = pd.merge(comp,prob,on= '身份证号码')
#     comp = pd.merge(comp,to_flag, on = '身份证号码')
#     hcomp = hcomp.append(comp)
#     fpr,tpr,threshold = roc_curve(test_label, ypre)
#     tprs.append(interp(mean_fpr, fpr, tpr))
#     roc_auc = auc(fpr,tpr)
#     aucs.append(roc_auc)
#     ks = max(tpr-fpr)
#     kss.append(ks)
#     plt.plot(fpr, tpr, lw=1, alpha=0.3,label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
#     i += 1
# plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operating characteristic example')
# plt.legend(loc="lower right")
# plt.show()

# f0 = hcomp[hcomp['target'] == 0]
# f1 = hcomp[hcomp['target'] == 1]
# # f2 = hcomp[hcomp['target'] == 2
# # print('平均识别正确率为：' + str(np.mean(score)))
# print('风险客户识别正确率为：' + str(len(f0[f0['ypre'] == 0])/len(f0)))   
# print('正常客户识别正确率为：' + str(len(f1[f1['ypre'] == 1])/len(f1)))
# print('识别正确的样本数为：' + str(len(f0[f0['ypre'] == 0]) + len(f1[f1['ypre'] == 1])))
# # print('正常客户识别正确率为：' + str(len(f2[f2['ypre'] == 2])/len(f2)))
# print('平均AUC为：' + str(np.mean(aucs)))
# print('平均KS指标为：' + str(np.mean(kss)))

 
# print(gv.best_estimator_,gv.best_score_,gv.best_params_)
# y_pred = gv.predict(X)
# y_predprob = gbm2.predict_proba(X)[:,1]
# print("Accuracy : %.4g" % metrics.accuracy_score(y.values, y_pred))
# print("AUC Score (Train): %f" % metrics.roc_auc_score(y, y_predprob))



imf = pd.DataFrame()

for train_index,test_index in sfolder.split(xdata,ydata):
    train_data = xdata.iloc[train_index,:]
    train_label = ydata[train_index]
    test_data = xdata.iloc[test_index,:]
    test_label = ydata[test_index]
    x_smo,y_smo = smo.fit_sample(train_data, train_label)
    # gbdt.fit(pca.fit_transform(x_smo),y_smo)
    gbdt.fit(x_smo,y_smo)
    # gbdt.fit(train_data,train_label)
    # score.append(gbdt.score(pca.transform(test_data),test_label))
    score.append(gbdt.score(test_data,test_label))
    ypre = pd.Series(gbdt.predict(test_data), name= 'ypre')
    # ypre = pd.Series(gbdt.predict(pca.transform(test_data)), name= 'ypre')
    prob = pd.DataFrame(gbdt.predict_proba(test_data),index = test_data.index)
    test_label = test_label.reset_index(drop = True)
    comp = pd.DataFrame([test_label,ypre]).T
    comp.index = test_data.index
    comp = pd.merge(comp,prob,on= '身份证号码')
    hcomp = hcomp.append(comp)
    imf = pd.concat([imf,pd.DataFrame(gbdt.feature_importances_).T])
    fpr,tpr,threshold = roc_curve(test_label, ypre)
    tprs.append(interp(mean_fpr, fpr, tpr))
    roc_auc = auc(fpr,tpr)
    aucs.append(roc_auc)
    ks = max(tpr-fpr)
    kss.append(ks)
    plt.plot(fpr, tpr, lw=1, alpha=0.3,label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
    i += 1
# import graphviz
# with open('credit.dot','rb') as f:
#     dot_graph = f.read()
# dot=graphviz.Source(dot_graph)
# dot.view()

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
plt.legend(loc="lower right")
plt.show()    
    

hcomp = pd.merge(hcomp,to_flag, on = '身份证号码')
hcomp.reset_index(inplace = True)

errorId = list(hcomp[(hcomp['target'] == 0) & (hcomp['ypre'] == 1)]['身份证号码'])

errordata = alldata_copy[alldata_copy['身份证号码'].isin(errorId)]

    
imf = imf.T
imf.index = train_data.columns
# 分类别计算正确率
f0 = hcomp[hcomp['target'] == 0]
f1 = hcomp[hcomp['target'] == 1]
# f2 = hcomp[hcomp['target'] == 2
print('平均识别正确率为：' + str(np.mean(score)))
print('风险客户识别正确率为：' + str(len(f0[f0['ypre'] == 0])/len(f0)))   
print('正常客户识别正确率为：' + str(len(f1[f1['ypre'] == 1])/len(f1)))
print('识别正确的样本数为：' + str(len(f0[f0['ypre'] == 0]) + len(f1[f1['ypre'] == 1])))
# print('正常客户识别正确率为：' + str(len(f2[f2['ypre'] == 2])/len(f2)))
print('平均AUC为：' + str(np.mean(aucs)))
print('平均KS指标为：' + str(np.mean(kss)))

# =============================================================================
# 模型评估，利用正确率，roc曲线以及Ks指标对模型进行评估
# =============================================================================
# 1.二分类模型评估（风险类型为 有风险 无风险）
# 2.多分类模型评估（风险类型为 骗贷/二押 退车/收车（逾期） 正常）

# 

# hcomp.to_csv('识别结果.csv')
# errordata.to_csv('风险客户错误识别结果.csv')
# imf.to_csv('特征重要度.csv')
