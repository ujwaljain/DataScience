import sys
import json
import re

# prints out the most used hashtags.

def loadTweet(fp):
	tweets = []
	for line in fp:
		result = json.loads(line.encode('utf-8'))
		tweets.append(result)

	# Filter out tweets with no hashtags information
	tweets = filter(lambda tweet: tweet.get("entities").get("hashtags"), tweets)
	# Filter out english tweets
	tweets = filter(lambda tweet: tweet.get("lang") == "en", tweets)

	# Print out tweets
	#for t in tweets: print (t.get("entities").get("hashtags")[0]).get("text")
	return tweets

def getHashTagFreq(fp):
	tweets = loadTweet(fp)
	hashdict = {}
	
	# extract state info
	for tweet in tweets:
		hashtag = (tweet.get("entities").get("hashtags")[0]).get("text")
		if hashtag in hashdict.keys():
			hashdict[hashtag] += 1
		else:
			hashdict[hashtag] = 1
	
	#print hashdict.items()		
	#sort by decreasing count
	sorted_scores = sorted(hashdict.items(), key=lambda x: x[1])[0:10]
	
	for k, v in sorted_scores:
		print k, "%.01f" % v


def main():
    tweet_file = open(sys.argv[1])
    getHashTagFreq(tweet_file)

if __name__ == '__main__':
    main()
