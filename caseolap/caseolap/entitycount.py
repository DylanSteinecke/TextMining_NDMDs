import sys
import json
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from collections import Counter


"""
Entity Count Class
"""

class EntityCount(object):
    
    def __init__(self,):
        
        self.entity_dict = {}
        
    


    def entity_dictionary(self,input_file_user_entity_list,logfile):
        
        print("Entity dictionary is created.......")
        logfile.write("Entity dictionary is created....... \n")
        logfile.write("=========================================== \n")
        
        with open(input_file_user_entity_list, "r") as f_in:
            for line in f_in:
                # synonyms seperated by "|" and represented by the first one on each line
                line_split = line.strip().split("|")
                self.entity_dict[line_split[0]] = line_split
            
    
    def entity_count_dictionary(self,input_file_textcube_pmid2cell,logfile):
        
        print("Entity count dictionary is initiated.......")
        logfile.write("Entity count dictionary is initiated....... \n")
        logfile.write("==================================================== \n")
        
        with open(input_file_textcube_pmid2cell, "r") as f_in:
            self.pmid_and_cat = json.load(f_in)
        self.concerned_pmid_set = set(map(lambda x: x[0], self.pmid_and_cat))
        self.entity_count_per_pmid = {pmid: Counter() for pmid in self.concerned_pmid_set}
               
        
    def entity_search(self,logfile,key):    
        """
        Search and count entities: to optimize and find count from indexer
        """
        print("Entity count is running .....")
        logfile.write("Entity count is running ..... \n")
        logfile.write("============================================== \n")
        
        es = Elasticsearch(timeout=300)
        k = 0
        
        for entity_rep in self.entity_dict:
            print('entity_rep: ', entity_rep)
            for entity in self.entity_dict[entity_rep]:
                entity_space_sep = entity.replace("_", " ")
                if key == "abstract":
                    #Query to search through both abstract and full text
                    q = Q("match_phrase", abstract=entity_space_sep) 
                if key == "full_text":
                    q = Q("match_phrase", abstract=entity_space_sep) | \
                            Q("match_phrase", full_text=entity_space_sep)
                if key == "all":
                    q = Q("match_phrase", title=entity_space_sep) | \
                        Q("match_phrase", abstract=entity_space_sep) | \
                        Q("match_phrase", full_text=entity_space_sep)

               
                s = Search(using=es, index="nd_mito2")\
                            .params(request_timeout=300)\
                            .query(q) 
                              
                num_hits = 0
                num_valid_hits = 0
                num_counts = 0

                for hit in s.scan():
                    num_hits += 1
                    cur_pmid = str(hit.pmid)

                    if cur_pmid not in self.concerned_pmid_set:
                        continue

                    if key == "abstract":
                        abst = hit.abstract
                        entity = entity_space_sep
                        entity_cnt = abst.count(entity)
                        
                    if key == "full_text":
                        abst = hit.abstract
                        full_text = hit.full_text
                        entity = entity_space_sep
                        entity_cnt = abst.count(entity) + full_text.count(entity)
                        
                    if key == "all":
                        try: 
                            abst = hit.abstract
                        except:
                            abst = 'beep'
                        try: 
                            full_text = hit.full_text
                        except:
                            full_text = 'beep'
                        try: 
                            title = hit.title
                        except:
                            title = 'beep'
                        try: 
                            entity1 = entity_space_sep
                        except:
                            entity1 = ' '
                        if(type(title) == str):
                            entity_cnt = abst.count(entity1) + \
                            full_text.count(entity1) + \
                            title.count(entity1)
                        else:
                            entity_cnt = abst.count(entity1) + \
                            full_text.count(entity1)
                        #print('title', title)
                        #print('abstract', abst)
                        #print('full_text', full_text)

                    if entity_cnt == 0:
                        continue

                    else:
                        self.entity_count_per_pmid[cur_pmid][entity_rep] += entity_cnt
                        num_valid_hits += 1
                        num_counts += entity_cnt

                        logfile.write('entity_rep ' + entity_rep + ': '  + str(entity1) + " #hits:" +  str(num_hits)+\
                                            " #valid hits:" + str(num_valid_hits) +\
                                            " #counts:"+ str(num_counts))
                        logfile.write("\n")
                
                
            k = k +1
            if k%100 == 0:
                print(k,'entity successfully counted!')
                logfile.write(str(k) + "entity successfully counted!")
                logfile.write("\n")        
    
    
    def entity_count_output(self,output_file_entity_count,output_file_entityfound_pmid2cell,logfile):
        
        '''
        paper entity count & paper category
        '''
        
        print("Entity count output is being saved...")
        logfile.write("Entity count outpput is being saved...")
        logfile.write("\n")
        
        with open(output_file_entity_count, "w") as f_entity,\
                open(output_file_entityfound_pmid2cell , "w") as f_pmid2cell:

            f_pmid2cell.write("doc_id\tlabel_id\n")

            paper_new_id = 1

            for cur_pmid,cur_cat in self.pmid_and_cat:

                if len(self.entity_count_per_pmid[cur_pmid]) == 0:
                    continue


                '''
                print paper category
                '''
                f_pmid2cell.write(str(cur_pmid) + "\t" + str(cur_cat) + "\n")


                '''
                print paper entity count
                '''
                f_entity.write(str(cur_pmid))


                for entity in self.entity_count_per_pmid[cur_pmid]:
                    f_entity.write(" " + entity +"|" + str(self.entity_count_per_pmid[cur_pmid][entity]))


                f_entity.write("\n")


            paper_new_id += 1

        
