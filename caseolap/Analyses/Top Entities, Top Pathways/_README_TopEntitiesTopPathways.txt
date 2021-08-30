.py files can be run in the Runner in the caseolap folder.
Notebook (.ipynb) files can be run in here and will display the dataframes and heatmaps better. 
Either way, the dataframes and heatmaps can be found in the Data folder. 

Files names with (entities) can be reused for future uses which do or don't use proteins as their entities. 


1) CaseOLAP_Ranked_Entities_in_Each_Category.ipynb
This ranks all entities (i.e. proteins) in each category (i.e. disease) based on CaseOLAP scores. 


2) Popularity_Ranked_Entities_in_Each_Category.ipynb
This ranks all entities (i.e. proteins) in each category (i.e. disease) based on frequency of occurence in the dataset (i.e. popularity). This is likely a better way to understand what is most important in each category because CaseOLAP scores will be lower if an entity (i.e. protein) is important in multiple or all categories. 
 

3) Popularity_Ranked_Pathways_in_Each_Category.ipynb
This ranks all pathways in each category (i.e. disease) based on frequency of occurence in the dataset (i.e. popularity). This is likely a better way to understand what is most important in each category because CaseOLAP scores will be lower if an entity (i.e. protein) is important in multiple or all categories. Entities (i.e. proteins) were submitted to Reactome pathways database and were then mapped to pathways. Thus, the pathway popularity corresponds to the protein popularity. 


4) Top 10 CaseOLAP Entities in Each Category Notebook.ipynb
This ranks the top 10 entities (i.e. proteins) in each category (i.e. disease) based on CaseOLAP scores. Same as (1) but only for 10, not all entities. 


5) CaseOLAP_Ranked_Entities_in_Each_Category.py
Same as (1) but .py


6) Popularity_Ranked_Entities_in_Each_Category.py
Same as (2) but .py


7) Popularity_Ranked_Pathways_in_Each_Category.py
Same as (3) but .py

