The PCAs are based on code provided by Dibakar Sigdel. The K-means part was based on https://www.askpython.com/python/examples/plot-k-means-clusters-python. The agglomerative clustering was based on https://www.dezyre.com/recipes/do-agglomerative-clustering-in-python. These 2 clustering methods were only used in the PCA with both PMDs and SMDs because the purpose was to find if there were clusters/groups that corresponded to PMD and SMD group identity.


1) PCA-Both.ipynb
This produces a PCA based on the proteins' 19-dimensional CaseOLAP scores and the 19 disease vectors.
Also, to check for groups of disease vectors, K-means and agglomerative clustering are used. The amount of clusters can be changed, but 3 is used because it showed the PMDs and SMDs clustering together the most. 


2) PCA-Primary.ipynb
This produces a PCA based on the PMDs' proteins' 19-dimensional CaseOLAP scores and the 19 disease vectors.


3) PCA-Secondary.ipynb
This produces a PCA based on the SMDs' proteins' 19-dimensional CaseOLAP scores and the 19 disease vectors.


4) PCA_Both.py
The same as (1) but a .py file which can be run in the Runner.ipynb in the caseolap folder. 


5) PCA_Primary.py
The same as (2) but a .py file which can be run in the Runner.ipynb in the caseolap folder. 


6) PCA_Secondary.py
The same as (3) but a .py file which can be run in the Runner.ipynb in the caseolap folder. 


7) Data
The output for these files.