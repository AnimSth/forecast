import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
import warnings

warnings.filterwarnings('ignore')



file_name = 'kalimati0311.xlsx' 
df = pd.read_excel(file_name, index_col=0)
df_value = df[['Commodity']]
df_values = df_value.value_counts()
df_values = pd.DataFrame(df_values)
df_values.columns =['Commodity']
df_values.drop('Commodity', axis=1, inplace=True)
df_values.reset_index(level=0, inplace=True)
datas= df_value.values
dat=[]
dat = pd.DataFrame(dat, columns=['Date',"Forecast(MIN)","Forecast(AVG)","Forecast(MAX)",'Commodity'])



def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele    
    return str1 


for data in datas:
    res = listToString(data)
    file_name = 'kalimati0311.xlsx' 
    df = pd.read_excel(file_name, index_col=0)
    df = pd.DataFrame(df)
    tom= (df['Commodity'] == res)
    df_to = df[tom]
    val = len(df_to)
    ta= 1
    sta = val-ta
    df_to.index = pd.to_datetime(df_to['Date'], format='%Y.%m.%d')
    
    df_to['Minimum'] = df_to['Minimum'].str.replace('Rs. ', '')
    df_min=df_to[['Minimum']]
    df_min= df_min.astype(float)
    df_train= df_min[0:sta]
    df_tester= df_min[sta:val]
   
    df_to['Maximum'] = df_to['Maximum'].str.replace('Rs. ', '')
    df_max = df_to[['Maximum']]
    df_max= df_max.astype(float)
    df_train1= df_max[0:sta]
    df_tester1= df_max[sta:val]

    df_avg = df_to[['Average']]
    df_avg= df_avg.astype(float)
    df_train2= df_avg[0:sta]
    df_tester2= df_avg[sta:val]


#MINIMUM_FORECAST
    df_model= sm.tsa.ARIMA(df_train, order=(4,1,2),trend ='t')
    df_model_fit= df_model.fit()
    df_fore=df_model_fit.forecast(steps=7)
    df_fore = pd.DataFrame(df_fore)
    df_fore.reset_index(drop=True, inplace=True)
    df_tester.reset_index(drop=True, inplace=True)
    
#AVERAGE_FORECAST
    df_model2= sm.tsa.ARIMA(df_train2, order=(4,1,2),trend ='t')
    df_model_fit2= df_model2.fit()
    df_fore2=df_model_fit2.forecast(steps=7)
    df_fore2 = pd.DataFrame(df_fore2)
    df_fore2.reset_index(drop=True, inplace=True)
    df_tester2.reset_index(drop=True, inplace=True)

    
#MAXIMUM_FORECAST
    df_model1= sm.tsa.ARIMA(df_train1, order=(4,1,2),trend ='t')
    df_model_fit1= df_model1.fit()
    df_fore1=df_model_fit1.forecast(steps=7)
    df_fore1 = pd.DataFrame(df_fore1)
    df_fore1.reset_index(drop=True, inplace=True)
    df_tester1.reset_index(drop=True, inplace=True)


    df_forecast = pd.date_range(start='2022-03-11', periods=len(df_fore), freq='D')
    df_forecast = pd.DataFrame(df_forecast)
    df_forecast.columns=['Date']
    
    df_forecast = df_forecast.join(df_fore['predicted_mean'])
    df_forecast.columns=['Date',"Forecast(MIN)"]


    df_forecast = df_forecast.join(df_fore2['predicted_mean'])
    df_forecast.columns=['Date',"Forecast(MIN)","Forecast(AVG)"]


    df_forecast = df_forecast.join(df_fore1['predicted_mean'])
    df_forecast.columns=['Date',"Forecast(MIN)","Forecast(AVG)","Forecast(MAX)"]
  


    df_forecast['Commodity'] = res
    df_forecast['Forecast(MIN)'] = df_forecast['Forecast(MIN)'].round()
    df_forecast['Forecast(AVG)'] = df_forecast['Forecast(AVG)'].round()
    df_forecast['Forecast(MAX)'] = df_forecast['Forecast(MAX)'].round()
    print(df_forecast)

#To append the forecasted data and save it into csv file.
    # dat = dat.append([df_forecast],ignore_index=False, verify_integrity=False, sort=None)
# dat.to_('df.csv')


