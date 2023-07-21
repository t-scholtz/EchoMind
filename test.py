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
from collections import Counter

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
    prev = difflib.Match(0, 0, 0)
    for match in difflib.SequenceMatcher(a=l1, b=l2).get_matching_blocks():
        if prev.a + prev.size != match.a:
            for i in range(prev.a + prev.size, match.a):
                res2 += ["[" + (l1[i]) + "]"]
            res1 += l1[prev.a + prev.size:match.a]
        if prev.b + prev.size != match.b:
            for i in range(prev.b + prev.size, match.b):
                res1 += ["[" + (l2[i]) + "]"]
            res2 += l2[prev.b + prev.size:match.b]
        res1 += l1[match.a:match.a + match.size]
        res2 += l2[match.b:match.b + match.size]
        prev = match
    return untokenize(res1), untokenize(res2)

def jaccard_similarity(x, y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)

# Copy audio from testfolder to input
dir_path = os.path.dirname(os.path.realpath(__file__))
shutil.rmtree(dir_path + '/InputAudioData')
os.makedirs(dir_path + '/InputAudioData')

for folder in os.listdir(dir_path + '/testData/input'):
    for file in os.listdir(dir_path + '/testData/input/' + folder):
        if file != 'text.txt':
            shutil.copy(dir_path + '/testData/input/' + folder + '/' + file, dir_path + '/InputAudioData')

# Run tests
with open("speechProcess.py") as f:
    exec(f.read())

# field names
fields = [
    'FileName', 'WER', 'NO. of words', 'NO. Added Words', 'NO. Missing Words',
    'levenshtein Distance', 'Jacard Distance', 'Cosine similarity'
]

# Compress results
shutil.rmtree(dir_path + '/testData/results/')
rFile = [
    "/Whisper_transcipt.txt", "/vosk_transcipt.txt", #"/Cmu_transcipt.txt",
    "/Espnet_transcipt.txt", "/combined.txt"
]
store = ["/whisper.txt", "/vosk.txt", #"/cmu.txt", 
         "/espnet.txt", "/combined.txt"]
os.makedirs(dir_path + '/testData/results/')
for folder in os.listdir(dir_path + '/output'):
    os.makedirs(dir_path + '/testData/results/' + folder)
    for file in store:
        with open(dir_path + '/testData/results/' + folder + file, "x"):
            pass
        with open(dir_path + '/testData' + file[:-4] + '.csv', 'w') as c:
            csvwriter = csv.writer(c)
            csvwriter.writerow(fields)

    ls = os.listdir(dir_path + '/output/' + folder + '/')
    ls.sort()
    for output in ls:
        test_path = dir_path + '/output/' + folder + '/' + output
        if os.path.isdir(test_path):
            for i in range(len(rFile)):
                pwd = test_path + rFile[i]
                with open(pwd, 'r') as read:
                    with open(dir_path + '/testData/results/' + folder + store[i], 'a+') as s:
                        for line in read.readlines():
                            line = re.sub(r"<.*?>", "", line)
                            line = re.sub(r"\(.*?\)", '', line)
                            line = re.sub(r"\[.*?\]", '', line)
                            line = (line.translate(str.maketrans('', '', string.punctuation))).lower()
                            line = line.replace("\n", " ")
                            line = line.replace("  ", " ")
                            s.write(line + " ")

# Analyses and output data
filename = "STT_Metrics.csv"
filename2 = "STT_Differences.txt"
for folder in os.listdir(dir_path + '/testData/results'):
    comp = ''
    with open(dir_path + '/testData/input/' + folder + '/text.txt', 'r') as r:
        comp = r.read().lower().translate(str.maketrans('', '', string.punctuation)).strip().replace('\n', ' ')
    # Data rows of csv file
    rows = []
    rows2 = ["Original -\n" + comp + "\n"]

    files = os.listdir(dir_path + '/testData/results/' + folder)
    for file in files:
        text = ""
        transcript = comp

        # Read transcript and format to plain text
        with open(dir_path + '/testData/results/' + folder + "/" + file, 'r') as test:
            text = test.read().lower().translate(str.maketrans('', '', string.punctuation)).strip()

        noWords = len(text.split())

        transDict = Counter(transcript.split())
        textDict = Counter(text.split())

        noAddedWords = sum((transDict - textDict).values())
        noMissingWords = sum((textDict - transDict).values())

        lev_dist = jellyfish.levenshtein_distance(text, comp)
        vector1 = text_to_vector(text)
        vector2 = text_to_vector(comp)
        cosine = get_cosine(vector1, vector2)
        WER = wer(comp, text)
        jac = jaccard_similarity(text.split(), transcript.split())
        out = [file, WER, noWords, noAddedWords, noMissingWords, lev_dist, jac, cosine]
        rows.append(out)

        # Create a visual output of differences
        eq = equalize(text, transcript)
        rows2.extend(["_" * 100 + "\n", file + " -\n" + eq[0] + "\n"])

        with open(dir_path + '/testData/' + file[:-4] + '.csv', 'a') as cv:
            csvwriter = csv.writer(cv)
            csvwriter.writerow(
                [folder, WER, noWords, noAddedWords, noMissingWords, lev_dist, jac, cosine]
            )

    with open(dir_path + '/testData/results/' + folder + "/" + filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)
        csvwriter.writerows(rows)

    with open(dir_path + '/testData/results/' + folder + "/" + filename2, 'w') as text:
        text.writelines(rows2)

    # Append data to combined.csv
    # with open(dir_path + '/testData/results/' + folder + "/combined.csv", 'a') as combined_file:
    #     csvwriter = csv.writer(combined_file)
    #     csvwriter.writerows(rows)
