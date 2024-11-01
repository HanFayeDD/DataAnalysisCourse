import streamlit as st
import pandas as pd
import numpy as np
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

plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False 

pg = st.navigation([
    st.Page("1可视化.py", title="数据可视化", icon="🔥"),
    st.Page("2回归预测.py", title="回归预测", icon="🚂"),
    st.Page("3聚类分析.py", title="聚类分析", icon="😍"),
    st.Page("4河南省冬小麦产量与气温.py", title="河南省冬小麦产量与气温关系", icon="🚅"),
])
pg.run()


