
import time
import re
import sys
import os
import json
from collections import defaultdict
from elasticsearch import Elasticsearch


from caseolap.index_populate import *




'''
Input data files
'''
inputFilePath = "../../../../caseolap/data/pubmed.json"
index_populate_config_file = "./config/index_populate_config.json"

'''
Out datafile
'''
logFilePath = "./log/indexing_log.txt"

'''
Index parameter
'''
    
INDEX_NAME = "nd_mito2"
TYPE_NAME = "nd_mito_meta2"


'''
Start poputating index
'''
    
if __name__ == '__main__':

    logfile = open(logFilePath, "w")
    
    with open(index_populate_config_file,'r') as f:
        index_populate_config = json.load(f) 


    '''
    Populate the index with provided indexing configuration 
    '''
    populate_index(inputFilePath,\
                   logfile,\
                   INDEX_NAME,\
                   TYPE_NAME,\
                   index_populate_config)

    logfile.close()

    
    
    
    
