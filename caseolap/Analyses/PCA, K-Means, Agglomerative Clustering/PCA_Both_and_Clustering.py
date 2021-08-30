# PCA based on code provided by Dibakar Sigdel
NUM_CLUSTERS = 3
print('Number of Clusters', NUM_CLUSTERS)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.tools as tls
from sklearn.decomposition import PCA
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import AgglomerativeClustering

sns.set(font_scale=2.8)

data = pd.read_csv('./result/caseolap.csv')
data = data.set_index('protein')
ndf = data

nonzero_dict = {}
for col in ndf.columns:
    nonzero = 0
    for i in range(0,len(ndf)):
        if(ndf[col][i] > 0):
            nonzero += 1
    nonzero_dict[col] = nonzero

def feature_norm(df):
    dff = df.copy(deep =True)
    fchr =  ["LHON", "MELAS", "ADOA", "Leigh", "MERRF", "KSS", "Alpers", "LBSL", "PDD", "PEO", "MS", "Parkin", "ALS", "AD", "Epil", "Schiz", "FA", "HSP", "WD"]
    for t in fchr:
        dff[t] = (df[t]-df[t].min())/(df[t].max()-df[t].min())
    return dff
ndfn = feature_norm(ndf)
ndfn.head()

tdata = ndf.copy(deep =True)

def pca_results(good_data, pca,fname):
	#clc  =['navy','green','firebrick','mediumslateblue','darkgoldenrod', 'deepskyblue',"red","blue"]

	# Dimension indexing
	dimensions = dimensions = ['Dimension {}'.format(i) for i in range(1,len(pca.components_)+1)]

	# PCA components
	components = pd.DataFrame(np.round(pca.components_, 4), columns = good_data.keys())
	components.index = dimensions

	# PCA explained variance
	ratios = pca.explained_variance_ratio_.reshape(len(pca.components_), 1)
	variance_ratios = pd.DataFrame(np.round(ratios, 4), columns = ['Explained Variance'])
	variance_ratios.index = dimensions

	# Create a bar plot visualization
	fig, ax = plt.subplots(figsize = (22,10))

	# Plot the feature weights as a function of the components
	components.plot(ax = ax, kind = 'bar' );
	ax.set_ylabel("Feature Weights",fontsize =20)
	ax.set_xticklabels(dimensions, rotation=0, fontsize = 20)


	# Display the explained variance ratios
	for i, ev in enumerate(pca.explained_variance_ratio_):
		ax.text(i-0.40, ax.get_ylim()[1] + 0.05, "Explained Variance\n %.4f"%(ev),fontsize =10)

	# Return a concatenated DataFrame
	plt.legend(fontsize =15)
	plt.savefig(fname)
	return pd.concat([variance_ratios, components], axis = 1)


wt_data = ndf.copy(deep =True)

wt_data.head()

from sklearn.decomposition import PCA

# TODO: Apply PCA by fitting the good data with the same number of dimensions as features
pca = PCA()
pca.fit(wt_data)


# Generate PCA results plot
pca_results(wt_data, pca, fname = 'Analyses/PCA, K-Means, Agglomerative Clustering/Data/pca-both-mito-weights.pdf')
pca_results(wt_data, pca, fname = 'Analyses/PCA, K-Means, Agglomerative Clustering/Data/pca-both-mito-weights.png')

clrs = []
for row,col in tdata.T.iteritems():
    val = np.array(col)
    mx = max(val)
    for item in val:
        if  mx == col[0]:
            grp =  'navy'
        elif mx == col[1]:
            grp =  'orange'
        elif mx == col[2]:
            grp = 'green'
        elif mx == col[3]:
            grp = 'red'
        elif mx == col[4]:
            grp = 'purple'
        elif mx == col[5]:
            grp = 'brown'
        elif mx == col[6]:
            grp = "pink"
        elif mx == col[7]:
            grp = "grey"
        elif mx == col[8]:
            grp =  'orange'
        elif mx == col[9]:
            grp = 'green'
        elif mx == col[10]:
            grp = 'red'
        elif mx == col[11]:
            grp = 'purple'
        elif mx == col[12]:
            grp = 'brown'
        elif mx == col[13]:
            grp = "pink"
        elif mx == col[14]:
            grp = "grey"
        elif mx == col[15]:
            grp =  'orange'
        elif mx == col[16]:
            grp = 'green'
        elif mx == col[17]:
            grp = 'red'
        elif mx == col[18]:
            grp = 'purple'

    clrs.append(grp)
    
    
pdata = ndf.copy(deep = True)
ppdata = ndf.copy(deep = True)   

# TODO: Apply PCA by fitting the good data with only two dimensions
pca = PCA(n_components=2)
pca.fit(pdata)

# TODO: Transform the good data using the PCA fit above
reduced_data = pca.transform(ppdata)

# Create a DataFrame for the reduced data
reduced_data = pd.DataFrame(reduced_data, columns = ['Dimension 1', 'Dimension 2'])

def biplot(good_data, reduced_data, pca,fname,clrs):
   

    fig, ax = plt.subplots(figsize = (25,15))
    clc  =['navy','orange','green','red','purple', 'brown',"pink","grey",'navy','orange','green','orange','purple', 'brown',"pink","grey",'pink','grey','navy']
    
    # scatterplot of the reduced data    
    ax.scatter(x=reduced_data.loc[:, 'Dimension 1'], y=reduced_data.loc[:, 'Dimension 2'], 
        facecolors = clrs, edgecolors= clrs, s=50, alpha=0.5)
    
    # Label the points: COMMENT OUT IF YOU WANT TO REMOVE THE ID LABELS
    #for i in range(0,len(reduced_data)):
    #    ax.annotate(wt_data.index.values[i], (reduced_data.loc[:, 'Dimension 1'][i],reduced_data.loc[:, 'Dimension 2'][i]), xytext=(5,5), textcoords='offset points')

    
    feature_vectors = pca.components_.T

    # we use scaling factors to make the arrows easier to see
    asize, tpos = 0.5, 0.5,
    

    # projections of the original features
    for i, v in enumerate(feature_vectors):
        
        ax.arrow(0, 0, v[0]*asize, v[1]*asize,head_width=0.001, head_length=0.0005, linewidth=1, color= clc[i])
        ax.text(v[0]*tpos+ 0.01, v[1]*tpos, good_data.columns[i], color=clc[i], 
                 ha='center', va='center', fontsize=25)
        
    plt.axis([-0.1, 0.3, -0.3, 0.5])
    ax.set_xlabel("PC 1", fontsize=50)
    ax.set_ylabel("PC 2", fontsize=50)
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.savefig(fname)
    #return ax

def biplot_labeled_points(good_data, reduced_data, pca,fname,clrs):
   

    fig, ax = plt.subplots(figsize = (25,15))
    clc  =['navy','orange','green','red','purple', 'brown',"pink","grey",'navy','orange','green','orange','purple', 'brown',"pink","grey",'pink','grey','navy']
    
    # scatterplot of the reduced data    
    ax.scatter(x=reduced_data.loc[:, 'Dimension 1'], y=reduced_data.loc[:, 'Dimension 2'], 
        facecolors = clrs, edgecolors= clrs, s=50, alpha=0.5)
    
    # Label the points: COMMENT OUT IF YOU WANT TO REMOVE THE ID LABELS
    for i in range(0,len(reduced_data)):
        ax.annotate(wt_data.index.values[i], (reduced_data.loc[:, 'Dimension 1'][i],reduced_data.loc[:, 'Dimension 2'][i]), xytext=(5,5), fontsize = 14, textcoords='offset points')

    
    feature_vectors = pca.components_.T

    # we use scaling factors to make the arrows easier to see
    asize, tpos = 0.5, 0.5,
    

    # projections of the original features
    for i, v in enumerate(feature_vectors):
        
        ax.arrow(0, 0, v[0]*asize, v[1]*asize,head_width=0.001, head_length=0.0005, linewidth=1, color= clc[i])
        ax.text(v[0]*tpos+ 0.01, v[1]*tpos, good_data.columns[i], color=clc[i], 
                 ha='center', va='center', fontsize=25)
        
    plt.axis([-0.1, 0.3, -0.3, 0.5])
    ax.set_xlabel("PC 1", fontsize=50)
    ax.set_ylabel("PC 2", fontsize=50)
    plt.axhline(y=0, color='k')
    plt.axvline(x=0, color='k')
    plt.savefig(fname)
    #return ax

newdata = ndf.copy(deep =True)
# Create a biplot
biplot(newdata, reduced_data, pca,'Analyses/PCA, K-Means, Agglomerative Clustering/Data/protein-both-biplot.pdf',clrs);
biplot(newdata, reduced_data, pca,'Analyses/PCA, K-Means, Agglomerative Clustering/Data/protein-both-biplot.png',clrs);

# Create a biplot
biplot_labeled_points(newdata, reduced_data, pca,'Analyses/PCA, K-Means, Agglomerative Clustering/Data/protein-both-labeled-biplot.pdf',clrs);
biplot_labeled_points(newdata, reduced_data, pca,'Analyses/PCA, K-Means, Agglomerative Clustering/Data/protein-both-labeled-biplot.png',clrs);

print('Made PCA...')

# K-means
#https://www.askpython.com/python/examples/plot-k-means-clusters-python
fv = pca.components_.T
from sklearn.cluster import KMeans
#Initialize the class object
kmeans = KMeans(n_clusters= NUM_CLUSTERS)
#predict the labels of clusters.
label = kmeans.fit_predict(fv)

import matplotlib.pyplot as plt
clc  =['red', "blue", "green","black","orange","purple","pink"]

u_labels = np.unique(label)
#plotting the results:
 
fig, ax = plt.subplots(figsize = (25,15))
asize, tpos = 0.5, 1.1

names = {}
for i, v in enumerate(fv):
    names[str(v)] = newdata.columns[i]

#plotting the results
for j in u_labels:
    plt.scatter(x = fv[label == j, 0], y = fv[label == j, 1], label = j, color= clc[j])
    for i, v in enumerate(fv[label == j]):
        ax.text(v[0]+0.009, v[1]+0.009, names[str(v)], color=clc[j], ha='center', va='center', fontsize=10)
        
ax.set_xlabel("PC 1", fontsize=50)
ax.set_ylabel("PC 2", fontsize=50)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.axis([-0.01, 0.65, -0.6, 0.7])
plt.legend()
plt.savefig('Analyses/PCA, K-Means, Agglomerative Clustering/Data/K-Means-on-PCA-Vector-Heads.png')
plt.savefig('Analyses/PCA, K-Means, Agglomerative Clustering/Data/K-Means-on-PCA-Vector-Heads.pdf')
#plt.show()

print('Made K-means...')

from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#https://www.dezyre.com/recipes/do-agglomerative-clustering-in-python
X = fv
data = pd.DataFrame(X)

cor = data.corr()
#sns.heatmap(cor, square = True); #plt.show()
scaler = StandardScaler()
X_std = scaler.fit_transform(X)
clt = AgglomerativeClustering(linkage="complete", affinity="euclidean", \
                              n_clusters=NUM_CLUSTERS)
model = clt.fit(X_std)
clusters = pd.DataFrame(model.fit_predict(X_std))
data["Cluster"] = clusters
labels = list(data["Cluster"])
fig = plt.figure(); ax = fig.add_subplot(111)
scatter = ax.scatter(data[0],data[1], c=data["Cluster"],s=50)
ax.set_title("Agglomerative Clustering")
ax.set_xlabel("PC 2"); ax.set_ylabel("PC 1")
plt.axis([-0.2, 0.7, -0.7, 0.65])
for i, v in enumerate(X):
    j = labels[i]
    ax.text(v[0]+0.009, v[1]+0.009, names[str(v)], color=clc[j], ha='center', va='center', fontsize=10)
        
#plt.axis([-1,1,-1,1])
plt.savefig('Analyses/PCA, K-Means, Agglomerative Clustering/Data/Agglomerative-Clustering-on-PCA-Vector-Heads.png')
plt.savefig('Analyses/PCA, K-Means, Agglomerative Clustering/Data/Agglomerative-Clustering-on-PCA-Vector-Heads.pdf') 
plt.colorbar(scatter); #plt.show()
print('Made Agglomerative Clustering...')
print('Finished!')