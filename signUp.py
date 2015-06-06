#!/usr/bin/python
print "Content-type: text/html\n"

import cgi, cgitb, md5; cgitb.enable()
form =cgi.FieldStorage()
keys=form.keys()

user=''
pazz=''
Rpas=''
if "user" in keys:
    user=form['user'].value
if "pazz" in keys:
    pazz=form['pazz'].value
pazz=md5.new(pazz).hexdigest()
if "Rpas" in keys:
    Rpas=form['Rpas'].value
Rpas=md5.new(Rpas).hexdigest()

def checkForm():#checks to see if all information is allowed
    return "user" in keys and "pazz" in keys and "Rpas" in keys and pazz == Rpas 

def makeUserPazzDict():
    userPazzs=open('files/users.txt','r').read().strip().split('\n')
    for i in range(len(userPazzs)):
        userPazzs[i]=userPazzs[i].split(',')
    d={}
    for i in userPazzs:
        d[i[0]]=i[1]
    return d

userPazzs=makeUserPazzDict()

badChars="<>,|\\[]{}"
def checkSafeUser():
    for i in badChars:
        if i in user:
            return False
    return True
def altUser():
    ans=user
    for i in badChars:
        ans=ans.replace(i,'_')
    return ans

def checkUserPazz():
    return user not in userPazzs

def saveUserPazz():
    if checkForm():
        file=open('files/users.txt','a')
        file.write(user + ',' + pazz + '\n')
        file.close

def checks():
    return checkUserPazz() and checkForm() and checkSafeUser()

topHtml='''<!DOCTYPE HTML><html>
<head>
   <title>sign up</title>
   <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>'''

bottomHtml='''</body>
</html>
'''
        
def makePage():
    ans=topHtml
    if checks():
        saveUserPazz()
        ans+= 'Thank you ' + user + '. Login <a href="logIn.py">here</a>'
    else:
        if not checkUserPazz():
            ans+='Username Already Taken. Try again:<br>'
        if pazz != Rpas:
            ans+='Passwords do not match. Try again:<br>'
        if not checkSafeUser():
            ans+='No Special characters allowed. Try ' + altUser()
        ans+= '''<table><tr><th>Sign Up!</th></tr>
        <form method="POST" action="signUp.py">
       <tr><td> Username:</td><td> <input type="text" name="user"> </td></tr>
       <tr><td> Password:</td><td> <input type="password" name="pazz"> </td></tr>
       <tr><td> Verify Password:</td><td> <input type="password" name="Rpas"> </td></tr> 
       <tr><td> <input type="submit"></td></tr>
        </form></table>
        Already have an account? Log in <a href="logIn.py">here</a>'''
    return ans+bottomHtml


print makePage()
