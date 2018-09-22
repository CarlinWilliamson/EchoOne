import re

line = '<div aria-label="Open Video Menu for COMP2521 Lecture 1UGA Thu 9:05 (2 hours)" class="menu-opener" tabindex="0" role="button" aria-haspopup="true" aria-controls="G_d5d0e9af-d27a-4ab1-9e2f-fb2a5e38c7be_ffd239ca-aab9-445f-ab8d-2b90308b4a60_2018-07-26T09:05:00.000_2018-07-26T10:55:00.000_Video_menu" aria-expanded="false" style=""><div class="courseMediaIndicator capture" data-tooltip=""></div></div>'
matchObj = re.match( r'.*_(\d{4})-(\d{2})-(\d{2})T.*', line)
#matchObj = re.match( r'!(\w*)!', line)
if matchObj:
   #print ("matchObj.group() : " + matchObj.group(0)) #Entire Statement
   print ("matchObj.group(1) : " + matchObj.group(1)) #Year!
   print ("matchObj.group(2) : " + matchObj.group(2)) #Month!
   print ("matchObj.group(3) : " + matchObj.group(3)) #Day!
else:
   print ("No match!!")