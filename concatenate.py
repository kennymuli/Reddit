import glob as gb
import pandas as pd 

#Collect the Comments files in a list to parse
commentsFile = "posts*" #the string that all comments.pk files contain
fileList = [] #the list where we will store the comments.pk files

for file in gb.glob(commentsFile): #compile a list of all the comments.pk files
	fileList.append(file)

df = pd.concat([pd.read_pickle(file) for file in fileList], axis=0) #concatenate all comments files into one comment file
df.to_pickle('./allposts.pk') 