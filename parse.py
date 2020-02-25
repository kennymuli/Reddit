import time
import datetime
import requests as r
import pandas as pd

currentTime = datetime.datetime.now() #Get the current time
unixtime = time.mktime(currentTime.timetuple()) #Convert current time to Unix format

#hardcode variables
subreddit ="ama"
time = int(unixtime)
beforeTime = str(time)
length = 7 #in days
afterTime = str(time - length*(24*60*60))
endTime = 1252540800 #Unix Time for August 10, 2009 at 12:00AM, when the AMA subreddit was created
responseSize = 1000
postsFile = './posts.pk' #storage area for all of the posts
commentsFile = './comments.pk' #storage area for all of the comments

def postsURL(subreddit, afterTime, beforeTime, responseSize): #Create the URL
	urlBase = "https://api.pushshift.io/reddit/search/submission/"
	appendSubreddit = "?subreddit=" +subreddit 
	#the tails of the cURL
	appendSort = "&sort=desc&sort_type=created_utc"
	appendAfterTime = "&after=" + afterTime
	appendBeforeTime = "&before=" + beforeTime
	size = "&size=" + str(responseSize)
	return(urlBase+appendSubreddit+appendSort+appendAfterTime+appendBeforeTime+size)

def curlCall(url): #Get the cURL response from a URL
	response = r.get(url)
	return(response.json())

def parsePosts(response): #set up the data in a Pandas Data Frame
	return(pd.DataFrame(response['data']))

def appendPosts(data,file): #saving the posts data frames
	try: 
		f.open(file)
		OGFile = pd.read_pickle(file)
		OGFile.append(data)
	except:
		print("Creating Posts Data Frame")
		data.to_pickle(directoryPosts)

def commentsURL(post_id,responseSize): #Get the comments from the posts
	urlBase = "https://api.pushshift.io/reddit/comment/search/"
	appendPostID = "?link_id=" + post_id
	responseSize = "&limit=" + str((responseSize*200))
	return(urlBase + appendPostID + responseSize)

def getNewUTC(postsDataframe): #Get the new UTC time for beforeTime in UTC
	return(postsDataframe['created_utc'].min())

response = curlCall(curlURL) #get the response from the created URL, returns in JSON format

while afterTime > endTime: #while there are still other posts to go through, keep going
	#1 run postURL to get the pushshift list of URLs
	postURL = postsURL(subreddit,afterTime,beforeTime,responseSize)

	#2 get the URL, get the API response, and change it into a JSON
	responsePosts = curlCall(postURL)

	#3 take the JSON and parse it with Pandas Data Frame
	postsDF = parsePosts(responsePosts)

	#4 save the parsed data frame into a file
	appendposts(postsDF,postsFile)

	#5 for each of the posts in the DF, get all of the comments
	for postID in postsDF['id']:
		post_id = postID

		#6 Create the URL for each pushshift comments API call
		commentURL = commentsURL(post_id,responseSize)

		#7 Get the URL, get the API response, and change it into JSON
		responseComments = curlCall(commentURL)

		#8 Parse each API call into a dataframe
		commentsDF = parsePosts(responseComments)

		#9 add the comments df into the comments file
		appendposts(commentsDF,commentsFile)

	#10 get the new time
	time = getNewUTC(commentsDF)
	beforeTime = str(time)
	afterTime = str(time - length*(24*60*60)) #as long as afterTime > endTime, it will loop and continue again with new beforeTime and new afterTime

#MEASUREMENT: TOtal no-OP responses vs total OP responses, for response rate (number of questions responded to)

#LIST OF DATA FOR POST
#"author": "DonHijoPadre",
#"author_flair_css_class": null,
#"author_flair_richtext": [],
#"author_flair_text": null,
#"author_flair_type": "text",
#"brand_safe": true,
#"can_mod_post": false,
#"contest_mode": false,
#"created_utc": 1523932719,
#"domain": "self.learnpython",
#"full_link": "https://www.reddit.com/r/learnpython/comments/8ct9yq/need_help_sending_audio_over_twilio/",
#"gilded": 0,
#"id": "8ct9yq",
#"is_crosspostable": true,
#"is_original_content": false,
#"is_reddit_media_domain": false,
#"is_self": true,
#"is_video": false,
#"link_flair_richtext": [],
#"link_flair_text_color": "dark",
#"link_flair_type": "text",
#"locked": false,
#"no_follow": true,
#"num_comments": 0,
#"num_crossposts": 0,
#"over_18": false,
#"parent_whitelist_status": "all_ads",
#"permalink": "/r/learnpython/comments/8ct9yq/need_help_sending_audio_over_twilio/",
#"pinned": false,
#"retrieved_on": 1523935823,
#"rte_mode": "markdown",
#"score": 3,
#"selftext": "I'm a bit of a novice at Twilio so I hope someone can point me in the right direction. \n\nI would like to send audio over text. I already have the .mp3 saved on my computer, so where should i go after that? \n\nThanks. ",
#"send_replies": true,
#"spoiler": false,
#"stickied": false,
#"subreddit": "learnpython",
#"subreddit_id": "t5_2r8ot",
#"subreddit_subscribers": 117435,
#"subreddit_type": "public",
#"thumbnail": "self",
#"title": "Need Help sending audio over Twilio",
#"url": "https://www.reddit.com/r/learnpython/comments/8ct9yq/need_help_sending_audio_over_twilio/",
#"whitelist_status": "all_ads"

#LIST OF DATA FOR COMMENTS
#"approved_at_utc": null,
#"author": "doug89",
#"author_flair_css_class": "",
#"author_flair_text": "Bot Developer",
#"banned_at_utc": null,
#"body": "    &gt;&gt;&gt; submission = reddit.submission('79h5fc')\n    &gt;&gt;&gt; submission.url\n    'https://www.reddit.com/r/redditdev/comments/79h5fc/is_there_a_way_to_get_a_posts_permalink_using/'\n    &gt;&gt;&gt; submission.permalink\n    '/r/redditdev/comments/79h5fc/is_there_a_way_to_get_a_posts_permalink_using/'\n    &gt;&gt;&gt; 'https://www.reddit.com' + submission.permalink\n    'https://www.reddit.com/r/redditdev/comments/79h5fc/is_there_a_way_to_get_a_posts_permalink_using/'",
#"can_mod_post": false,
#"collapsed": false,
#"collapsed_reason": null,
#"created_utc": 1509322108,
#"distinguished": null,
#"edited": false,
#"id": "dp2l7oz",
#"is_submitter": false,
#"link_id": "t3_79h5fc",
#"parent_id": "t3_79h5fc",
#"permalink": "/r/redditdev/comments/79h5fc/is_there_a_way_to_get_a_posts_permalink_using/dp2l7oz/",
#"retrieved_on": 1509322109,
#"score": 1,
#"stickied": false,
#"subreddit": "redditdev",
#"subreddit_id": "t5_2qizd"