import os
import shutil
import csv
from difflib import SequenceMatcher
import jellyfish
import string
import difflib
import re
from jiwer import wer
import math
import re
from collections import Counter

#Copy audio from testfolder to input
dir_path = os.path.dirname(os.path.realpath(__file__))
shutil.rmtree(dir_path+'/InputAudioData')
os.makedirs(dir_path+'/InputAudioData')

for folder in os.listdir(dir_path+'/testIpa/input'):
    for file in os.listdir(dir_path+'/testIpa/input/'+folder):
        if file[-4:] != '.txt':
            shutil.copy(dir_path+'/testIpa/input/'+folder+'/'+file, dir_path+'/InputAudioData')


with open("speechProcess.py") as f:
    exec(f.read())

# Compress results
shutil.rmtree(dir_path+'/testIpa/results/')
os.makedirs(dir_path+'/testIpa/results/')

for folder in os.listdir(dir_path+'/output'):
    os.makedirs(dir_path+'/testIpa/results/'+folder)
    f = open(dir_path+'/testIpa/results/'+folder+"/transcipt.txt", "x")
    f.close
    ls = os.listdir(dir_path+'/output/'+folder+'/')
    ls.sort() 
    for output in ls:
        test_path = dir_path+'/output/'+folder+'/'+output
        if os.path.isdir(test_path):
            with open(test_path + "/Alosourus_noTime.txt" ,'r') as read:
                with open(dir_path+'/testIpa/results/'+folder+"/transcipt.txt", "a+") as store:
                    for line in read.readlines():
                        line = line.replace("  ", ' ')
                        store.write(line)



# field names 
fields = ['FileName', 'WER', 'NO. of  expected chars','NO. of actual chars', 'NO. Added chars', 'NO. Missing chars', 'levenshtein Distance','Proportional Lev'] 

#analyses and output data
actStats = "actaulStates.csv"
tranStats = "transcioptionStates.csv"
with open(dir_path+'/testIpa/'+actStats , 'w') as file:
    csvwriter = csv.writer(file)         
    # writing the fields 
    csvwriter.writerow(fields)

with open(dir_path+'/testIpa/'+tranStats , 'w') as file:
    csvwriter = csv.writer(file)         
    # writing the fields 
    csvwriter.writerow(fields)
   
for folder in os.listdir(dir_path+'/testIpa/results'):
    act =''
    tran = ''
    calc = ''
    with open(dir_path+'/testIpa/input/'+folder+'/actual.txt' , 'r') as r:
        for line in r.readlines():
            act+= line
    with open(dir_path+'/testIpa/input/'+folder+'/transcipt.txt' , 'r') as r:
        for line in r.readlines():
            tran+= line
    with open(dir_path+'/testIpa/results/'+folder+'/transcipt.txt' , 'r') as r:
        for line in r.readlines():
            calc+= line

    # data rows of csv file 
    actRows = [ ] 
    transRows = [ ]
  

    act = act.replace("  ",' ')
    tran = tran.replace("  ",' ')
    actChars = len(act.split())
    transChars = len(tran.split())
    calcChars = len(calc.split())

    actDict = {}
    transDict = {}
    calcDict = {}
    lis = [actDict , transDict , calcDict]
    text = [act, tran , calc]
    count = 0
    for l in lis:
        for word in text[count].split(): 
            if not word in l:
                l[word] = 1
            else:
                l[word] += 1
        count+=1

    chars = [[0,0],[0,0]]

    lis2= [actDict , transDict]
    count = 0
    for l in lis2:
        noAddedWords = 0
        noMissingWords = 0
        for word in calcDict:
            if not word in l:
                noAddedWords += calcDict[word]
            else:
                if (calcDict[word] - l[word])>0:
                    noAddedWords += calcDict[word] - l[word]
                else:
                    noMissingWords -= calcDict[word] - l[word]


        for word in l:
            if not word in calcDict:
                noMissingWords += l[word]
        chars[count][0]=noAddedWords
        chars[count][1] = noMissingWords
        count+=1

    WER = wer(act, calc)
    WER2 = wer(tran, calc)

    lev_dist = jellyfish.levenshtein_distance(act, calc)
    lev_dist2 = jellyfish.levenshtein_distance(tran, calc)

    with open(dir_path+'/testIpa/'+actStats, '+a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow([folder ,WER , actChars, calcChars, str(chars[0][0]),str(chars[0][1]),lev_dist,str(lev_dist/actChars) ])
    with open(dir_path+'/testIpa/'+tranStats, '+a') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerow([folder ,WER2 , transChars, calcChars, chars[1][0],chars[1][1],lev_dist2 ,str(lev_dist2/actChars)])




           