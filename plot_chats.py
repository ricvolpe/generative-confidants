import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from adjustText import adjust_text

file_path = 'data/chat_stats_grouped.xlsx'
df = pd.read_excel(file_path, sheet_name=0)
df = df[~df['user'].isin(['harlow', 'vic'])]
df['user'] = df['user'].str.capitalize()

X = df[['user_msg_mean', 'user_len_mean']].copy()
X['user_msg_count'] = X['user_len_mean'].apply(lambda x: np.log1p(x))
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

# Bar plot
ax1 = fig.add_subplot(gs[0])
ax1.bar(df['user'], df['ai_len_mean'], alpha=0.7, label='AI')
ax1.bar(df['user'], df['user_len_mean'], alpha=0.7, label='User')
ax1.set_title('Mean message length: AI vs User', fontsize=14)
ax1.set_ylabel('Mean message length', fontsize=12)
ax1.legend(facecolor='none',edgecolor='none', framealpha=0, fontsize=12)
ax1.tick_params(axis='x', rotation=90, labelsize=12)

# Dendrogram plot
# from scipy.cluster.hierarchy import dendrogram, linkage
# linked = linkage(X_scaled, method='ward')
# dendrogram(linked, labels=df['user'].values, orientation='top', distance_sort='descending')

# K-means clustering plot
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)
ax0 = fig.add_subplot(gs[1])
scatter = ax0.scatter(df['user_msg_mean'], df['user_len_mean'],
                      c=df['cluster'], 
                      cmap=ListedColormap(['#1f77b4', '#ff7f0e', '#2ca02c']), 
                      s=100, alpha=0.7)
ax0.set_title('K-means Clustering (K=3)', fontsize=14)
ax0.set_xlabel('Average message length', fontsize=12)
ax0.set_ylabel('Average number of messages', fontsize=12)
handles, _ = scatter.legend_elements()
ax0.legend(handles, ["Search", "Conversation", "Journal"])
texts = []
for i, row in df.iterrows():
    texts.append(
        ax0.text(row['user_msg_mean'], row['user_len_mean'], row['user'],
                 fontsize=10, alpha=0.7)
    )
adjust_text(texts, ax=ax0)


plt.tight_layout()
plt.savefig("chat_stats.pdf", bbox_inches="tight", transparent=True)