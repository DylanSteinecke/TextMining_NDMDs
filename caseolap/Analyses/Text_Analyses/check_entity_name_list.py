MC_HUP = {}
f = open("../UniProt API/MitoCartaAndHumanUPOnlyProteins.txt", "r")
for line in f:
    l = line.strip().split('|')
    MC_HUP[l[0]] = l
f.close()

MC_HUP_NHUP = {}
f = open("../UniProt API/MitoProteins.txt", "r")
for line in f:
    l = line.strip().split('|')
    MC_HUP_NHUP[l[0]] = l
f.close()

for ID,names in MC_HUP.items():
    for name in names:
        if(name not in MC_HUP_NHUP[ID]):
            print(ID, '|', name, '|', MC_HUP_NHUP[ID])
print('Done checking (if there were no issues, nothing else should be printed here)')