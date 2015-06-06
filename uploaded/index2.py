#!/usr/bin/python
print "Content-type: text/html\n"

import cgi, cgitb, md5, random, os, time, commands
cgitb.enable()
form =cgi.FieldStorage()
keys=form.keys()
aduser='test'
id='test'
ip=os.environ["REMOTE_ADDR"]
currentTime=time.time()

if "user" in keys:
    user=form['user'].value 
if "id" in keys:
    id=form['id'].value
    
topHtml='''<!DOCTYPE HTML><html>
<head>
   <title>Main Page</title>
   <link rel="stylesheet" type="text/css" href="style.css"> 
</head>
<body>'''

filess='''
<h2> UPLOADED FILES</h2>
<a href="03">Period 3</a><br>
<a href="04">Period 4</a><br>
<a href="05">Period 5</a><br>
<a href="06">Period 6</a><br>
<a href="07">Period 7</a><br>
<a href="08">Period 8</a><br>
<a href="09">Period 9</a><br>
<a href="10">Period 10</a><br>
'''


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
    logg=readCSV('../files/loggedin.txt')
    for a in logg:
        if a[0]==user and a[1]==id and a[2]==ip:
            return True
    return False

def timeExpired():
    logg=readCSV('../files/loggedin.txt')
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
                            Please click <a href="../admlogIn2.py?user=''' + user + '&id=' + id + '''&logOut=True">here</a> 
                            to relogin.</h2>
            '''
        else:
            retHTML+=  filess
            retHTML+='''<br>
            Log out <a href="../admlogIn2.py?user=''' + user + '&id=' + id + '''&logOut=True">here</a>.

        '''
    else:
        retHTML+='<h2>Page not found.</h2>'
    return retHTML+bottomHtml


print makePage()
