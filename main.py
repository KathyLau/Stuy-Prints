#!/usr/bin/python
print "Content-type: text/html\n"

import cgi, cgitb, md5, random, os, time, commands
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
   <title>Main Page</title>
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
            retHTML+=  '''<h1>''' + user.capitalize() + ''' , What would you like to print today?</h1>
            <form method="post" 
               enctype="multipart/form-data"
               onsubmit="return check();"
               action="uploading.py">
            <p>
               Please select a .txt file to be sent:
               <br>
               <input type="file" name="file" size="40"
                  accept="application/msword, application/vnd.ms-excel, application/vnd.ms-powerpoint,
                  text/plain, application/pdf">
               </p>
           <p>Period# 
       <select name="pd" size="1">
  <option selected>03</option>
  <option>04</option>
  <option>05</option>
  <option>06</option>
  <option>07</option>
  <option>08</option>
  <option>09</option>
  <option>10</option>
</select>
Floor# 
       <select name="fl" size="1">
  <option selected>01</option>
  <option>02</option>
  <option>03</option>
  <option>04</option>
  <option>05</option>
  <option>06</option>
  <option>07</option>
  <option>08</option>
  <option>09</option>
  <option>10</option>
</select>
Room#
<input type="text" name="rm">

</p>

               Please include a short explanation:<br>
               <textarea name="expl" rows="3" cols="40"
               onfocus="check();"> 
               </textarea>
<input type="hidden" name="user" value="%s">
<input type="hidden" name="id" value="%s">
             
            <input type="submit" value="Send">
            </form>
<br>
Future forum<a href="post.py?user='''%(user,id) + user + '&id=' + id + '''&logIn=True">here</a>

<br>
            Log out <a href="logIn.py?user=''' + user + '&id=' + id + '''&logOut=True">here</a>.
        '''
    else:
        retHTML+='<h2>Page not found.</h2>'
    return retHTML+bottomHtml


print makePage()

import datetime

now=datetime.datetime.time(datetime.datetime.now())
today5pm = now.replace(hour=17, minute=0, second=0, microsecond=0)
today7pm = now.replace(hour=19, minute=0, second=0, microsecond=0)
if now > today5pm and now < today7pm:
    commands.getoutput("rm uploaded/03/*")
    commands.getoutput("rm uploaded/04/*")
    commands.getoutput("rm uploaded/05/*")
    commands.getoutput("rm uploaded/06/*")
    commands.getoutput("rm uploaded/07/*")
    commands.getoutput("rm uploaded/08/*")
    commands.getoutput("rm uploaded/09/*")
    commands.getoutput("rm uploaded/10/*")
    open('files/uploaded.txt','w').write('')
#while True: 
#  autoRM()
