import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error


file_name = 'kalimati0311.xlsx' 
df = pd.read_excel(file_name, index_col=0)
df = pd.DataFrame(df)

#taking one particular product
tom= (df['Commodity'] == 'Tomato Big(Nepali)')
df_to = df[tom]
val = len(df_to)
ta= 10
sta = val-ta
df_to.index = pd.to_datetime(df_to['Date'], format='%Y.%m.%d')
    
df_to['Maximum'] = df_to['Maximum'].str.replace('Rs. ', '')
df_max = df_to[['Maximum']]
df_max= df_max.astype(float)
df_train1= df_max[0:sta]
df_tester1 = df_max[sta:val]


import itertools
import statsmodels.api as sm

#change the range for more possibilities for better accuracy
p=d=q=range(0,5)
pdq = list(itertools.product(p,d,q))
pdq

Z=[]

import warnings
warnings.filterwarnings('ignore')


# lower ac_error = more accuracy
for param in pdq:
    try:
        model_arima = sm.tsa.ARIMA(df_train1,order=param, trend='t')
        model_arima_fit = model_arima.fit()
        df_fore=model_arima_fit.forecast(steps=10)
        df_fore = pd.DataFrame(df_fore)
        ac_error = np.sqrt(mean_squared_error(df_tester1,df_fore))
        
        print(ac_error, param)
        Z.append(ac_error + param)
    except:
        continue
print(Z)
#then pick the param with lowest acc_error then add it to your ARIMA training mode
