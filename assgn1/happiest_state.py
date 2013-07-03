import sys
import json
import re

# This prints out the happiest state in US. 
# To Run:
# python happiest_state.py <sent_file> <tweets>
# Details:
# It extracts state information from location field of tweet and calculates
# its score. 
# This scripts does some checking as the data could be dirty.
state_mapping = { 
	"alabama": "al",
	"alaska": "ak",
	"arizona": "az",
	"arkansas": "ar",
	"california": "ca",
	"colorado": "co",
	"connecticut": "ct",
	"delaware": "de",
	"florida": "fl",
	"georgia": "ga",
	"hawaii": "hi",
	"idaho": "id",
	"illinois": "il",
	"indiana": "in",
	"iowa": "ia",
	"kansas": "ks",
	"kentucky": "ky",
	"louisiana": "la",
	"maine": "me",
	"maryland": "md",
	"massachusetts": "ma",
	"michigan": "mi",
	"minnesota": "mn",
	"mississippi": "ms",
	"missouri": "mo",
	"montana": "mt",
	"nebraska": "ne",
	"nevada": "nv",
	"new hampshire": "nh",
	"new jersey": "nj",
	"new mexico": "nm",
	"new york": "ny",
	"north carolina": "nc",
	"north dakota": "nd",
	"ohio": "oh",
	"oklahoma": "ok",
	"oregon": "or",
	"pennsylvania": "pa",
	"rhode island": "ri",
	"south carolina": "sc",
	"south dakota": "sd",
	"tennessee": "tn",
	"texas": "tx",
	"utah": "ut",
	"vermont": "vt",
	"virginia": "va",
	"washington": "wa",
	"west virginia": "wv",
	"wisconsin": "wi",
	"wyoming": "wy" }

def hasLocationInfo(tweet):
	userInfo = tweet.get("user")
	if userInfo == None and tweet.get("place") == None:
		return False
	if userInfo["location"] == None and userInfo["time_zone"] == None and tweet.get("place") == None:
		return False
	if userInfo["location"] == "" and userInfo["time_zone"] == None and tweet.get("place") == None:
		return False
	return True

def printTweetLocation(tweet):
	if tweet.get("place") and tweet.get("place").get("location"):
		print "==>" + tweet.get("place").get("location") + tweet.get("text")

	if tweet.get("user") and tweet.get("user").get("location"):
		print "==>" + tweet.get("user").get("location") + tweet.get("text")


def retTweet(tweet):
	print tweet["user"].get("time_zone") + " " + tweet["user"].get("location") + " " + tweet["text"]

def isEnglishTweet(tweet):
	# tweet with undefined lang will be treated as english tweet
	lng = tweet.get("lang")

	if lng == None or lng == "" or lng == "en":
		return True
	return False

def loadTweet(fp):
	tweets = []
	for line in fp:
		result = json.loads(line.encode('utf-8'))
		tweets.append(result)

	# Filter out only english tweets
	tweets = filter (isEnglishTweet, tweets)
	# Filter out tweets with no location information
	tweets = filter (hasLocationInfo, tweets)
	# Filter out tweets with no text
	tweets = filter(lambda tweet: tweet.get("text") != None, tweets)
	
	# Print out tweets
	#map(printTweetLocation, tweets)

	return tweets

def extractState(tweet):
	place = tweet.get("place")
	user = tweet.get("user")
	if place:
		loc = place.get("location")
		if loc and loc.lower() in state_mapping.keys():
			return loc.lower()

	if user:
		loc = user.get("location")
		if loc and loc.lower() in state_mapping.keys():
			return loc.lower()

	return None

def getScore(tweet, dict):
	score = 0
	if tweet.get("text"):
		words = tweet.get("text").split()
		for word in words:
			if word.lower() in dict:
				score = score + dict[word.lower()]
	return score

def initializeHappStDict(happ_st):
	for state in state_mapping.keys():
		happ_st[state] = 0
	return

def getTermSent(fp, dict):
	tweets = loadTweet(fp)
	happ_st = {}
	initializeHappStDict(happ_st)

	# extract state info
	for tweet in tweets:
		state = extractState(tweet)
		if state:
			happ_st[state] += getScore(tweet, dict)

	#sort highest score state
	#print happ_st.items()
	lst = happ_st.items()
	lst.sort(lambda a,b : int(b[1]-a[1]))
	print state_mapping[lst[0][0]]

def buildDictFromSentFile(file):
    scores = {} # initialize an empty dictionary
    for line in file:
		# The file is tab-delimited. "\t" means "tab character"
        term, score  = line.split("\t") 
        scores[term] = float(score)  # Convert the score to an integer.
    
    return scores

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    dict = buildDictFromSentFile(sent_file)
    getTermSent(tweet_file, dict)

if __name__ == '__main__':
    main()