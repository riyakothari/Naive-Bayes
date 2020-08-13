# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 16:21:25 2020

@author: riyak
"""
import sys
import os
import time
import math
start_time = time.time()
spamWordCount = 0
spamFileCount = 0
hamWordCount = 0
hamFileCount = 0
commonWords = {'a':0, 'the':0, 'to':0, 'of':0, 'on':0, 'in':0, 'an':0, 'am':0, 'at':0, 'for':0, 'this':0, 'that':0, 
               'so':0, 'has':0, 'have':0, 'had':0, 'them':0, 'they':0, 'it':0, 'be':0, 'is':0, 'or':0, 'we':0,
               '?':0, '.':0, ':':0, ',':0, '-':0, '#':0, 'and':0, '/':0, '%':0, 'i':0, 'my':0, 'with':0, 'as':0,
               'then':0, 'than':0, 'can':0, 'he':0, 'she':0, 'will':0 } #for enhancement
def readModelFile(inputFilePath):
    global spamFileCount, spamWordCount, hamFileCount, hamWordCount
    model = open("nbmodel.txt", "r", encoding="latin1")
    path = model.readline().strip().split(" ")[-1]
    vocabSize = int(model.readline().strip().split(" ")[-1])
    spamWordCount = model.readline().strip().split(" ")[-1]
    spamFileCount = model.readline().strip().split(" ")[-1]
    hamWordCount = model.readline().strip().split(" ")[-1]
    hamFileCount = model.readline().strip().split(" ")[-1]
    x = model.readline().strip().split(" ")
#    print(x)
#    print(vocabSize)
    if x[0].lower() == "dictham" and len(x)==1:
        givenHamDict = {}
    count=0
    for i in range(vocabSize):
        count+=1
        x = model.readline().strip().split(" ")
    #    print(x)
    #    print(count)
        if len(x)!=2:
            continue
        word, prob = x
        givenHamDict[word.lower()] = prob
        
    x = model.readline().strip().split(" ")
#    print(x, "nkjj")
    if x[0].lower() == "dictspam" and len(x)==1:
#        print("heya")
        givenSpamDict = {}
    for i in range(vocabSize):
        count+=1
        x = model.readline().strip().split(" ")
    #    print(x)
    #    print(count)
        if len(x)!=2:
            continue
        word, prob = x
        givenSpamDict[word.lower()] = prob
#    print("yahan") 
    model.close()
    predictLabel(path, givenHamDict, givenSpamDict, vocabSize, inputFilePath)

def predictLabel(givenpath, givenHamDict, givenSpamDict, vocabSize, inputFilePath):
#    print("ab yahan")
    output = open("nboutput.txt", "w+", encoding="latin1")
    
    
    for root, dirs, files in os.walk(inputFilePath):
#        print(root)
#        print(dirs)
        for file in files:
            if file.endswith(".txt"):
                wordDict = {}
                with open(os.path.join(root,file), "r", encoding="latin1") as f:
                    for line in f:
                        wordList = line.strip().split(" ")
                        for w in wordList:
                            w = str(w.lower())
                            if w in commonWords: #improvement code line 79-80
                                continue
                            if w not in givenSpamDict:
                                continue
                            if w not in wordDict:
                                wordDict[w] = 1
                            else:
                                wordDict[w] += 1
                pSpam = 1               
                pHam = 1
                pSpamLog = 0
                pHamLog = 0
                for j in wordDict:
                    if j not in givenSpamDict:
                        continue
                    #print(givenSpamDict[j])
                    pSpam *= float(givenSpamDict[j])
                    pHam *= float(givenHamDict[j])
                    pSpamLog += (math.log(float(givenSpamDict[j])) * wordDict[j])
                    pHamLog += (math.log(float(givenHamDict[j])) * wordDict[j])
                if pSpamLog>=pHamLog: #pSpam>=pHam:
                    output.write("spam\t"+os.path.join(root,file)+"\n")
                else:
                    output.write("ham\t"+os.path.join(root,file)+"\n")
                        
    output.close()
#    print(vocabSize, spamFileCount, spamWordCount, hamFileCount, hamWordCount)
#    print(len(givenHamDict), len(givenSpamDict))
#model.close()


if __name__ == '__main__':
    inputPath = sys.argv[1]
    readModelFile(inputPath)
#print(time.time() - start_time)