import pandas as pd
#from IPython.display import display

# Run in Runner
# Use the notebook to see a nicer display of the dataframes, particularly the heatmap

# Protein --> Pathway mapping
pathways = pd.read_csv('../Knowledge Graph/data/pw2proteins.csv')

# Disease Category --> PMID mapping
# Make a dictionary of Disease Name: [PMID,...PMID], ...
cat2pmid = {}
cat_name = pd.read_json('./config/textcube_config.json')[0]
f_cat2pmidegory = open('./data/entityfound_pmid2cell.txt')
i = 0
for line in f_cat2pmidegory:
    pmid = line.split('	')[0]
    cat = line.split('	')[1].split('\n')[0]
    i += 1

    if(pmid != 'doc_id'):
        cat_num = int(cat)
        if(cat_name[cat_num] not in cat2pmid.keys()):
            cat2pmid[cat_name[cat_num]] = []
        cat2pmid[cat_name[cat_num]].append(pmid)   


        
cat2protein = {}
cat2prot = {}
cat2pathway = {}
cat2pw = {}
for cat,v in cat2pmid.items():
    cat2protein[cat] = []
    cat2prot[cat] = []
    cat2pathway[cat] = []
    cat2pw[cat] = []

# Category: Proteins
f_entitycount = open('./data/entitycount.txt')
for line in f_entitycount:
    pmid = line.split(' ')[0]
    protein_freq = line.split(' ')[1:]
    protein_list = []
    for prot in protein_freq:
        protein_list.append(prot.split('|'))
    
    for category,pmids in cat2pmid.items():
        if(pmid in cat2pmid[category]): 
            for protein in protein_list:
                cat2protein[category].append(protein)
    
for cat,prot_lists in cat2protein.items():
    curr_cat_prot_dict = {}
    for prot_list in prot_lists:
        protein = prot_list[0]
        freq = int(prot_list[1].split('\n')[0])
        if(protein not in curr_cat_prot_dict.keys()):
            curr_cat_prot_dict[protein] = 0
        curr_cat_prot_dict[protein] += freq
    cat2prot[cat] = curr_cat_prot_dict


# Category: Pathways
current = 0
for cat,protfreq_dicts in cat2prot.items():
    current += 1; print(cat, ':', current, 'of', len(cat2prot), end='\r')
    for protein,freq in protfreq_dicts.items():
        for ind in range(0,len(pathways)):
            if(pathways['protein'][ind] == protein):
                cat2pathway[cat].append({pathways['name'][ind]: freq})
                
for cat,pw_dicts in cat2pathway.items():
    curr_cat_pw_dict = {}
    for pw_dict in pw_dicts:
        pw = list(pw_dict.keys())[0]
        freq = int(list(pw_dict.values())[0])
        if(pw not in curr_cat_pw_dict.keys()):
            curr_cat_pw_dict[pw] = 0
        curr_cat_pw_dict[pw] += freq
    cat2pw[cat] = curr_cat_pw_dict
    
# Sort the pathway dictionary by the most popular pathway in each disease
sorted_cat2pw = {}
for cat in cat2pw:
    sorted_cat2pw[cat] = sorted(cat2pw[cat].items() , reverse=True, key=lambda x: x[1])
#sorted_cat2pw


# Make dataframe ranking all pathways for each disease
top_pws = pd.DataFrame(columns = sorted_cat2pw.keys())
lengths = []
for cat in sorted_cat2pw: lengths.append(len(sorted_cat2pw[cat]))
max_cat = lengths.index(max(lengths))

for i in range(0,lengths[max_cat]):
    row = {}
    for cat in sorted_cat2pw:
        try: row.update({cat: sorted_cat2pw[cat][i][0]})
        except: row.update({'N/A':'N/A'})
    top_pws = top_pws.append(row, ignore_index=True)

top_pws.to_csv('Analyses/Top Entities, Top Pathways/Data/Popularity_Ranked_Pathways_in_Each_Category.csv')
#display(top_pws)
print('Made popularity-ranked pathways...')

# Make dataframe ranking all pathways for each disease
top_pws_counts = pd.DataFrame(columns = sorted_cat2pw.keys())
lengths = []
for cat in sorted_cat2pw: lengths.append(len(sorted_cat2pw[cat]))
max_cat = lengths.index(max(lengths))

for i in range(0,lengths[max_cat]):
    row = {}
    for cat in sorted_cat2pw:
        try: row.update({cat: float(sorted_cat2pw[cat][i][1])})
        except: row.update({'N/A':'N/A'})
    top_pws_counts = top_pws_counts.append(row, ignore_index=True)
    
#display(top_pws_counts.style.background_gradient(cmap ='Reds').set_properties(**{'font-size': '10px'}))

top_pws_counts.to_csv('Analyses/Top Entities, Top Pathways/Data/Popularity_Ranked_Pathway_Counts_in_Each_Category.csv')
print('Finished!')