# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 12:06:44 2020

@author: riyak
"""
import sys
import os
import time

#directoryPath = "Spam or Ham/train"
#directoryPath = sys.argv[1]
#subDirectoryList = os.listdir(directoryPath)
spamFileCount = 0
hamFileCount = 0
spamWordCount = 0
hamWordCount = 0
spamDict = {}
hamDict = {}
start_time = time.time()
vocabulary = {}
commonWords = {'a':0, 'the':0, 'to':0, 'of':0, 'on':0, 'in':0, 'an':0, 'am':0, 'at':0, 'for':0, 'this':0, 'that':0, 
               'so':0, 'has':0, 'have':0, 'had':0, 'them':0, 'they':0, 'it':0, 'be':0, 'is':0, 'or':0, 'we':0,
               '?':0, '.':0, ':':0, ',':0, '-':0, '#':0, 'and':0, '/':0, '%':0, 'i':0, 'my':0, 'with':0, 'as':0,
               'then':0, 'than':0, 'can':0, 'he':0, 'she':0, 'will':0 } #for enhancement
def fileParser(Path, category):
    #fileList = os.listdir(Path)
    global spamWordCount, spamDict, spamFileCount, hamWordCount, hamDict, hamFileCount
    if category=='ham':
        hamFileCount+=1
        with open(Path, "r",  encoding="latin1") as f:
            for line in f:
                wordList = line.strip().split(" ")
                for w in wordList:
                    w = str(w).lower()
                    if w in commonWords: #improvement code line 36-37
                        continue 
                    if not hamDict.get(w):
                        hamDict[w] = 1
                    else:
                        hamDict[w] += 1
                    if not spamDict.get(w): # w not in spamDict:
                        spamDict[w] = 0
                    if w not in vocabulary:
                        vocabulary[w] = 1
                    hamWordCount += 1
                            
    elif category=='spam':
        spamFileCount += 1
        with open(Path, "r",  encoding="latin1") as f:
            for line in f:
                wordList = line.strip().split(" ")
                for w in wordList:
                    w = str(w).lower()
                    if w in commonWords: #improvement code line 55-56
                        continue
                    if not spamDict.get(w):
                        spamDict[w] = 1
                    else:
                        spamDict[w] += 1
                    if not hamDict.get(w): #w not in hamDict:
                        hamDict[w] = 0
                    if w not in vocabulary:
                        vocabulary[w] = 1
                    spamWordCount += 1
                #close(f)
                    #print(wordList)
    return

def accessTrainingFolders(directoryPath):      
    for root, dirs, files in os.walk(directoryPath, topdown=True):
#        print(root)
#        print(dirs)
        for f in files:
            if "spam" in f and f.endswith(".txt"):
                fileParser(os.path.join(root, f), "spam")
            elif "ham" in f and f.endswith(".txt"):
                fileParser(os.path.join(root, f), "ham")
        
def writeToFile(directoryPath):
#    print("reached here")
    global hamDict, spamDict, vocabulary, spamFileCount, spamWordCount, hamFileCount, hamWordCount
    vocabSize = len(vocabulary)
    model = open("nbmodel.txt", "w+", encoding="latin1")
    model.write("directoryPath" + directoryPath)
    model.write("\nVocabSize "+str(vocabSize))
    model.write("\nSpamWordCount "+str(spamWordCount) + "\nSpamFileCount "+str(spamFileCount))
    model.write("\nHamWordCount "+str(hamWordCount) + "\nHamFileCount "+str(hamFileCount))
    model.write("\nDICTHAM")
#    print("DictHam")
    #print(hamDict)
    for i in hamDict:
        hamDict[i] = (hamDict[i] +1) / (hamWordCount+vocabSize)
        model.write("\n" +str(i) + " " + str(hamDict[i]))
    #model.write("\n"+str(hamDict))
    model.write("\nDICTSPAM")
#    print("DictHam")
    for i in spamDict:
        spamDict[i] = (spamDict[i] +1) / (spamWordCount+vocabSize)
        model.write("\n"+str(i) + " " + str(spamDict[i]))
    #model.write("\n"+str(spamDict))
#    print(hamWordCount)
#    print(spamWordCount)
#    print(len(spamDict))
#    print(len(hamDict))
#    print(spamFileCount, hamFileCount)
    model.close()
    

#print("Hello")

if __name__ =="__main__":
#    print(sys.argv[1], "system arguments")
    directoryPath = sys.argv[1]
    accessTrainingFolders(directoryPath)
    writeToFile(directoryPath)
#    print(time.time() - start_time)