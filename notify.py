#!/usr/bin/python
print "Content-type: text/html\n"

import cgi, cgitb, md5, random, os, time
cgitb.enable()
form =cgi.FieldStorage()
keys=form.keys()
user='test'
id='test'
ip=os.environ["REMOTE_ADDR"]
currentTime=time.time()

if "user" in keys:
    user=form['user'].value 
if "id" in keys:
    id=form['id'].value
        
topHtml='''<!DOCTYPE HTML><html>
<head>
   <title>Forum</title>
   <link rel="icon" href="http://stuy.enschool.org/favicon.ico" type="image/x-icon">
   <link rel="stylesheet" type="text/css" href="style.css"> 
</head>
<body>'''


bottomHtml='''
</body>
</html>
'''
def readCSV(csv):
    text=open(csv).read().strip()
    log=text.split('\n')
    logList=[]
    for a in log:
        logList.append(a.split('|'))
    return logList

def loggedIn():
    logg=readCSV('files/loggedin.txt')
    for a in logg:
        if a[0]==user and a[1]==id and a[2]==ip:
            return True
    return False

def timeExpired():
    logg=readCSV('files/loggedin.txt')
    for a in logg:
        if a[0]==user and a[1]==id and a[2]==ip:
            logOutTime=float(a[3])
    if currentTime > logOutTime:
        return True
    return False


def makePage():
    retHTML=topHtml
    if loggedIn():
        if timeExpired():
            retHTML+='''<h2>The time limit on your account has expired. 
                            Please click <a href="logIn.py?user=''' + user + '&id=' + id + '''&logOut=True">here</a> 
                            to relogin.</h2>
            '''
        else:
            retHTML+=  '''
<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
            <div id="bar">
            <ul class="sidebar">
                <li><a class="bar_element" href="forum.py?user=''' + user +'&id=' + id + '''&logIn=True">Home</a> </li>
                <br><li><a class="bar_element" href="rules.py?user=''' + user +'&id=' + id + '''&logIn=True">Rules</a> </li>
                <br><li><a class="bar_element" href="next.py?user=''' + user +'&id=' + id + '''&logIn=True">Our Forum</a> </li>
                <br><li><a class="bar_element" href="main.py?user=''' + user +'&id=' + id + '''&logIn=True">Upload Something</a> </li>
                <br><li><a class="bar_element" href="account.py?user=''' + user +'&id=' + id + '''&logIn=True">View Uploads</a> </li>
                <br><li><a class="bar_element" href="delete.py?user=''' + user +'&id=' + id + '''&logIn=True">Delete Uploads</a> </li>
                <br><li><a class="bar_element" href="notify.py?user=''' + user +'&id=' + id + '''&logIn=True">Notifications</a> </li>
                <br><li><a class="bar_element" href="logIn.py?user=''' + user + '&id=' + id + '''&logOut=True">Log Out</a> </li>
                           </ul></p>
            </div>
'''
            if len(str(notify()))!=0:
              retHTML+='<div id="par">'
              retHTML+=str(notify())
              retHTML+='</div>'
              retHTML+=bottomHtml
              return retHTML
            else:
              retHTML+='<div id="par">'
              retHTML+="No notifications!"
              retHTML+='</div>'
              retHTML+=bottomHtml
              return retHTML
            


def notify():
  files=[]
  notifs=readCSV("files/notif.txt")
  if len(notifs)!=1 or notifs[0][0]!='':
    for line in notifs[:]:
        if line[0]==user:
            files.append(line[1])
            notifs.remove(line)
    for pos in range(len(notifs)):
        notifs[pos]='|'.join(notifs[pos])
    if len(notifs)!=1:
        notifs='\n'.join(notifs) + '\n'
    else: notifs=notifs[0]+'\n'
    rwrite=open("files/notif.txt","w")
    rwrite.write(notifs)
    rwrite.close() 
  if len(files)==0:
    fmessage=''
  if len(files)==1:
    fmessage="%s has been printed~"%(files[0])
  if len(files)>1:
    fill=files[0]+" "
    for pos in range(1,len(files)):
        fill+=",%s "%(files[pos])
    fmessage="%s have been printed~"%(fill)
  return fmessage


print makePage()
