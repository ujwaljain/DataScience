import sys
import json

def hw():
    print 'Hello, world!'

def getScore(fp, dict):
    for line in fp:
        result = json.loads(line.encode('utf-8'))
        score = 0
        if 'text' in result:
            tweet = result['text']
            words = tweet.split()
            for word in words:
                if word.lower() in dict:
                    score = score + dict[word.lower()]
        print score


def buildDictFromSentFile(file):
    scores = {} # initialize an empty dictionary
    for line in file:
		# The file is tab-delimited. "\t" means "tab character"
        term, score  = line.split("\t") 
        scores[term] = int(score)  # Convert the score to an integer.
    
    return scores
    #print scores.items() # Print every (term, score) pair in the dictionary

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    dict = buildDictFromSentFile(sent_file)
    getScore(tweet_file, dict)

if __name__ == '__main__':
    main()
