# Adapted from Vladimir Guevara
import pandas as pd
# Finds all PMIDs in PubMed with Abstracts, Finds PMIDs with Full Text
fin = open('../../../../caseolap/data/pubmed.json', 'r')    
total_pmids = 0
title_pmids = []
abstract_pmids = []
full_text_pmids =[]
for line in fin:
    
    title = line.split("\"ArticleTitle\": ")[1].split(", \"Abstract\": ")[0]
    # If there is a title, store the PMID
    if(title != "\"\""):
        pmid = int(line.split("PMID\": \"")[1].split("\", ")[0])
        title_pmids.append(pmid)
    
    abstract = line.split("\"Abstract\": ")[1].split(", \"MeshHeadingList\":")[0]
    # If there is anything in abstract, store the PMID
    if(abstract != "\"\""):
        pmid = int(line.split("PMID\": \"")[1].split("\", ")[0])
        abstract_pmids.append(pmid)
    
    full_text = line.split("\"full_text\": ")[1].split(", \"Journal\":")[0]    # If there is anything in full_text, store the PMID
    if(full_text != "\"\""):
        pmid = int(line.split("PMID\": \"")[1].split("\", ")[0])
        full_text_pmids.append(pmid)
        
    total_pmids += 1
    if(total_pmids % 1000000 == 0):
        print("Total PMIDs Sorted Through:", total_pmids, end = '\r')
        
print('\nTitle PMIDs: ', len(title_pmids))
print('Abstract PMIDs: ', len(abstract_pmids)) 
print('Full text PMIDs: ', len(full_text_pmids))





# Makes PMID list of PMIDs used in this study
usedpmidList_ = []
f_cat2pmid = open('data/entityfound_pmid2cell.txt')
i = 0
for line in f_cat2pmid:
    pmid = line.split('	')[0]
    cat = line.split('	')[1].split('\n')[0]
    if(pmid != 'doc_id'):
        usedpmidList_.append(pmid)
usedpmidList = pd.DataFrame(usedpmidList_)
usedpmidList.to_csv('Analyses/Text_Analyses/Data/usedpmidList.csv')
usedPMIDlist = pd.read_csv('Analyses/Text_Analyses/Data/usedpmidList.csv', index_col=0)
f_cat2pmid.close()



# Find how many PMIDs in the nd_mito2 index have abstracts, have full text
ND_pmidsDF = pd.read_csv('Analyses/Text_Analyses//Data/pmidList.csv', index_col=0); ND_pmids = []
for row in ND_pmidsDF.iterrows():
    ND_pmids.append(row[0])
print('\nND Mito PMIDs: ', len(ND_pmids))  # All PMIDs in current database

print('Titles in indexed database: ', len(set(title_pmids).intersection(ND_pmids)), '/', len(ND_pmids), ' = ', round(len(set(title_pmids).intersection(ND_pmids))/len(ND_pmids), 4)*100, '%')
print('Abstracts in indexed database: ', len(set(abstract_pmids).intersection(ND_pmids)), '/', len(ND_pmids), ' = ', round(len(set(abstract_pmids).intersection(ND_pmids))/len(ND_pmids), 4)*100, '%')
print('Full text in indexed database: ',len(set(full_text_pmids).intersection(ND_pmids)), '/', len(ND_pmids), ' = ', round(len(set(full_text_pmids).intersection(ND_pmids))/len(ND_pmids), 4)*100, '%\n')

# Find how many PMIDs *USED* in the nd_mito2 index have abstracts, have full text
ND_used_pmidsDF = pd.read_csv('Analyses/Text_Analyses/Data/usedpmidList.csv', index_col=0); ND_used_pmids = []
for row in ND_used_pmidsDF.iterrows():
    ND_used_pmids.append(row[0])
print('\nND Mito PMIDs Used: ', len(ND_used_pmids))  # All PMIDs in current database

print('Titles *used* in indexed database: ', len(set(title_pmids).intersection(set(ND_used_pmids))), '/', len(ND_used_pmids), ' = ', round(len(set(title_pmids).intersection(set(ND_used_pmids)))/len(ND_used_pmids), 4)*100, '%')
print('Abstracts *used* in indexed database: ', len(set(abstract_pmids).intersection(set(ND_used_pmids))), '/', len(ND_used_pmids), ' = ', round(len(set(abstract_pmids).intersection(set(ND_used_pmids)))/len(ND_used_pmids), 4)*100, '%')
print('Full text *used* in indexed database: ',len(set(full_text_pmids).intersection(set(ND_used_pmids))), '/', len(ND_used_pmids), ' = ', round(len(set(full_text_pmids).intersection(set(ND_used_pmids)))/len(ND_used_pmids), 4)*100, '%')


fin.close()