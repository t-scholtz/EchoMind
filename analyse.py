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

import time

WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def tokenize(s):
    return re.split('\s+', s)
def untokenize(ts):
    return ' '.join(ts)
        
def equalize(s1, s2):
    l1 = tokenize(s1)
    l2 = tokenize(s2)
    res1 = []
    res2 = []
    prev = difflib.Match(0,0,0)
    for match in difflib.SequenceMatcher(a=l1, b=l2).get_matching_blocks():
        if (prev.a + prev.size != match.a):
            for i in range(prev.a + prev.size, match.a):
                res2 += ["["+(l1[i])+"]"]
            res1 += l1[prev.a + prev.size:match.a]
        if (prev.b + prev.size != match.b):
            for i in range(prev.b + prev.size, match.b):
                res1 += ["["+(l2[i])+"]"]
            res2 += l2[prev.b + prev.size:match.b]
        res1 += l1[match.a:match.a+match.size]
        res2 += l2[match.b:match.b+match.size]
        prev = match
    return untokenize(res1), untokenize(res2)

def jaccard_similarity(x,y):
  """ returns the jaccard similarity between two lists """
  intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
  union_cardinality = len(set.union(*[set(x), set(y)]))
  return intersection_cardinality/float(union_cardinality)

#Copy audio from testfolder to input
dir_path = os.path.dirname(os.path.realpath(__file__))
shutil.rmtree(dir_path+'/InputAudioData')
os.makedirs(dir_path+'/InputAudioData')
 

for folder in os.listdir(dir_path+'/testData/input'):
    for file in os.listdir(dir_path+'/testData/input/'+folder):
        if file != 'text.txt':
            shutil.copy(dir_path+'/testData/input/'+folder+'/'+file, dir_path+'/InputAudioData')
#Run tests
with open("speechProcess.py") as f:
    exec(f.read())

# Compress results
shutil.rmtree(dir_path+'/testData/results/')
os.makedirs(dir_path+'/testData/results/')
for folder in os.listdir(dir_path+'/output'):
    os.makedirs(dir_path+'/testData/results/'+folder)
    f = open(dir_path+'/testData/results/'+folder+"/cmu.txt", "x")
    f.close
    f = open(dir_path+'/testData/results/'+folder+"/whisper.txt", "x")
    f.close
    f = open(dir_path+'/testData/results/'+folder+"/vosk.txt", "x")
    f.close
    ls = os.listdir(dir_path+'/output/'+folder+'/')
    ls.sort() 
    for output in ls:
        test_path = dir_path+'/output/'+folder+'/'+output
        if os.path.isdir(test_path):
            with open(test_path + "/Whisper_transcipt.txt" ,'r') as read:
                with open(dir_path+'/testData/results/'+folder+"/whisper.txt", "a+") as store:
                    for line in read.readlines():
                        store.write(line+"\n")
            with open(test_path + "/vosk_transcipt.txt" ,'r') as read:
                with open(dir_path+'/testData/results/'+folder+"/vosk.txt", "a+") as store:
                    for line in read.readlines():
                        store.write(line+"\n")
            with open(test_path + "/Cmu_transcipt.txt" ,'r') as read:
                with open(dir_path+'/testData/results/'+folder+"/cmu.txt", "a+") as store:
                    for line in read.readlines():
                        line = re.sub(r"<.*?>" , "", line)
                        line = re.sub(r"\(.*?\)", '', line)
                        line = re.sub(r"\[.*?\]", '', line)
                        store.write(line+"\n")


# field names 
fields = ['FileName', 'WER', 'NO. of words', 'NO. Added Words', 'NO. Missing Words', 'levenshtein Distance', 'Jacard Distance', 'Cosine similarity'] 

#analyses and output data
filename = "STT_Metrics.csv"
filename2 = "STT_Differences.txt"
with open(dir_path+'/testData/whisperOutput.csv' , 'w') as file:
    csvwriter = csv.writer(file)         
    # writing the fields 
    csvwriter.writerow(fields)
   
for folder in os.listdir(dir_path+'/testData/results'):
    # shutil.copy(, dir_path+'/testData/results/'+folder)
    comp = ''
    with open(dir_path+'/testData/input/'+folder+'/text.txt' , 'r') as r:
        for line in r.readlines():
            comp+= line+" "
    comp = ((comp).lower()).translate(str.maketrans('', '', string.punctuation)).strip()
    comp = comp.replace('\n','')
    comp = comp.replace('\t','')

    # data rows of csv file 
    rows = [ ] 
    rows2 = [ ]
    rows2.append("Original -" +"\n"+comp+"\n")

    files = os.listdir(dir_path+'/testData/results/'+folder)
    for file in files:
        text = ""
        transcript = comp

        #read transcipt, and format to plain text
        with open(dir_path+'/testData/results/'+folder+"/"+file , 'r') as test:
            lines = test.readlines()
            text = ""
            for line in lines:
                text += line+" "
            text = ((text).lower()).translate(str.maketrans('', '', string.punctuation)).strip()


        noWords = len(text.split())

        transDict = {}
        textDict = {}
        for word in transcript.split(): 
            if not word in transDict:
                transDict[word] = 1
            else:
                transDict[word] += 1

        for word in text.split(): 
            if not word in textDict:
                textDict[word] = 1
            else:
                textDict[word] += 1

        noAddedWords = 0
        noMissingWords = 0
        for word in transDict:
            if not word in textDict:
                noAddedWords += transDict[word]
            else:
                if (transDict[word] - textDict[word])>0:
                    noAddedWords += transDict[word] - textDict[word]
                else:
                    noMissingWords -= transDict[word] - textDict[word]

        for word in textDict:
            if not word in transDict:
                noMissingWords += textDict[word]

        lev_dist = jellyfish.levenshtein_distance(text, comp)
        vector1 = text_to_vector(text)
        vector2 = text_to_vector(comp)

        cosine = get_cosine(vector1, vector2)
        
        WER = wer(comp, text)
        jac = jaccard_similarity(text.split(), transcript.split())
        out = [file ,WER, noWords, noAddedWords, noMissingWords, lev_dist,jac,cosine]
        rows.append(out)
    
        #Creates a visual output of differences
        eq = equalize(text, transcript)
        rows2.append("_"*100 +"\n")

        rows2.append(file +" - " +"\n"+ eq[0]+ "\n")
        print(file)
        if(file == "whisper.txt"):
            with open(dir_path+'/testData/whisperOutput.csv' , 'a+') as file:
                csvwriter = csv.writer(file)         
                # writing the fields 
                csvwriter.writerow([folder, WER, noWords, noAddedWords, noMissingWords, lev_dist,jac,cosine])


    with open(dir_path+'/testData/results/'+folder+"/"+filename, 'w') as csvfile: 
        # creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # writing the fields 
        csvwriter.writerow(fields) 
            
        # writing the data rows 
        csvwriter.writerows(rows)

    with open(dir_path+'/testData/results/'+folder+"/"+filename2, 'w') as text: 
        for line in rows2:
            text.write(line)
    




