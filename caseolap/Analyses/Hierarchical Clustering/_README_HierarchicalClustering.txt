This folder contains programs and data for hierarchical clustering based on the proteins' 19-dimensional CaseOLAP scores corresponding to the 19 disease catgegories. 

The notebooks can be run within this folder.
The .py file should be run in the Runner.ipynb which is in the caseolap folder. 

1) HierarchicalCluster_CombinedSection.ipynb
This version has the entire code in one cell.

2) HierarchicalCluster_SeparatedSections.ipynb
This version has the code split into different cells based on the section of the code. This is more ideal when trying to tweak only one or some parts of the program without having to run the sections which take longer to run (such as the clustering).

3) HierarchicalCluster_Cutoff.ipynb
This version allows the user to set a custom cutoff value. This cutoff value only includes proteins which have at least one of their 19 scores (i.e. one score in the 19 disease categories) large enough based on the cutoff. This subset of proteins is used for the hierarchical clustering.

4) HierarchicalCluster.py
This is a .py script version which can be run in the Runner.ipynb or somewhere else within that directory (unless the paths are changed). 


5) Data
This contains the outputs for the above programs. 