#!/usr/bin/python
print "Content-type: text/html\n"

import cgi, cgitb, md5; cgitb.enable()
form=cgi.FieldStorage()
keys=form.keys()
badChars="<>,|\\[]{}"

if form.has_key("user"):
    user=form["user"].value
if form.has_key("Opass"):
    Opass=form["Opass"].value
    Opass=md5.new(Opass).hexdigest()
if form.has_key("Npass"):
    Npass=form["Npass"].value
    Npass=md5.new(Npass).hexdigest()

def dataInput():
    return "user" in keys and "Opass" in keys and "Npass" in keys

def makeUserPazzDict():#Reused this
    userPazzs=open('files/users.txt','r').read().strip().split('\n')
    for i in range(len(userPazzs)):
        userPazzs[i]=userPazzs[i].split('|')
    d={}
    for i in userPazzs:
        d[i[0]]=i[1]
    return d

UserPass=makeUserPazzDict()#Dictionary containing User:Pass

def checkLanguage():
    for i in badChars:
        if i in Npass:
            return False
    return True

def checkUser():
    return user in UserPass

def checkOPass():
    return Opass == UserPass[user]

def editPass():
    DATA=open('files/users.txt','r')
    File=DATA.read()
    DATA.close()
    index=File.find(user+"|")+len(user)+1
    File=File[:index]+Npass+File[index+len(Opass):]
    FileW=open('files/users.txt','w')
    FileW.write(File)    

def PassorNah():
    return dataInput() and checkUser() and checkOPass()

topHtml='''<!DOCTYPE HTML><html>
<head>
   <title>sign up</title>
   <link rel="icon" href="http://stuy.enschool.org/favicon.ico" type="image/x-icon">
   <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>'''

bottomHtml='''</body>
</html>
'''

        
def makePage():
    ans=topHtml
    if PassorNah():
        editPass()
        ans+= 'Password Changed Successfully. Try logging in <a href="logIn.py">here</a>'
    else:
        if dataInput():
            if not checkUser():
                ans+='Not a valid username.<br>'
            else:
                if not checkOPass():
                    ans+='Incorrect password.<br>'
                else:
                    if Npass=='d41d8cd98f00b204e9800998ecf8427e':
                        ans+='Please input a new password.<br>'                    
        ans+= '''<table><tr><th>Password Change</th></tr>
        <form method="POST" action="passChange.py">
       <tr><td> Username:</td><td> <input type="text" name="user"> </td></tr>
       <tr><td> Password:</td><td> <input type="password" name="Opass"> </td></tr>
       <tr><td> New Password:</td><td> <input type="password" name="Npass"> </td></tr> 
       <tr><td> <input type="submit"></td></tr>
        </form></table>
        Don't know why you're here? Login <a href="logIn.py">here</a>'''
    return ans+bottomHtml

print makePage()
