import sys
import json

def getFrequency(tweet, freq, wordCount):
	words = tweet.split()
	for word in words:
		wordCount += 1

		if word.lower() in freq:
			freq[word.lower()] += 1
		else:
			freq[word.lower()] = 1
	
	return wordCount

def normalizeAndPrintFreq(freq, wordCount):
	for key in freq.keys():
		freq[key] /= wordCount
		print key, "%.04f" % freq[key]

def getTermFrequency(fp):
	freq = {}
	wordCount = 0.000;

	for line in fp:
		result = json.loads(line.encode('utf-8'))
		tweet = result.get('text')
		#print tweet
		if tweet:
			wordCount = getFrequency(tweet, freq, wordCount)
			
	normalizeAndPrintFreq(freq, wordCount)

def main():
    tweet_file = open(sys.argv[1])
    getTermFrequency(tweet_file)

if __name__ == '__main__':
    main()
