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

plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False 


def draw_1760_2015_global_temp():
    df = pd.read_csv('GlobalData\GlobalTemperatures.csv')
    df = df.iloc[:, :3]
    df['dt'] = df['dt'].astype(str)
    df['year'] = df['dt'].str[:4]
    p = df.groupby(['year'])['LandAverageTemperature'].mean()
    p = p.reset_index()
    st.line_chart(data=p, x='year', y='LandAverageTemperature')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(p['year'], p['LandAverageTemperature'], label='LandAverageTemperature')
    newx = list(range(p.shape[0]))
    newy = p['LandAverageTemperature'].to_list()
    z = np.polyfit(newx, newy, 1)
    p_fit = np.poly1d(z)
    ax.plot(newx, p_fit(newx), "r--", label='Trend Line')
    plt.xlabel('year')
    plt.ylabel('LandAverageTemperature(℃)')
    plt.legend()
    plt.xticks(list(range(0, len(newx), 10)), rotation=45)
    st.pyplot(fig)
    st.write("注:趋势线由线性回归得到")
    
def draw_by_city_country(name:str):
    df = df_country.loc[df_country['Country']==name]
    p = df.groupby(['year'])['AverageTemperature'].mean()
    p = p.reset_index()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    p.plot(x='year', y='AverageTemperature', kind='line', ax=ax)
    plt.ylabel('AverageTemperature(℃)')
    st.pyplot(fig)
    st.write("注:部分折线不连续是因为数据缺失")


def draw_by_city_name(cn:str):
    temp = base.loc[base['city']==cn]
    st.write(''+cn+'气象要素数据表格')
    st.dataframe(temp)
    aver = temp['月平均气温_value'].astype(float).to_list()
    hig = temp['极端最高气温_value'].astype(float).to_list()
    low = temp['极端最低气温_value'].astype(float).to_list()
    date = temp['date'].astype(str).to_list()
    aver = [round(el, 1) for el in aver]
    hig = [round(el, 1) for el in hig]
    low = [round(el, 1) for el in low]
    line = Line()
    line.add_xaxis(date).add_yaxis('月平均气温', aver).add_yaxis('极端最高气温', hig).add_yaxis('极端最低气温', low)
    line.set_global_opts(datazoom_opts=opts.DataZoomOpts(is_show=True),
                         toolbox_opts=opts.ToolboxOpts(is_show=True),
                         title_opts=opts.TitleOpts(title=cn + '气温变化图'))
    st_pyecharts(line)
    ll = ['各月本站平均气压_value', '各月降水量_value', '日照时数_value',  '相对湿度_value']
    for ele in ll:
        st.write('{:}{:}变化'.format(cn, ele.split('_')[0]))
        pp = temp.loc[:, ['date', ele]]
        st.line_chart(pp, x='date', y=ele)
    
    # 绘制热力图
    st.subheader("{:}气象要素相关性热力图".format(cn), divider='rainbow')
    relevant_columns = ['各月本站平均气压_value', '各月降水量_value', '日照时数_value', '月平均气温_value', '极端最高气温_value', '极端最低气温_value','相对湿度_value']
    data = temp[relevant_columns]
    correlation_matrix = data.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
    st.pyplot(plt)
    st.markdown("##### 相关性分析结果:")
    st.markdown(
    '''
        热力图展示了几个气象变量之间的线性关系。每个值代表了两个变量之间的相关系数，取值范围在-1到1之间。
        根据大多数城市的热力图，我们来逐一分析这些变量之间比较明显的关系：
        - 平均气压与平均气温、极端最高气温、极端最低气温的相关性都接近-1，呈负相关，说明平均气温增加时，平均气压会显著减少。
        - 降水量与相对湿度的相关性大多都大于0.5，呈中度正相关，这意味着降水量增加时，相对湿度显著增加
        - 降水量与日照时数的相关性大多在-0.2和0之间，呈轻微负相关，这意味着降水量增加时，日照时数略微减少。
        - 平均气温和降水量相关性大多在0.5以上，呈中度正相关，这意味着气温增高时，降水量也会增加。
        - 平均气温和极端最高气温相关性较高，呈正相关，这意味着平均气温升高时，极端最高气温也显著升高。
        - 平均气温和极端最低气温相关性较高，呈正相关这意味着平均气温升高时，极端最低气温也显著升高。
        
        从上述分析可以看出：
        - 平均气温、极端最高气温和极端最低气温之间的正相关性很强，表明它们在变化时有一致的趋势。
        - 日照时数与平均气温、极端最高气温和极端最低气温也有较强的正相关性，表明日照时数对气温有显著影响。
        - 降水量和相对湿度之间的正相关性较强，表明降水量的增加通常伴随着相对湿度的增加。
        - 平均气压与其他变量（尤其是气温）的负相关性较强，表明气温的变化对气压有较大的影响。
    '''
    )




st.title("数据可视化")
st.subheader("1760-2015年全球气温变化", divider='rainbow')
draw_1760_2015_global_temp()

st.subheader("全球国家/地区气温变化", divider='rainbow')
df_country = pd.read_csv("GlobalData\GlobalLandTemperaturesByCountry.csv")
df_country['dt'] = df_country['dt'].astype(str)
df_country['year'] = df_country['dt'].str[:4]
option1 = st.selectbox(
    "选择一个国家",
    ['Åland', 'Afghanistan', 'Africa', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua And Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Asia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Baker Island', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bonaire, Saint Eustatius And Saba', 'Bosnia And Herzegovina', 'Botswana', 'Brazil', 'British Virgin Islands', 'Bulgaria', 'Burkina Faso', 'Burma', 'Burundi', "Côte D'Ivoire", 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'China', 'Christmas Island', 'Colombia', 'Comoros', 'Congo (Democratic Republic Of The)', 'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark (Europe)', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Europe', 'Falkland Islands (Islas Malvinas)', 'Faroe Islands', 'Federated States Of Micronesia', 'Fiji', 'Finland', 'France (Europe)', 'France', 'French Guiana', 'French Polynesia', 'French Southern And Antarctic Lands', 'Gabon', 'Gambia', 'Gaza Strip', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea Bissau', 'Guinea', 'Guyana', 'Haiti', 'Heard Island And Mcdonald Islands', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Isle Of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kingman Reef', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macau', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Mali', 'Malta', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands (Europe)', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'North America', 'North Korea', 'Northern Mariana Islands', 'Norway', 'Oceania', 'Oman', 'Pakistan', 'Palau', 'Palestina', 'Palmyra Atoll', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russia', 'Rwanda', 'Saint Barthélemy', 'Saint Kitts And Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Pierre And Miquelon', 'Saint Vincent And The Grenadines', 'Samoa', 'San Marino', 'Sao Tome And Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South America', 'South Georgia And The South Sandwich Isla', 'South Korea', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Svalbard And Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor Leste', 'Togo', 'Tonga', 'Trinidad And Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks And Caicas Islands', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom (Europe)', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Virgin Islands', 'Western Sahara', 'Yemen', 'Zambia', 'Zimbabwe']
)
draw_by_city_country(option1)

st.subheader("我国主要城市气象要素可视化", divider='rainbow')
base = pd.read_excel("气象要素合并.xlsx")
option = st.selectbox(
    "选择一个城市",
    ('北京', '天津', '石家庄', '太原', '呼和浩特', '沈阳', '长春', '哈尔滨', '上海', '南京',
       '杭州', '合肥', '福州', '南昌', '济南', '郑州', '武汉', '长沙', '广州', '南宁', '海口',
       '重庆', '成都', '贵阳', '昆明', '拉萨', '西安', '兰州', '西宁', '银川', '乌鲁木齐'))
draw_by_city_name(option)

