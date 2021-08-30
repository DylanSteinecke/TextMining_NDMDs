# Entities Ranked By Top CaseOLAP Score
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# Run in Runner
from IPython.core.display import display, HTML
#display(HTML("<style>.container { width:90% !important; }</style>"))

scores = pd.read_csv('./result/caseolap.csv')
cols = list(scores.columns)
entities = cols[0]

top_scores = pd.DataFrame(columns = cols)
for i in range(0,len(scores)):
    top_scores = top_scores.append(pd.Series(0.0, index=cols), ignore_index=True)
top_scores.columns = cols
top_scores = top_scores.drop(['protein'], axis=1)       #<---switch out with the entity column name depending on your entity
top_entities = top_scores.copy()

for i in range(1,len(cols)):
    categ_scores = list(scores[cols[i]])
    end = len(categ_scores)
    
    for j in range(0,len(categ_scores)):
        TOP = max(categ_scores)
        if(TOP == 0.0): break
        TOP_ind = categ_scores.index(TOP)
        top_scores.iloc[j,i-1] = TOP
        top_entities.iloc[j,i-1] = scores[entities][TOP_ind]
        categ_scores[TOP_ind] = -1
        
top_scores.index = range(1,end+1)
print('Made Top Scores...')
#display(top_scores)
top_scores.to_csv('Analyses/Top Entities, Top Pathways/Data/top_scores.csv')

top_entities.index = range(1,end+1)
print('Made Top Entities...')
#display(top_entities)
top_entities.to_csv('Analyses/Top Entities, Top Pathways/Data/top_entities.csv')

alltop_entities = set()
for row in range(1,end+1):
    for col in top_entities.columns:
        alltop_entities.add(top_entities.loc[row,col])
        
total_instances = 0
for i in range(1,len(top_entities)):
    for col in top_entities.columns[1:20]:
        if(top_entities[col][i] != '0.0'):
            total_instances += 1
total_top = total_instances
unique_top = len(alltop_entities)
# Not working: print('Unique Entities / Total Entities in all categories: ', unique_top, '/', total_top)

print('Heatmap of Top Entities')
df = top_scores
#display(df.style.background_gradient(cmap ='Reds').set_properties(**{'font-size': '10px'}))
print('Finished!')