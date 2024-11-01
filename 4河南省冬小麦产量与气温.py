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

def draw2():
    df['year'] = df['year'].astype(int)
    temp = df.loc[(df['year']>=begin_year) & (df['year']<=end_year)]
    temp['趋势产量'] = temp['Product'].rolling(window=3, center=True, min_periods=1).mean()
    temp['气候产量'] = temp['Product'] - temp['趋势产量']
    fig = plt.figure()
    ax = fig.add_subplot(111)
    temp['year'] = temp['year'].astype(str)
    temp.plot(x='year', y=['Product', '趋势产量', '气候产量'], ax=ax, kind='line',
              color=['#a62927', '#397995', '#E16593'],
              legend=True,
              title='{:}-{:}年河南冬小麦实际产量、趋势产量、气候产量'.format(begin_year, end_year),
              label=['实际产量', '趋势产量', '气候产量'])
    ax.set_ylabel('产量(万吨)')
    st.pyplot(fig)
    return temp

def sigma(temp):
    temp['sigma'] = temp['气候产量']/temp['趋势产量']
    st.dataframe(temp,use_container_width=True)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    temp.plot(x='AverageTemperature', y='sigma', ax=ax, kind='scatter', color='#a62927',
              title='{:}-{:}年气候影响因子σ与气温关系'.format(begin_year, end_year))
    y = temp['sigma'].values.tolist()
    x = temp['AverageTemperature'].values.tolist()
    a, b, c = np.polyfit(x, y, 2)
    x_fit = np.linspace(min(x), max(x), 100)
    y_fit = a * x_fit**2 + b * x_fit + c
    ax.plot(x_fit, y_fit)
    st.pyplot(fig)
    return {'a':a, 'b':b, 'c':c}

st.title("河南省冬小麦产量与春季气温分析")

st.subheader("数据集", divider='rainbow')
df = pd.read_csv('1950-2013河南省春季（3-6月）均温与小麦产量的关系.csv')
df = df.iloc[:, 1:]
df['year'] = df['year'].astype(str)
st.dataframe(df, use_container_width=True)
words = '''
数据集覆盖1950-2013年3-6月平均气温（℃）与冬小麦年产量（万吨）数据。3-6月正值河南冬小麦生长、成熟季节，
故选择3-6月平均气温分析气温对冬小麦产量的影响。\n
气温数据来源：https://www.heywhale.com/mw/dataset/58d1252b97c4b112cbb82b98/content
\n
冬小麦产量数据来源：国家统计局https://data.stats.gov.cn/easyquery.htm?cn=E0103
'''
st.write(words)


st.subheader("数据集可视化", divider='rainbow')
fig = plt.figure()
ax = fig.add_subplot(111)
df.plot(x='year', y='AverageTemperature', ax=ax, label='3-6月平均气温')
ax.set_ylabel('3-6月平均气温(℃)')
ax2 = ax.twinx()
df.plot(x='year', y='Product', ax=ax2, color='purple', label='小麦产量')
ax2.set_ylabel('冬小麦产量(万吨)')
xx = list(range(2014-1950))
yy = df['AverageTemperature'].values.tolist()
coef = np.polyfit(xx, yy, 1)
func = np.poly1d(coef)
y_fit = func(xx)
ax.plot(xx, y_fit, 'r--', label='3-6月平均气温拟合直线')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
st.pyplot(fig)
mse = mean_squared_error(yy, y_fit)
st.write("Trend Line斜率:{:}".format(coef[0]))
st.write("均方误差(MSE):{:.5f}".format(mse))
st.write("均方根误差(RMSE):{:.5f}".format(mse**(1/2)))

begin_year = 1960
end_year = 1980
st.subheader("以{:}-{:}为基准，计算趋势产量、气候产量".format(begin_year, end_year), divider='rainbow')
st.write('计算方法：')
st.write('（1）实际产量 = 气候产量 + 趋势产量 + 随机误差')
st.latex(r'Y = Y_{t} + Y_{m} + e')
st.write('（2）气候影响因子σ与气候产量Yt的关系')
st.latex(r'Y_{w}=\sigma Y_{t}')
st.write('（3）趋势产量由实际产量进行移动平均得到，相比于实际产量更为平滑、更能反映出数据增长趋势')
st.write('（4） 气候影响因子σ与温度x的关系')
st.latex(r'\sigma = ax^{2}+bx+c')
temp = draw2()

st.subheader("计算气候影响因子，分析气候影响因子与温度之间关系", divider='rainbow')
dic_abc = sigma(temp)
st.write('气候影响因子σ与温度x的关系')
st.latex(r'\sigma = ax^{2}+bx+c')
st.write('其中，a={:.5f}, b={:.5f}, c={:.5f}'.format(dic_abc['a'], dic_abc['b'], dic_abc['c']))
st.markdown('''
            - **当气温过低时**（大致小于16℃），σ为负数，说明此时气温对于冬小麦生长、成熟起到负面作用；
            - **当气温过高时**（大致大于17.5℃），σ为负数，说明此时气温对于冬小麦生长、成熟起到负面作用；
            - **当气温适中时**（大致在16.5-17.0℃），σ为正，说明此时气温对于冬小麦生长、成熟起到正面作用；
            ''')


st.subheader("根据气候影响因子σ与气温的关系，计算气候产量", divider='rainbow')
st.write('由(1)(2)：')
st.latex(r'(1)Y = Y_{t} + Y_{m} + e')
st.latex(r'(2)Y_{w}=\sigma Y_{t}')
st.write('得到气候产量计算公式：')
st.latex(r'Y_{w}=\frac{\sigma Y}{1 + \sigma}')
df['气候影响因子'] = dic_abc['a']*df['AverageTemperature']**2 + dic_abc['b']*df['AverageTemperature'] + dic_abc['c']
df['气候产量'] = df['气候影响因子']*df['Product']/(1+df['气候影响因子'])
st.write('计算结果：')
df['year'] = df['year'].astype(str)
st.dataframe(df[['year', 'AverageTemperature', 'Product', '气候影响因子', '气候产量']], use_container_width=True)
st.write('绘制气候产量曲线：')
fig = plt.figure()
ax = fig.add_subplot(111)
df.plot(x='year', y='气候产量', ax=ax, color='#df9357', linewidth=2)
ax.set_ylabel('产量（万吨）')
ax1 = ax.twinx()
df.plot(x='year', y='AverageTemperature', ax=ax1, label='3-6月平均气温', color='#50696d',linewidth=1.5, linestyle='--')
ax1.set_ylabel('气温（℃）')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax1.get_legend_handles_labels()
plt.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
st.pyplot(fig)
st.markdown('''
            - 1980年以前，气候产量在0上下正常波动，气候变暖对于河南省冬小麦产量影响不大；
            - 1980年以后，特别是1990年之后，3-6月月均气温显著升高，σ随着气温的增长进入负数区域。相较于1980年以前，
            气候产量在大多数时间内都是负数，波动范围也更大。说明近年来全球气候变暖的大背景给河南省冬小麦的产量造成了不利影响。
            ''')