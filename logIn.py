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
        userPazzs[i]=userPazzs[i].split(',')
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
   <link rel="stylesheet" type="text/css" href="style.css"> 
</head>
<body>'''


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
    return ",".join(L) + '\n'

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
        log.append(i.split(','))
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
        newLoggedin.write(",".join(i) +"\n")
    newLoggedin.close()

def makePage():
    retS=topHtml
    if logOuts:
        logOut(user)
    if checkAll():
        logIn()
        retS+= 'Congratulations ' + user + '! You have succesfully logged in!<br>Click <a href="main.py?user=' + user + '&id=' + id + '">here</a> to begin using our page.<br>Click <a href="forum.py?user=' + user + '&id=' + id + '"here</a> to view our forum.'
    else:
        if user not in userPazzs:
            retS+='<b>STUY PRINTS</b>'
        elif logOuts:
            retS+='You have successfully logged out.'
        elif userPazzs[user]!=pazz:
            retS+='Incorrect Username/Password. Try again:'
        retS+= '''<br>
        <table><tr><th>Log In!</th></tr>
        <form method="POST" action="logIn.py">
       <tr><td> Username:</td><td> <input type="text" name="user"></td></tr>
       <tr><td> Password:</td><td> <input type="password" name="pazz"> </td></tr>
       <tr><td> <input type="submit"></tr></td>
        </form>
        </table>
        Don\'t have an account? Sign up <a href="signUp.py">here</a>! It's free.'''
    return retS+bottomHtml


print makePage()
