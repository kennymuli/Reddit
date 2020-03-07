import glob as gb
import pandas as pd 

#Collect the Comments files in a list to parse
commentsFile = "comments*" #the string that all comments.pk files contain
columnGroup = 'link_id' #the column we will use to group all of the rows in the data frame
fileList = [] #the list where we will store the comments.pk files

for file in gb.glob(commentsFile): #compile a list of all the comments.pk files
	fileList.append(file)

print len(fileList)

def totalComments(fileList): #Get the total amount of all comments collected
	totalCount = 0
	for file in fileList:
		df = pd.read_pickle(file)
		count = len(df.index)
		totalCount += count
	return totalCount

totalCount = totalComments(fileList)
print totalCount

for file in fileList:
	df = pd.read_pickle(file)
	dfgroups = df.groupby('link_id')
	totalComments = dfgroups['is_submitter'].count()
	responses = dfgroups['is_submitter'].sum()
	comments = totalcomments - responses
	responseRatio = comments/responses
	print responseRatio

#List of all columns in the content data frame
#--------------
#Columns to Use  	
#--------------
#body - what the person actually wrote
#is_submitter - is the person commenting the person who submitted (OP)?
#id - the unique ID for the particular comment
#link_id - the ID of the parent post (the original post, not parent comment)
#parent_id - the ID of the preceding comment (or the OP if there is no parent comment), good for checking which comment the OP responded to
#score - the total upvotes/downvotes the comment received

#--------------
#Other Columns
#--------------
#all_awardings
#approved_at_utc
#associated_award
#author
#author_cakeday
#author_flair_background_color
#author_flair_css_class
#author_flair_richtext
#author_flair_template_id
#author_flair_text
#author_flair_text_color
#author_flair_type
#author_fullname
#author_patreon_flair
#author_premium
#awarders
#banned_at_utc
#can_mod_post
#collapsed
#collapsed_because_crowd_control
#collapsed_reason
#created_utc
#distinguished
#edited
#gildings
#locked
#no_follow
#permalink
#retrieved_on
#send_replies
#steward_reports
#stickied
#subreddit
#subreddit_id
#total_awards_received

#Questions to Answer
#What is the average % of questions/comments that an AMAer responds to?
#Does that % change based on the number of questions?
#How many questions before the OP stops asking questions?
#NLP - any particular types of questions that people who post respond to?
#What's the upvoted questions that the author answers?
#What qualifies as a good AMA vs a BS AMA?

#Create a dictionary, do it by link_id:
	#total non-OP comments
	#total OP comments
	#total comments