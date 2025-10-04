import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import StandardScaler
from matplotlib.patches import Patch
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
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(X_scaled)
df = df.sort_values(by=['cluster', 'user_len_mean'], ascending=[True, True])
cluster_palette = ['#1f77b4', '#ff7f0e', '#2ca02c']
cluster_colours = df['cluster'].map(dict(zip(df['cluster'].unique(), cluster_palette)))


fig = plt.figure(figsize=(18, 7))
gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1])

# Bar plot
ax1 = fig.add_subplot(gs[0])
ax1.bar(df['user'], df['ai_len_mean'], alpha=0.7, label='AI', color='gray')
ax1.bar(df['user'], df['user_len_mean'], alpha=0.7, label='User', color=cluster_colours)
ax1.set_title('Mean message length: AI vs User', fontsize=14)
ax1.set_ylabel('Mean message length', fontsize=14)
ax1.tick_params(axis='x', rotation=90, labelsize=12)

# Dendrogram plot
# from scipy.cluster.hierarchy import dendrogram, linkage
# linked = linkage(X_scaled, method='ward')
# dendrogram(linked, labels=df['user'].values, orientation='top', distance_sort='descending')

# K-means clustering plot
ax0 = fig.add_subplot(gs[1])
scatter = ax0.scatter(df['user_msg_mean'], df['user_len_mean'],
                      c=df['cluster'], 
                      cmap=ListedColormap(cluster_palette), 
                      s=100, alpha=0.7)
ax0.set_title('K-means Clustering (K=3)', fontsize=14)
ax0.set_xlabel('Average number of messages', fontsize=14)
ax0.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0f}'))
ax0.set_ylabel('Average message length', fontsize=14)
texts = []
for i, row in df.iterrows():
    texts.append(
        ax0.text(row['user_msg_mean'], row['user_len_mean'], row['user'],
                 fontsize=10, alpha=0.7)
    )
adjust_text(texts, ax=ax0)

custom_legend = {
    'AI': 'gray',
    '"Web search" users': '#1f77b4',
    '"Conversational" users': '#ff7f0e',
    '"Interactive journal" users': '#2ca02c'
}
handles = [Patch(color=colour, label=label) for label, colour in custom_legend.items()]
fig.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, 1.075), ncol=len(handles), fontsize=14)
plt.tight_layout()
plt.savefig("chat_stats.pdf", bbox_inches="tight", transparent=True)