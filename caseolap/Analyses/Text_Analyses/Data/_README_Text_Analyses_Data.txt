1) pmidSizes.csv
A co-occurrence table of the combined number of documents in both categories on the column and row
This type of data was used in calculating proportions


2) pmidOverlaps.csv
The number of times that a disease pair is studied in the same publication
Note: This is not the same as the amount of documents. Some documents may study more than 2 diseases. For example, if a document studies disease A, B, and C, the counts will increment for 3 pair: AB, BC, AC


3) pmidProportions.csv
The proportion of the amount of times a pair of diseases appeared in a document divded by the number of documents in those disease categories.


4) diffdocs.csv
A table with the number of documents found with the row's disease (column 1), those documents which weren't studying any of the other diseases (column 2), and the proportion of col1/col2 (column 3)

5) pmidList.csv
A list of the PubMed IDs for all the documents considered/analyzed in this study.

6) usedpmidList.csv
A list of the PubMed IDs for all the documents containing our entity terms for this study. 