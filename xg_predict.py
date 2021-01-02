import xgboost as xgb
import pandas as pd
from sklearn.model_selection import train_test_split

data = pd.DataFrame()
for i in range(0,29):
    rpath = "train_data\\train_data_p"+str(i)+".csv"
    print("[TRAIN] Reading:",rpath)
    d0 = pd.read_csv(rpath)
    data = pd.concat([data,d0])

test = pd.read_csv('train_data\\train_data_p29.csv')

buy = data.groupby('buy')
ybuy = buy.get_group(1)
nbuy = buy.get_group(0).head(115000)

train_new = pd.concat([ybuy,nbuy])

x_train = train_new[['sales','duration','items','clicks']]
y_train = train_new['buy']
x_test = test[['sales','duration','items','clicks']]
y_test = test['buy']

print("Trainning data size:",x_train.shape)
print("Testing data size:",x_test.shape)

xgbc = xgb.XGBClassifier(
 learning_rate =0.1,
 n_estimators=1000,
 max_depth=9,
 min_child_weight=1,
 gamma=0,
 subsample=0.8,
 colsample_bytree=0.8,
 objective= 'binary:logistic',
 scale_pos_weight=1,
 seed=27,
 tree_method='gpu_hist')
xgbc.fit(x_train, y_train)
print("Accuracy:",xgbc.score(x_test,y_test))
y_pred = pd.DataFrame(data = xgbc.predict_proba(x_test),columns=['prob1','prob2'])
print(y_pred.head())
