# CaseOLAP :

CaseOLAP is a cloud computing platform for phrase-mining. specifically, for user-defined entity-category association. It has five major steps; 'downloading', 'parsing', 'indexing', 'entity count' and 'CaseOLAP score calculation'. There are mltiple steps in a single major step, which are based on user's interest in entity list and categories as well as data set being used. This pipeline describes these major steps for PubMed abstracts as text data, the mitochondrial proteins as entity list, and MeSH descriptors attached to abstracts as categories.

### Publication: 
1. [Cloud-Based Phrase Mining and Analysis of User-Defined Phrase-Category Association in Biomedical Publications](https://www.jove.com/video/59108/cloud-based-phrase-mining-analysis-user-defined-phrase-category)
2. [Phrase mining of textual data to analyze extracellular matrix protein patterns across cardiovascular disease](https://www.physiology.org/doi/full/10.1152/ajpheart.00175.2018)


***1. Setting up Python Environment*** : 

Install Anconda python and git in the Unix system. Creat the 'caseolap' python environment.

```
conda env create -f environment.yaml
```
---------------------------
***2. Download Documents*** : 

Set up the FTP data address at 'config/ftp_config.json' and select 'baseline' or 'updatefiles' in 'config/download_config.json'. This will download the data file from source to the cloud storage, check the integrity of download data, and extract them.

```
python run_download.py
```
-------------------------------

***3. Parsing Documents*** : 
Set up the parameters for parsing at 'config/parsing_config.json'. Based on the items selected. Parsed data for each document becomes available as JSON dictionary.
```
python run_parsing.py
```
---------------------------
***4. MeSH to PMID Mapping***

Create a mapping table for each MeSH term. There are multiple MeSH attached to a single document.

```
python run_mesh2pmid_mapping.py

```
---------------------------
***5. Document Indexing***
Create a Elasticsearch indexing database for parsed documents. To initiate the index select the parameters in 'config/indrx_init.json' and to populate the index, select parameters at 'config/index_populate.json'.

```
python run_index_init.py
python run_populate_init.py
```
---------------------------
***6. Text-Cube Creation***: 

 Create a user-defined categories at 'input/categories.txt'. Create a data-cube for text data (i.e. a text-cube) for making text-data more functional for information extraction and manipulation.
 
```
python run_textcube.py
```
---------------------------
***7. Entity Count***
Create a user-defined entities in 'input/entities.txt'. Use Elasticsearch indexing database to search and count entities and documents including such entities.

```
python run_entitycount.py
```
---------------------------
***8. Metadata Update***

Update the metadata for Textcube from entity-count result.

```
python run_metadata_update.py

```
---------------------------
***9. CaseOLAP score Calculation***

Create the CaseOLAP score based on entity count and document count data using ```Integrity```, ```Popularity``` and ```Distintiveness```.

```
python run_caseolap_score.py
```



***Additional Notes***
Runner
- This is the main place to run all the steps in the CaseOLAP pipeline (including the modified steps such as removing text documents which are in multiple categories). Also, many downstream analyses can be run in this runner (analyses in the Analyses folder). That data is stored in the Analyses folder with notebook versions of the .py scripts run for the analyses too. 

All other files

- The other files are part of/are CaseOLAP. 

- The 'run_...' files are run in the runner and call on files in the 'caseolap' folder within this 'caseolap' folder. 

- The 'data' folder has output data produced by CaseOLAP, which is often used as input in the next steps. The pubmed.json folder should typically be in here, but for this project, a different path was used. If this analysis is rerun somewhere not in the original environment it was run (i.e. without access to the main pubmed.json file), all steps of the runner may have to be run. Alternatively, the 'not_full_text_pubmed.json' could be used. 

- The 'config' folder has files which configure CaseOLAP. One major modification here is in the 'index_init_config' file. This is changed so that the ElasticSearch database is not automatically made lowercase but instead preserves the case sensitivity of the words. This is compensated for by making entities (i.e. proteins) have another alternatve spelling with the first letter capitalized or lowercased when appropriate (e.g., not for acronyms).

- The 'ftp.ncbi.nlm.nih.gov' folder stores raw PubMed data

- The 'input' folder has the 'categories.txt' which are the MeSH tree numbers for each disease category. 




