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

ans=''
ip=os.environ["REMOTE_ADDR"]

if "user" in keys:
    user=form['user'].value 
if "num" in keys:
    id=form['num'].value


def readCSV(csv):
    text=open(csv).read().strip()
    log=text.split('\n')
    logList=[]
    for a in log:
        logList.append(a.split('|'))
    return logList


def writeCSVline(L):
    return "|".join(L) + '\n'


def printPage():
  ans= '''<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
          <div id="par">
                <form method="POST" action="verify.py?">
              Your user email:
                    <input type="text" name="user" size="20" required><br><br><br>
              Verification number:
                    <input type="text" name="num" size="20" required><br><br>
                  <input type="submit" name="Submit" value="Post">
                </form></div>
           '''   
  return ans

def match():
   f=readCSV('files/pending.txt')
   for w in f:
     if user==w[0] and id==w[2]:
       print "Success"
       a=open('files/users.txt','a')
       a.write(w[0] + '|' + w[1] +'\n')
       a.close()
       for line in f:
         if line[0]==user:
           f.remove(line)
                
   
     
if "user" in keys and "num" in keys:
  match()
else:
  print printPage()
  
print "</body></html>"




