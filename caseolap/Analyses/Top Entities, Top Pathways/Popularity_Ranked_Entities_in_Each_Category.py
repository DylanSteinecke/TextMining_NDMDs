import pandas as pd
#from IPython.display import display

# Run in Runner
#Interchangeable with other types of entities, not just proteins. 
# Use the notebook to see a nicer display of the dataframes, particularly the heatmap


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
        
cat2entity = {}
cat2ent = {}

for cat,v in cat2pmid.items():
    cat2entity[cat] = []
    cat2ent[cat] = []

# Category: entitys
f_entitycount = open('./data/entitycount.txt')
for line in f_entitycount:
    pmid = line.split(' ')[0]
    entity_freq = line.split(' ')[1:]
    entity_list = []
    for ent in entity_freq:
        entity_list.append(ent.split('|'))
    
    for category,pmids in cat2pmid.items():
        if(pmid in cat2pmid[category]): 
            for entity in entity_list:
                cat2entity[category].append(entity)
    
for cat,ent_lists in cat2entity.items():
    curr_cat_ent_dict = {}
    for ent_list in ent_lists:
        entity = ent_list[0]
        freq = int(ent_list[1].split('\n')[0])
        if(entity not in curr_cat_ent_dict.keys()):
            curr_cat_ent_dict[entity] = 0
        curr_cat_ent_dict[entity] += freq
    cat2ent[cat] = curr_cat_ent_dict

# Sort the entity dictionary by the most popular entities in each disease
sorted_cat2ent = {}
for cat in cat2ent:
    sorted_cat2ent[cat] = sorted(cat2ent[cat].items() , reverse=True, key=lambda x: x[1])
#sorted_cat2ent

# Make dataframe ranking all entities for each disease
top_ents = pd.DataFrame(columns = sorted_cat2ent.keys())
lengths = []
for cat in sorted_cat2ent: lengths.append(len(sorted_cat2ent[cat]))
max_cat = lengths.index(max(lengths))

for i in range(0,lengths[max_cat]):
    row = {}
    for cat in sorted_cat2ent:
        try: row.update({cat: sorted_cat2ent[cat][i][0]})
        except: row.update({'N/A':'N/A'})
    top_ents = top_ents.append(row, ignore_index=True)
top_ents.to_csv('Analyses/Top Entities, Top Pathways/Data/Popularity_Ranked_Entities.csv')
#display(top_ents)
print('Made Top Entities...')

# Make dataframe ranking all entities' counts for each disease
top_counts = pd.DataFrame(columns = sorted_cat2ent.keys())
lengths = []
for cat in sorted_cat2ent: lengths.append(len(sorted_cat2ent[cat]))
max_cat = lengths.index(max(lengths))

for i in range(0,lengths[max_cat]):
    row = {}
    for cat in sorted_cat2ent:
        try: row.update({cat: float(sorted_cat2ent[cat][i][1])})
        except: row.update({'N/A':'N/A'})
    top_counts = top_counts.append(row, ignore_index=True)
top_counts.to_csv('Analyses/Top Entities, Top Pathways/Data/Popularity_Ranked_Entity_Counts.csv')
print('Made Top Counts...')
#display(top_counts)
#display(top_counts.style.background_gradient(cmap ='Reds').set_properties(**{'font-size': '10px'}))
print('Finished!')