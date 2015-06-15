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
       print'''<center><h2>Success. </h2> 
<div id="par2"> Before you start using the site:<b> <center>General Rules & Guidelines</center></b>
<UL> Please note: Unacceptable posts/comments/uploads will result in major consequences. We are not responsible for your actions</LI>
<LI> No Impersonation (trying to be someone else) This isn't allowed and you will be banned without prior notice. </LI>
<LI>Please keep spam to a minimum.</LI></UL> <br>We thank your for your cooperation.    
</UL>
 <br><br>Log on <a href="logIn.py">here</a></center>'''
       a=open('files/users.txt','a')
       a.write(w[0] + '|' + w[1] +'\n')
       a.close()
       for line in f:
         if line[0]==user:
           f.remove(line)
       for i,x in enumerate(f):
          f[i]='|'.join(x)
       f='\n'.join(f)+'\n'
       File=open('files/pending.txt','w')
       File.write(f)
       File.close()
       break
      
      
                
   
     
if "user" in keys and "num" in keys:
  match()
else:
  print printPage()
  
print "</body></html>"
