#yamoah
#This algorithm is a naive bayes implementation...
#This is one of the implementations that were not completed

#!/usr/bin/python
import sys
import re

#A class for the data
#Each data has the attributes below
class Data:
    question = [""]
    answer = [""]
    keywords = [""]
    threshold = 0
    wordsAll = [""]
    setWordsAll = ()
    numWords = 0
    setNumWords = 0

#method to create an instance of the the data class
def newData():
    d1 = Data()
    return d1

#Takes the various inputs and processes them
def readFiles(quest, topic, ans, test):
    print("hello")
    myList = []
    classZero = [""] #set of elements in class zero
    classOne = [""] #set of elements in class one
    setClassZero =() # unique set of elements in class zero
    setClassOne = () # unique set of elements in class one
    noClass = [""] #unclassified
    BagOfWords = [""]
    #----------------------------------------#
    countZero=countOne=countLess=0
    classZeroCount = classOneCount = classlessCount = 0
    numLines = 0
    curData = newData()#here
    line = myFile.readline()
    f_ques,f_topic, f_ans = open(quest, "r"),open(topic, "r"),open(ans, "r")
    myFile = open(test, "r")
    line = myFile.readline()
    line2, line3, line4 = f_ques.readline(), f_topic.readline(), f_ans.readline()   
    while (line!=""):
        lineSplit = line.split()
        lineLength = len(lineSplit)
        if(int(lineSplit[lineLength-1])): #the class (0 or 1)
            lineSplit.pop(lineLength-1)

        curData.wordsAll.extend(lineSplit)#
        curData.numWords = curData.numWords + lineLength

        numLines = numLines + 1
        line = myFile.readline()
    myList.append(curData)
    #At this point we have our bag of words and the counts
    #But the words may not be unique, so I will use sets
    #print(numLines)
    #print(countLess)
    #......prior prob..........#
    priorZero = countZero/(countZero+countOne)
    priorOne = countOne/(countZero+countOne)

    setClassZero = set(classZero)
    setClassOne = set(classOne)
    countSetZero = -1
    countSetOne = -1
    for a in setClassZero:
        countSetZero = countSetZero + 1
    for b in setClassOne:
        countSetOne = countSetOne + 1

    #.......calculate likelihood.....#

    myFilee = open(filename,"r")
    linee = myFilee.readline()
    outFile = open("results_file.txt","w")
    while (linee!=""):
        probClassZero = 1
        probClassOne = 1
        lineSplitt = linee.split()
        for m in lineSplitt:
            a = classZero.count(m)
            aa = a + 1
            probClassZero = probClassZero * (aa/(classZeroCount+countSetZero+countSetOne))
            b = classOne.count(m)
            bb = b + 1
            probClassOne = probClassOne * (bb/(classOneCount+countSetZero+countSetOne))
        if probClassZero > probClassOne:
            outFile.write("0\n")
        elif probClassZero < probClassOne:
            outFile.write("1\n")
        else:
            outFile.write("uncertain\n")
        linee = myFilee.readline()
    outFile.close()
    
try:
    #print(sys.argv[1])
    #myFile = sys.argv[1],"Topics.txt"]
    #readDataSet(myDataSet,myFile)
    readFiles("Questions.txt", "Topic.txt", "Answers.txt", "hello.txt")
except:
    print("Big Error")
