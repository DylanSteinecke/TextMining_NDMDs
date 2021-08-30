import json
import sys
import time
import pandas as pd
import time



"""
This class builds a Text-Cube.
"""
class TextCube(object):
    
    
    def __init__(self,cell_names):
        
        
        self.cell_names = cell_names
        self.concerned_cat = []
        self.pmid2cell = []
        
    

        
    """
    Collect all descendent MeSH terms for each root terms for a category
    """
    def descendent_MeSH(self,input_file_root_cat,input_file_meshtree,outputfile_MeSHterms_percat,logfile):
        
        print("descendent MeSH terms are being collected....")
        logfile.write("descendent MeSH terms are being collected.... \n")
        logfile.write("=================================================== \n")
        
        with open(input_file_root_cat, "r") as f_cat:
            for line in f_cat:
                self.concerned_cat.append(line.strip().split())
                
        self.num_cat = len(self.concerned_cat)
        
        self.MeSH_terms_per_cat = [set() for _ in range(self.num_cat)]
        with open(input_file_meshtree, "r") as f_tree:
            for line in f_tree:
                
                term_tree = line.strip().split(";")
                cur_term = term_tree[0]
                cur_tree = term_tree[1]
                
                for i in range(self.num_cat):
                    for cur_cat_tree in self.concerned_cat[i]:
                        if cur_cat_tree in cur_tree:
                            # BLOCK A: Prevent duplicate terms from being added to multiple nodes #
                            # To customize, use code in Block B to find duplicates. Choose        #
                            # the category you don't want the term to be added to.                #
                            if(cur_term == 'Kearns-Sayre Syndrome' and i == 9):                   #
                                print('Not adding KSS to category 9')                             #
                            elif(cur_term == 'MERRF Syndrome' and i == 14):                       #
                                print('Not adding MERRF Syndrome to category 14')                 #
                            else:                                                                 #
                                self.MeSH_terms_per_cat[i].add(cur_term)                          #
            
            #BLOCK B: Identifying duplicate terms. See the printed message and then look in  #
            # the mesh_terms_per_cat.json to see the categories                              #
            cat_num = -1;                                                                    #
            for cat in self.MeSH_terms_per_cat:                                              #
                cat_num += 1                                                                 #
                for mesh_term in cat:                                                        #
                                                                                             #
                    catcomp_num = -1                                                         #
                    for CAT in self.MeSH_terms_per_cat:                                      #
                        catcomp_num += 1                                                     #
                        for MESH_TERM in CAT:                                                #
                            #print('MESH_TERM', MESH_TERM)                                   #
                            if(mesh_term == MESH_TERM and cat_num != catcomp_num):           #
                                print(mesh_term, 'found in disease #', cat_num, 'and ', catcomp_num)#
        
        
        for i in range(self.num_cat):                    
            logfile.write(self.cell_names[i] + " : includes decendents " + str(self.MeSH_terms_per_cat[i]) + "\n")

        MeSHset = []
        for item in self.MeSH_terms_per_cat:
            MeSHset.append(list(item))
        with open(outputfile_MeSHterms_percat, "w") as f_out:
            json.dump(MeSHset,f_out)

                    
    """
    Find corresponding papers for each category.
    """
    def cell2pmids_mapping(self,input_file_mesh2pmid,output_file_textcube_cell2pmid,logfile):
        
        start_time = time.time()
        #print('start_time of cell2pmids_mapping', round(start_time, 4))
        print("Textcube cell to PMID mapping is being created....")
        logfile.write("Textcube cell to PMID mapping is being created.... \n")
        logfile.write(" ========================================== \n")
        
        self.cell2pmid = [set() for _ in range(len(self.cell_names))]
        with open(input_file_mesh2pmid, "r") as f_in:   # A dictionary with Term:[PMID,...,PMID] for a lot of terms and PMIDs
            start = time.time()
            k = 0
            for line in f_in:    # Term:PMID,...,PMID
                mesh2pmid = {}
                Info = json.loads(line.strip())
                for key,value in Info.items():
                    mesh2pmid.update({key:value})   #Make it Term:PMID,...,Term:OtherPMID

                k = k+1
                if k%1000 ==0:
                    print(k,'MeSH descriptors analysed for textcube...!')
                    logfile.write(str(k) + 'MeSH descriptors analysed for textcube...! \n')
                  
                    
                for i in range(self.num_cat):       # Cycle through each disease category
                    for cur_term in self.MeSH_terms_per_cat[i]:  # Cycle through each disease category's synonyms
                        if cur_term == key:         # If the disease category's synonym matches the current name in the mesh2pmid dict
                            self.cell2pmid[i] = self.cell2pmid[i] | set(mesh2pmid[cur_term]) # create a dict of relevant Terms : PMIDs
                            
        Cell2PMID = []
        for item in self.cell2pmid:
            Cell2PMID.append(list(item))
        
        beforenewfunctiontime = round(time.time() - start_time, 4)
        print("BEFORE NEW FUNCITON: --- %s seconds ---" % beforenewfunctiontime)
        
        #################################################################################################################################
        # I added this section here to have the option of removing PMIDs which appear in multiple categories
        L = Cell2PMID.copy()  #The original list to be iterated through
        Lc = L.copy()         #A copy which be modified to remove duplicate pmids
        
        pmidOverlaps = pd.DataFrame(columns = [i for i in range(0,len(L))]); 
        pmidProportions = pmidOverlaps.copy()
        pmidSizes = pmidOverlaps.copy()

        #### Remove duplicates within each category ####
        for i in range(0,len(L)): Lset = list(set(L[i])); print('Duplicates found within cat #', i, ': ', len(L[i]) - len(Lset), '/', len(L[i]), 'New size --> ', len(Lset)); Lc[i] = Lset 
        L = Lc.copy()

        #### Remove duplicates across categories ####
        for i in range(0,len(L)):
            rOverlaps = {}; rSizes = {}; rProportions = {}; Lcij_temp = set()
            for j in range(0,len(L)):
                if(i != j):
                    Lc[i] = list(set(Lc[i]) - set(L[j]))
                    rOverlaps[j] = len(L[i]) - len(list(set(L[i]) - set(L[j])))
                    rSizes[j] = len(L[i]) + len(L[j])
                    rProportions[j] = round(rOverlaps[j]/rSizes[j], 3)
                else:
                    rOverlaps[j] = 'N/A'
                    rSizes[j] = 'N/A'
                    rProportions[j] = 'N/A'
            pmidOverlaps = pmidOverlaps.append(rOverlaps, ignore_index = True)
            pmidSizes = pmidSizes.append(rSizes, ignore_index = True)
            pmidProportions = pmidProportions.append(rProportions, ignore_index = True) 
        
        print('Made pmidOverlaps (How many duplicate PubMed IDs are in both categories i and j where i and j are rows and columns)')
        print('Made pmidSizes (How many total PubMed IDs are in categories i + j where i and j are rows and columns')
        print('Made pmidProportions (pmidOverlaps/pmidSizes)')
        pmidOverlaps.to_csv('Analyses/Text_Analyses/Data/pmidOverlaps.csv')
        pmidSizes.to_csv('Analyses/Text_Analyses/Data/pmidSizes.csv')
        pmidProportions.to_csv('Analyses/Text_Analyses/Data/pmidProportions.csv')
        
        ###############################################################################################################################
        afternewfunctiontime = round(time.time() - start_time, 4)
        print("AFTER NEW FUNCTION --- %s seconds ---" % afternewfunctiontime)
     
        self.cell2pmid = Lc.copy()
        pmidLIST = []
        for LIST in Lc:
            pmidLIST += LIST
        pmidList = pd.DataFrame(pmidLIST)
        pmidList.to_csv('Analyses/Text_Analyses/Data/pmidList.csv')
        print('Made pmidList (A list of the PubMed IDs for all the documents considered/analyzed in this study.')
        
        # Outputs the file with list of categories' PMIDs which only have *one* of the studied disease categories' MeSH Terms
        # To change it to the file allowing *multiple* studied disease categories in a publication, switch Cell2PMID_Copy to Cell2PMID
        with open(output_file_textcube_cell2pmid, "w") as f_out:
            json.dump(Lc, f_out)
        
        diffdocs = []
        for k,name in enumerate(self.cell_names):    
            logfile.write("Cell - " + name + " : includes " + str(len(L[k])) + " documents. --> " + str(len(Lc[k])) + "documents exclusively containing MeSH terms for this disease and not any of the other disease categories of interest. \nRemoved " + str(len(L[k]) - len(Lc[k])) + str(len(self.cell2pmid[k])) + 'All good? (self.cell2pmid == L, i.e. object == variable): ' + str((len(self.cell2pmid[k]))==len(Lc[k])) + "\n")
            print("Cell - " + name + " : includes " + str(len(L[k])) + " documents. --> " + str(len(Lc[k])) + " documents exclusively containing MeSH terms for this disease and not any of the other disease categories of interest. \nRemoved " + str(len(L[k]) - len(Lc[k])) + "Also self.cell2pmid[k] is "  + str(len(self.cell2pmid[k])) + "\nAll good? (self.cell2pmid == L, i.e. object == variable): " + str((len(self.cell2pmid[k]))==len(Lc[k])) + "\n")
            diffdocs.append([name, len(L[k]), len(Lc[k]), round(((len(L[k]) - len(Lc[k]))/len(L[k])),4)]) #Category name, length before removing duplicates across categories, length after removing duplicates across categories, percent removed
        
        diffd = pd.DataFrame(diffdocs)
        diffd.to_csv('Analyses/Text_Analyses/Data/diffdocs.csv')
                         
        totaltime = round(time.time() - start_time, 4)
        print("MODIFIED FUNCTION ADDED ", round(afternewfunctiontime - beforenewfunctiontime,4), " out of a total of ", totaltime, " which is ", round((afternewfunctiontime - beforenewfunctiontime)/(totaltime-(afternewfunctiontime - beforenewfunctiontime)),4)*100, "% more")   
                
        
    """
    Serialize papers
    """
    def pmid2cell_mapping(self,output_file_textcube_pmid2cell,logfile):
        
        print("Textcube PMID to cell mapping is being created....")
        logfile.write("Textcube PMID to cell mapping is being created.... \n")
        logfile.write("============================================== \n")
        
        for i in range(self.num_cat):
            for cur_pmid in self.cell2pmid[i]:
                self.pmid2cell.append([cur_pmid, i])

        with open(output_file_textcube_pmid2cell, "w") as f_out:
            json.dump(self.pmid2cell, f_out)
            


    """
    Print cell statistics
    """
    def cell_statistics(self,outputfile_textcube_stat,logfile): 
        
        print("Textcube cell statistics is being created....")
        logfile.write("Textcube cell statistics is being created.... \n")
        logfile.write("================================================ \n")
        
        with open(outputfile_textcube_stat, "w") as f_stat:
            allpmid = [] 
            cell_count = [0 for i in range(self.num_cat)]
            for item in self.pmid2cell:
                allpmid.append(item[0])
                for i in range(self.num_cat):
                    if item[1] == i:
                        cell_count[i] += 1
           
            for k,name in enumerate(self.cell_names):
                f_stat.write("Total documents selected in cell - " + str(name) + " is "
                   + str(cell_count[k]) + " out of total " + str(len(set(allpmid)))   + " documents . \n" )
        print('Finished!')


