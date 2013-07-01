import sys
import json
import re

def getNormScore(tweet, dict):
	score = 0
	normScore = 0
	wdCount = 0
	words = tweet.split()
	for word in words:
		if word.lower() in dict:
			score = score + dict[word.lower()]
			wdCount =+ 1
	if wdCount:
		normScore = score/wdCount;
	return normScore

def updateScore(tweet, dict, newDict, freq, normScore):
	words = tweet.split()

	for word in words:
		if word not in dict:
			if word in newDict:
				newDict[word] += normScore
				freq[word] += 1
			else:
				newDict[word] = normScore
				freq[word] = 1

def buildDictFromSentFile(file):
    scores = {} # initialize an empty dictionary
    for line in file:
		# The file is tab-delimited. "\t" means "tab character"
        term, score  = line.split("\t") 
        scores[term] = float(score)  # Convert the score to an integer.
    
    return scores

def normalizeScore(newDict, freq):
	for key in newDict.keys():
		newDict[key] /= freq[key]

def print_sentiment(newDict):
	for key in newDict.keys():
		print key + " %.03f" % newDict[key]

def getTermSent(fp, dict):
	newDict = {}
	freq = {}
	for line in fp:
		result = json.loads(line.encode('utf-8'))
		tweet = result.get('text')
		if tweet:
			normScore = getNormScore(tweet, dict)
			updateScore(tweet, dict, newDict, freq, normScore)

	normalizeScore(newDict, freq)			
	print_sentiment(newDict)

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    dict = buildDictFromSentFile(sent_file)
    getTermSent(tweet_file, dict)

if __name__ == '__main__':
    main()
