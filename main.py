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
            retHTML+='''
<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
<div id="par2">
'''
            retHTML+=  user.capitalize() + ''' , What would you like to print today?</h1>
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
           <p>Period # you're stopping by
       <select name="pd" size="1">
  <option selected>03</option>
  <option>04</option>
  <option>05</option>
  <option>06</option>
  <option>07</option>
  <option>08</option>
  <option>09</option>
  <option>10</option>
</select><br><br>
How would you like your paper organized?<br>
<input type="radio" name="clip_type" value="None"checked>None<br>
<input type="radio" name="clip_type" value="Stapled">Stapled<br>
<input type="radio" name="clip_type" value="Papercliped">Papercliped<br>
<br> No. of copies?
<select name="copy" size="1">
  <option selected>1</option>
  <option>2</option>
  <option>3</option>
</select>



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
Future forum<a href="forum.py?user='''%(user,id) + user + '&id=' + id + '''&logIn=True">here</a>

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
    open('files/uploaded.txt','w').write('user|file name|pd|clip type|copies\n')
#while True: 
#  autoRM()

