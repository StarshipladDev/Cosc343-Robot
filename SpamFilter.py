#Author: StarshipladDev 1/11/19
from dataset_trec import dataset_trec
from random import *
tstingLabel='spam'
tstingWord="This is a spam email"

nontstingWord=""
"""
Returns the probability that a word is spam based on prior chances a words is spam
wordStr - The string of words to check for spam
labelStr -The string of words labeled spam
messages - The list of prior messages
labels - The list of known spam words
"""
def prob_word_given_label(wordStr, labelStr, messages, labels):
    returnProb=0;
    for w in wordStr:
        i = 0
        prob = 0
        match = 0
        while(i<len(messages)):
            for m in messages[i]:
                if (w==m):
                    if (labels[i]== labelStr):
                        prob += 1
                    match += 1
            i+=1
        if(returnProb==0):
            if(match!=0):
                returnProb=prob/match
        else:
            if (match != 0):
                returnProb = returnProb * (prob/match)
    if(returnProb==0):
        return 0.5
    if prob==0:
        return 0
    else:
        return 100*(returnProb)
#--------------End of function---------------------------#
trec07 = dataset_trec.load()

messages = trec07.data
labels = trec07.target
if(tstingLabel=="ham"):
    nontstingWord="spam"
else:
    nontstingWord="ham"

print("BREAK           -----------\n\n ")
overall=1000
testStrings=messages[:overall]
testLabels=[]
ii=0
rights=0
for s in testStrings:
    if(prob_word_given_label(s, tstingLabel, messages, labels)>10):
        testLabels.append(tstingLabel)
    else:
        testLabels.append(nontstingWord)
    print("-------%d-----" % ii)
    print(messages[ii])
    print("Legit result: ",labels[ii])
    print("My result: ",testLabels[ii])
    if(labels[ii]==testLabels[ii]):
        rights+=1
    ii+=1
    print("Correct: %d / %d" % (rights, ii))
print("Correct: %d / %d" %(rights,overall))
exit(1)

