import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pyecharts.charts import *
from pyecharts.components import Table
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import random
import datetime
from pyecharts.globals import CurrentConfig
from streamlit_echarts import st_pyecharts
import time
CurrentConfig.ONLINE_HOST = "https://cdn.kesci.com/lib/pyecharts_assets/"
from streamlit_echarts import st_pyecharts
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False 

def draw():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df_China_by_year.plot(kind='line', x='year', y='AverageTemperature', ax=ax, title='中国1821-2012年年均气温')
    ax.set_ylabel('AverageTemperature(℃)')
    xx = list(range(df_China_by_year.shape[0]))
    coefficients = np.polyfit(xx, 
                              df_China_by_year['AverageTemperature'].to_list(),
                              1)
    polynomial = np.poly1d(coefficients)
    y_fit = polynomial(xx)
    ax.plot(xx, y_fit, color='red', linewidth=2, label='Trend Line')
    plt.legend()
    st.pyplot(fig)
    yy =  df_China_by_year['AverageTemperature'].to_list()
    mse = mean_squared_error(yy, y_fit)
    st.write("Trend Line斜率:{:}".format(coefficients[0]))
    st.write("均方误差(MSE):{:.5f}".format(mse))
    st.write("均方根误差(RMSE):{:.5f}".format(mse**(1/2)))
    
    
    
    

st.title("对中国的年均气温进行预测")

st.subheader("数据集", divider='rainbow')
st.write("数据集为中国1821-2012年的年均气温数据。在部分时间段有缺失值，采取使用前一个非缺失值填充的方法，下为填充之后的数据。")
df_China = pd.read_csv('China.csv')
df_China_by_year = df_China.groupby('year')['AverageTemperature'].mean().reset_index()
df_China_by_year['AverageTemperature'] = df_China_by_year['AverageTemperature'].fillna(method='ffill')
df_China_by_year['year'] = df_China_by_year['year'].astype(str)
st.dataframe(df_China_by_year, use_container_width=True)

st.subheader("数据集可视化与回归预测", divider='rainbow')
draw()


st.subheader("分析", divider='rainbow')
st.markdown('''
            - 中国1821-2012年的年均气温整体上来看呈上升趋势
            - 1970年以后，年均气温增长明显加快
            ''')
