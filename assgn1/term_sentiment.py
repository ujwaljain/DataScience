import sys
import json
import re

# Generates a sentiment for each term which is not defined in pre-defined sentiment file
# To Run:
# python term_sentiment <sentiment_file> <tweet_file> 
# this script parses a tweet_file which contains list of tweets and assigns sentiment to each term 
# using following alogrithm:-

# Parse sentiment file and create a dictionary of <words, sentiment>
# For each tweet, compute its sentiment. For words not present in dict, assign
# sentiment of their word as 0
# Now for all the words which are not present in the dictionary, assign 
# sentiment of each word as avg of sentiments of all tweets they appear in.

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
