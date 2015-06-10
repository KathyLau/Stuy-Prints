#!/usr/bin/python
print "Content-type: text/html\n"

import cgi, cgitb, md5, random, os, time

cgitb.enable()
form =cgi.FieldStorage()
keys=form.keys()

user='test'
pazz='test'
logOuts=False
id=str(random.randint(0,(10**10)))
ip=os.environ["REMOTE_ADDR"]
logOutTime= time.time() + (30*60) 

if "user" in keys:
    user=form['user'].value
if "pazz" in keys:
    pazz=form['pazz'].value
pazz=md5.new(pazz).hexdigest()
if 'logOut' in keys:
    logOuts=True
if "id" in keys:
    id=form['id'].value


def checkIt():
    return "user" in keys and "pazz" in keys

def dictOfUsers():
    userPazzs=open('files/users.txt','r').read().strip().split('\n')
    for i in range(len(userPazzs)):
        userPazzs[i]=userPazzs[i].split('|')
    d={}
    for i in userPazzs:
        d[i[0]]=i[1]
    return d

userPazzs=dictOfUsers()

def checkUserPazz():
    if checkIt() and user in userPazzs:
        return userPazzs[user]==pazz
    
def checkAll():
    return checkUserPazz() and checkIt()

topHtml='''<!DOCTYPE HTML><html>
<head>
   <title>log in</title>
   <link rel="icon" href="http://stuy.enschool.org/favicon.ico" type="image/x-icon">
   <link rel="stylesheet" type="text/css" href="style.css"> 


'''


bottomHtml='''
</body>
</html>
'''

def loggedInSpecial():
    log=readCSV('files/loggedin.txt')
    for i in log:
        if i[0]==user:
           logOut(i[0])

def writeCSVline(L):
    return "|".join(L) + '\n'

def logIn():
    loggedInSpecial()
    loggedin=open('files/loggedin.txt','a')
    loggedin.write(writeCSVline([user,id,ip,str(logOutTime)]))
    loggedin.close()

def readCSV(csv):
    text=open(csv).read().strip()
    loog=text.split('\n')
    log=[]
    for i in loog:
        log.append(i.split('|'))
    return log


def loggedIn():
    log=readCSV('files/loggedin.txt')
    for i in log:
        if i[0]==user and i[1]==id and i[2]==ip:
            return True
    return False

def logOut(theUser):
    log=readCSV('files/loggedin.txt')
    for i in log:
        if i[0]==theUser:
            log.remove(i)
    newLoggedin=open('files/loggedin.txt','w')
    for i in log:
        newLoggedin.write("|".join(i) +"\n")
    newLoggedin.close()

def makePage():
    retS=topHtml
    if logOuts:
        logOut(user)
    if checkAll():
        logIn()
        retS+='''

<div id="header"><h1><font face="Courier"><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></font></h1></div>


'''
        retS+='<div id="par">'
        retS+= 'Congratulations ' + user + '! You have succesfully logged in!<br><br>Click <a href="forum.py?user=' + user + '&id=' + id + '">\
                here</a> to begin using our page.<br>'
        retS+=notify()
        retS+='</div>'
    else:
        if user not in userPazzs:
            retS+=''
        elif logOuts:
            retS+='You have successfully logged out.'
        elif userPazzs[user]!=pazz:
            retS+='<center>Incorrect Username/Password. Try again:</center>'
        retS+= '''

<body>

<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>




        <div id="table">
        <form method="POST" action="logIn.py"><table>
       <tr><th><font size="6px">Log In</font></th></tr>
       <tr><td> <input type="text" name="user" placeholder="Username" style="height: 35px; width: 260px;" required></td></tr>
       <tr><td> <input type="password" name="pazz" placeholder="Password" style="height: 35px; width: 260px;" required></td></tr>
        <tr><td><input type="submit"></div></center></table></form><br><br><br><br><br><br>
       <center><h3>Don\'t have an account? Sign up <a href="./signUp.py">here</a>! It's free.</h3></center>
       <center><h3>Change your password <a href="./passChange.py">here</a></h3></center>
        
       
</div>'''
    return retS+bottomHtml



def notify():
  files=[]
  notifs=readCSV("files/notif.txt")
  if len(notifs)!=1 and notifs[0][0]!='':
    for line in notifs:
        if line[0]==user:
            files.append(line[1])
            notifs.remove(line)
    for pos in range(len(notifs)):
        notifs[pos]='|'.join(notifs[pos])
    if len(notifs)!=1:
        notifs='\n'.join(notifs)
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
