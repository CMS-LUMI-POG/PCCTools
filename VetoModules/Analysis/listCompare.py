#########################
#Author: Sam Higginbotham
'''

* File Name : listCompare.py

* Purpose :

* Creation Date : 30-08-2018

* Last Modified :

'''
#########################
file18MV=open("backup2018MV.txt","r")
file17MV=open("vetoModules_2017.txt","r")
fileML=open("2017moduleList.txt","r")
list18MV=[]
list17MV=[]
listML=[]
for line  in file18MV:
    list18MV.append(int(line))

for line  in file17MV:
    list17MV.append(int(line))

for line  in fileML:
    listML.append(int(line))

set18MV=set(list18MV)
set18MV=set(list17MV)
set18MV=set(list18MV)
set17MV=set(list17MV)
setML=set(listML)
len(set18MV&set17MV)

len(set18MV&setML)

len(set18MV)
