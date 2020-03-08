import glob as gb
import pandas as pd 

df = pd.read_pickle('./allcomments.pk')
records = df.groupby('link_id')
#-------------
#Basic Stats
#-------------
commentsTotal = records['is_submitter'].count()
commentsOP = records['is_submitter'].sum()
commentsOther = commentsTotal - commentsOP
commentsRatio = commentsOther/commentsOP

print commentsTotal.idxmax(10)

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