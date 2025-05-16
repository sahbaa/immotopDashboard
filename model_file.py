import pandas as pd
import numpy as np 
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
from sklearn.model_selection import train_test_split
import re
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import IsolationForest
import plotly.express as px
from plotly.subplots import make_subplots
from scorecardbundle.feature_discretization import ChiMerge as cm 
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.preprocessing import PowerTransformer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import accuracy_score,mean_absolute_percentage_error,make_scorer
# read dataset:
df = pd.read_csv('rent_changed.csv')

# define input and output :
inputs = df.iloc[:,:-1]
outputs = df.iloc[:,-1]

#define cat Col and count col : 
cat_col = ['Type','Floor','Lift','Furnished','Terrace','Garage','place', 'city']
count_col = [i for i in df.columns if i not in cat_col]


df_links = df.copy(deep=True).drop(['title','Type',	'Contract',	'Floor','Lift','Surface','Rooms','Bed',	'Bath',	'Furnished','Terrace','Garage','price'],axis=1).set_index('index')


def updateCol(tr) :
    cat = [i for i in cat_col if i  in tr.columns]
    cont = [i for i in count_col if i  in tr.columns]
    return cat,cont

# taghire label gozari:
def first_labeling (inp,outp):
    outp = outp.str.findall(r'\d+').apply(lambda x: ''.join(x[:2]))
    inp['Surface'] =inp['Surface'].str.findall(r'\d+').apply(lambda x : ''.join(x))
    inp['Garage'] = inp['Garage'].str.findall(r'\d+')
    inp['Garage'] = inp['Garage'].apply(lambda x: np.sum(list(map(int, x))) if isinstance(x, list) else 0)
    inp['Terrace'] = inp['Terrace'].apply(lambda x : '1' if x=='Yes' else '0')
    inp['Furnished'] = inp['Furnished'].apply(lambda x :'1' if x== 'Yes' else '0')
    inp['Lift'] = inp['Lift'].apply(lambda x :'1' if x== 'Yes' else '0')
    inp['Bed'] = inp['Bed'].apply(lambda x : int(x) if pd.notna(x) and str(x).isdigit() else 0)
    inp['Bath'] = inp['Bath'].apply(lambda x : int(x) if pd.notna(x) and str(x).isdigit() else 0)
    inp['Rooms'] = inp['Rooms'].apply(lambda x :int(x) if pd.notna(x) and str(x).isdigit() else 0)
    inp['Surface'] = inp['Surface'].apply(lambda x :int(x) if pd.notna(x) and str(x).isdigit() else 0)
    outp = outp.apply(lambda x :int(x) if pd.notna(x) and str(x).isdigit() else 0)
    inp['Floor'] = inp['Floor'].replace('Ground floor','0')
    inp = inp.set_index('index')
    inp['Type'] = inp['Type'].replace({'Apartment | Full ownership':'Apartment',
                                       'Apartment | Timeshare':'Apartment','Loft':'detached house',
                                       'Multi-family detached house':'detached house','Single-family detached house':'detached house'
                                       })
    
    inp['Floor'] = inp['Floor'].replace({'4':'more','5':'more','6':'more','7':'more'})
    inp ['place'] = inp['title'].apply(lambda x : x.split(',')[-2] if len(x.split(','))>2 else x.split(',')[-1])
    inp ['city'] = inp['title'].apply(lambda x : x.split(',')[-1] if len(x.split(','))>2 else 'Luxembourg' )
    inp.drop(['title','Contract','link'],axis=1,inplace = True)
    
    return inp,outp
inputs,outputs = first_labeling(inputs,outputs)

cat_col,count_col = updateCol(inputs)
print(count_col)
# cv for continues 
def cv_calc(tr):
    cv_result = tr[count_col].apply(lambda x : np.std(x)/np.mean(x) if np.mean(x) != 0 else 100)
    omitedlist = cv_result[cv_result<0.1].index
    print(omitedlist)
    tr =  tr.drop(omitedlist,axis=1)
    return tr

inputs = cv_calc(inputs)
#much diversity and min diversity: 
def diversity_calc(tr) : 
    high_diversity = tr[cat_col].apply(lambda x : x.value_counts().max()/len(x))
    low_diversity = tr[cat_col].apply(lambda x :x.nunique()/len(x))
    omited_list = set(high_diversity[high_diversity>0.9].index.to_list() + low_diversity[low_diversity >0.95].index.to_list())
    tr = tr.drop(omited_list,axis =1)
    return tr


inputs = diversity_calc(inputs)
cat_col,count_col = updateCol(inputs)
print(cat_col)
# maghadire khrej az baze manteghi va nasazegar  ba frequency tbl:
def freq_tbl(tr) : 
    l =[]
    for i in cat_col:
        val,cnt = np.unique(tr[i], return_counts=True)
        df_res = pd.DataFrame({'values':val, 'count':cnt})
        print(df_res)
    
# print(freq_tbl(inputs))
cat_col,count_col = updateCol(inputs)
# outlier:
def out_detector(tr):
    #impute nans : 
    tr_copy = tr.copy()
    for i in cat_col:
        cat_imp = SimpleImputer(strategy='most_frequent')
        cat_imp.fit_transform(tr_copy[[i]])
    for i in count_col : 
        cont_imp = SimpleImputer(strategy='median')
        cont_imp.fit_transform(tr_copy[[i]])
    
    ohe = OneHotEncoder(sparse_output=False,handle_unknown='ignore')
    arr_encoded = ohe.fit_transform(tr_copy[cat_col])
    encoded_df = pd.DataFrame(arr_encoded,columns=ohe.get_feature_names_out())
    scaler = MinMaxScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(tr[count_col]),columns=count_col)

    result = pd.concat([encoded_df,scaled_data],axis=1)

    model = IsolationForest()
    model.fit(result)
    result['outs']=model.predict(result)
    l = result[result['outs']==-1].index
    tr = tr.drop(l,axis=0)
    return tr

inputs = out_detector(inputs)
# print(inputs.isnull().sum()!=0)

# missing:add te
def missing_handler ( tr):
    # survay on each field :
    nan_each_col = tr[cat_col].apply(lambda x : x.isnull().sum()/len(x))
    field_for_ommiting = nan_each_col[nan_each_col>0.5].index
    tr.drop(field_for_ommiting,axis=1)

    nan_each_row = tr[tr.columns].apply(lambda x: x.isnull().sum()/len(x),axis=1)
    field_for_ommiting = nan_each_row[nan_each_row>0.5].index
    tr = tr.drop(field_for_ommiting,axis=1)
    return tr

inputs = missing_handler(inputs)

# discritization:add te
def discritization(tr):
    bins = KBinsDiscretizer(n_bins=8,strategy='kmeans',encode='ordinal')
    tr['Surface'] = bins.fit_transform(tr[['Surface']])
    print(bins.bin_edges_)
    tr['Surface'] = tr['Surface'].astype(int)
    tr['Surface'] = tr['Surface'].replace({0:'0-42',1:'42-75',2:'76-116',3:'116-167',4:'167-215',5:'>215',6:'>215',7:'>215'})
    return tr

inputs = discritization(inputs)

# store preprocessed data for dashboard :
stored_dataFrame = pd.concat((inputs,outputs),axis=1)
stored_dataFrame.to_csv('preprocessed_df.csv')
# transform : ad te

def encoding(tr):
    list_of_encoded =['Type', 'Floor', 'Lift', 'Furnished', 'Terrace', 'Garage']
    ohe = OneHotEncoder(handle_unknown='ignore',sparse_output=False)
    result = pd.DataFrame(ohe.fit_transform(tr[list_of_encoded]),columns=ohe.get_feature_names_out())
    return result


# # f_extraction:
# # f_selection :

inputs = inputs.drop(['place', 'city'],axis=1)
inputs = encoding(inputs)
print(inputs.head())

# modeling
def scoring(y_true,y_pred):
    return mean_absolute_percentage_error(y_true,y_pred)
evaluation_metric = make_scorer(scoring)
base_model = DecisionTreeRegressor(random_state=42)
param  = {'criterion':['squared_error','absolute_error','friedman_mse'], 'max_depth':[2,3,4,5],'min_samples_split':[10,20,30]}
best_model = GridSearchCV(base_model,param_grid=param,scoring=evaluation_metric,cv=10)
detected_model = best_model.fit(inputs,outputs)
y_pred = detected_model.predict(inputs)
print(mean_absolute_percentage_error(outputs,y_pred))
temp_value = inputs.iloc[6,:].values.reshape(1,-1)
print(detected_model.predict(temp_value))