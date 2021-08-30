Runner
- This is the main place to run all the steps in the CaseOLAP pipeline (including the modified steps such as removing text documents which are in multiple categories). Also, many downstream analyses can be run in this runner (analyses in the Analyses folder). That data is stored in the Analyses folder with notebook versions of the .py scripts run for the analyses too. 

All other files

- The other files are part of/are CaseOLAP. 

- The 'run_...' files are run in the runner and call on files in the 'caseolap' folder within this 'caseolap' folder. 

- The 'data' folder has output data produced by CaseOLAP, which is often used as input in the next steps. The pubmed.json folder should typically be in here, but for this project, a different path was used. If this analysis is rerun somewhere not in the original environment it was run (i.e. without access to the main pubmed.json file), all steps of the runner may have to be run. Alternatively, the 'not_full_text_pubmed.json' could be used. 

- The 'config' folder has files which configure CaseOLAP. One major modification here is in the 'index_init_config' file. This is changed so that the ElasticSearch database is not automatically made lowercase but instead preserves the case sensitivity of the words. This is compensated for by making entities (i.e. proteins) have another alternatve spelling with the first letter capitalized or lowercased when appropriate (e.g., not for acronyms).

- The 'ftp.ncbi.nlm.nih.gov' folder stores raw PubMed data

- The 'input' folder has the 'categories.txt' which are the MeSH tree numbers for each disease category. 