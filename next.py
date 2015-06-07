#!/usr/bin/env python
print "Content-type: text/html\n"
print '''<html><head>
   <link rel="icon" href="http://stuy.enschool.org/favicon.ico" type="image/x-icon">
<link rel="stylesheet" type="text/css" href="style.css"></head><body>'''
import cgi, os
import commands
import cgitb
cgitb.enable()
posted=False
form = cgi.FieldStorage()
keys=form.keys()


ip=os.environ["REMOTE_ADDR"]

if "user" in keys:
    user=form['user'].value 
if "id" in keys:
    id=form['id'].value
if 'post' in keys:
    post=form['post'].value
    posted=True

def readCSV(csv):
    text=open(csv).read().strip()
    log=text.split('\n')
    logList=[]
    for a in log:
        logList.append(a.split('|'))
    return logList

# Test if the file was uploaded
def loggedIn():
    logg=readCSV('files/loggedin.txt')
    for a in logg:
        if a[0]==user and a[1]==id and a[2]==ip:
            return True
    return False

def writeCSVline(L):
    return "|".join(L) + '\n'


import datetime   
n=str(datetime.datetime.now())[:-7]
def printPage():
  if loggedIn():
    ans=''
    if posted:
      ans='Your post has been posted.'
    ans+= '''<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>

                <form method="POST" action="next.py?user=''' + user + '&id=' + id + '''&logIn=True">
                    <textarea rows="10" name="post" cols="50">Ask/post a note</textarea>
                  <input type="submit" name="Submit" value="Post">
                </form>
           '''   
    if posted:
      postNum=int(readCSV('files/posts.txt')[0][0])   
      f=open('files/posts.txt','a')
      f.write(user+'|'+post+'|'+n+ '|'+str(postNum)+'\n')
      postNum+=1
      f.close()
      f=open('files/posts.txt')
      data=f.read()
      f.close()
      pos=data.find('\n')
      data=str(postNum)+data[pos:]
      f=open('files/posts.txt','w')
      f.write(data)
      f.close()
  else:
    ans= 'Log in to view'
  print ans
printPage()
f=open('files/posts.txt','r')
p=f.readlines()

try:
  for w in p[1:]:
    a=w.split('|')
    print '<div id="par3"><h3>'+a[1]+'</h3><BR>' + a[0]+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+a[2]+'<BR>'+'<HR></div>' 
  #for i in a:
   # i=i.strip('\n')
    #print i[0]+"<BR>"
  f.close()
except: print''


print '''<br><br>
Go Back <a href="forum.py?user=''' + user + '&id=' + id + '''&logIn=True">here</a>.
'''
print "</body></html>"




