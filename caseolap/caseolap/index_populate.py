
import time
import re
import sys
import os
import json
from collections import defaultdict
from elasticsearch import Elasticsearch


def populate_index(inputFilePath,logfile,INDEX_NAME,TYPE_NAME,index_populate_config):
    
    es = Elasticsearch()

    ic = 0
    ir = 0
    
    relevant_mesh = []
    with open('./data/meshterms_per_cat.json', 'r') as j:
        relevant_meshJSON = json.load(j)
    for cat in relevant_meshJSON:
        for name in cat:
            relevant_mesh.append(name)
    len_relevant_mesh = len(relevant_mesh)
    print(relevant_mesh)
    
    with open(inputFilePath, "r") as fin: 
        
            start = time.time()     
            bulk_size = 500             #number of document processed in each bulk index
            bulk_data = []              #data in bulk index

            cnt = 0
            subsample_count = 0
           
            print('Starting...')
            totcount = 0
            
            for line in fin:               #each line is single document

                proceed = False
                paperInfo = json.loads(line.strip())
                totcount += 1                
                if(totcount % 10000 == 0):
                    print('Total Count: ', totcount, 'Relevant Doc Counts: ', cnt, end = '\r')

                    
                mesh_list = paperInfo['MeshHeadingList'] #Checking if document is relevant
                for i in range(0,len_relevant_mesh):
                    if(relevant_mesh[i] in mesh_list):
                        proceed = True
                        
                if(proceed == True):
                    cnt += 1
                    data_dict = {}
   
                    data_dict["pmid"] = paperInfo.get("PMID", "-1")
                    data_dict["title"] = paperInfo.get("ArticleTitle")
                    data_dict["abstract"] = paperInfo.get("Abstract", "")
                    data_dict["full_text"] = paperInfo["full_text"]

                
                    if index_populate_config['date']:
                        data_dict["date"] = str(paperInfo['PubDate'])
                        
                        '''
                        Update MeSH
                        '''
                    if index_populate_config['MeSH']:
                        data_dict["MeSH"] = paperInfo['MeshHeadingList']
                        
                        '''
                        Update location
                        '''  
                    if index_populate_config['location']:
                        data_dict["location"] = paperInfo['Country']
                        
                        '''
                        Update Author
                        ''' 
                    if index_populate_config['author']:
                        data_dict["author"] = paperInfo['AuthorList']
                        
                        '''
                        Update Journal
                        '''
                    if index_populate_config['journal']:
                        data_dict["journal"] = paperInfo['Journal']
                        

                    '''
                    Put current data into the bulk 
                    '''
                    op_dict = {
                        "index": {
                         "_index": INDEX_NAME,
                         "_type": TYPE_NAME,
                         "_id": data_dict["pmid"]
                            }
                        }

                    bulk_data.append(op_dict)
                    bulk_data.append(data_dict) 

                    subsample_count += 1

                    if cnt % bulk_size == 0 and cnt != 0:
                        ic += 1
                        tmp = time.time()
                        es.bulk(index=INDEX_NAME,\
                                body=bulk_data,\
                                request_timeout = 2000)

                        logfile.write("bulk indexing... %s, %s, escaped time %s (seconds) \n" % ( cnt, subsample_count, tmp - start ) )
                        if ic%100 ==0:
                            print(" i bulk indexing... %s, %s, escaped time %s (seconds) " % ( cnt, subsample_count, tmp - start ) )

                        bulk_data = []


            '''
            indexing those left papers
            '''
            if bulk_data:
                ir +=1
                tmp = time.time()
                es.bulk(index=INDEX_NAME, body=bulk_data, request_timeout = 500)

                logfile.write("bulk indexing... %s, escaped time %s (seconds) \n" % ( cnt, tmp - start ) )
                if ir%100 ==0:
                    print(" r bulk indexing... %s, escaped time %s (seconds) " % ( cnt, tmp - start ) )

                bulk_data = []




            end = time.time()
            logfile.write("Finish PubMed meta-data indexing. Total escaped time %s (seconds) \n" % (end - start) )
            print("Finish PubMed meta-data indexing. Total escaped time %s (seconds) " % (end - start) )
               


                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                