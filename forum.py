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
        logList.append(a.split(','))
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
            <div id="bar">
            <ul class="sidebar">
                <li><a class="bar_element" href="forum.py?user=''' + user +'&id=' + id + '''&logIn=True">Home Page</a> </li>
            </ul></p>
            </div>
<div id="r">
<h2>welcome to our forum</h2>
<h3> Come back later</h3>
<div id="logout"><a href="logIn.py?user=a123&id=35283893675859&logOut=True">
            Click here to log out.</a></div></div>
            '''
 
            #retHTML+='''
            #Log out <a href="logIn.py?user=''' + user + '&id=' + id + '''&logOut=True">here</a>.
        #'''
    else:
        retHTML+='<h2>Page not found.</h2>'
    return retHTML+bottomHtml


print makePage()

