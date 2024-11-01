import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

base = pd.read_excel("气象要素合并.xlsx")

cities = base['city'].unique()
relevant_columns = ['city', '各月本站平均气压_value', '各月降水量_value', '日照时数_value', '相对湿度_value', '月平均气温_value', '极端最高气温_value', '极端最低气温_value']
data = base[relevant_columns]

data_aggregated = data.groupby('city').mean().reset_index()

city_names = data_aggregated['city']

data_features = data_aggregated.drop(columns=['city'])

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_features)

sse = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(data_scaled)
    sse.append(kmeans.inertia_)

st.title('城市气候聚类分析')
st.subheader("肘部法则图:", divider='rainbow')
plt.figure(figsize=(10, 8))
plt.plot(range(1, 11), sse, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Sum of squared distances')
plt.title('Elbow Method For Optimal k')
st.pyplot(plt)

k = 4
kmeans = KMeans(n_clusters=k, random_state=0)
data_aggregated['Cluster'] = kmeans.fit_predict(data_scaled)

st.subheader("聚类结果:", divider='rainbow')
st.dataframe(data_aggregated[['city', 'Cluster']], use_container_width=True)

st.subheader("聚类结果图:", divider='rainbow')
plt.figure(figsize=(10, 8))
sns.scatterplot(x=data_aggregated['月平均气温_value'], y=data_aggregated['各月降水量_value'], hue=data_aggregated['Cluster'], palette='viridis')
plt.xlabel('月平均气温')
plt.ylabel('月平均降水量')
plt.title('城市气候聚类分析')
st.pyplot(plt)

# WCSS (within-cluster sum of square)
wcss = kmeans.inertia_    
# 计算轮廓系数
silhouette_avg = silhouette_score(data_scaled, kmeans.labels_)

st.write('聚类评估:')
st.write(f"WCSS: {wcss}")
st.write(f"Silhouette Coefficient: {silhouette_avg}")