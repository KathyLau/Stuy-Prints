#!/usr/bin/python
print "Content-type: text/html\n"
import smtplib
import random
import cgi, cgitb, md5; cgitb.enable()
form =cgi.FieldStorage()
keys=form.keys()

user=''
pazz=''
Rpas=''
if "user" in keys:
    user=form['user'].value
if "pazz" in keys:
    Opazz=form['pazz'].value
    pazz=md5.new(Opazz).hexdigest()
else:
    pazz=md5.new(pazz).hexdigest()
if "Rpas" in keys:
    Rpas=form['Rpas'].value
Rpas=md5.new(Rpas).hexdigest()



def checkForm():#checks to see if all information is allowed
    return "user" in keys and "pazz" in keys and "Rpas" in keys and pazz == Rpas 

def makeUserPazzDict():
    userPazzs=open('files/users.txt','r').read().strip().split('\n')
    for i in range(len(userPazzs)):
        userPazzs[i]=userPazzs[i].split('|')
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
        file=open('files/pending.txt','a')
        file.write(user + '|' + pazz + '|'+i +'\n' )
        file.close

def checks():
    return checkUserPazz() and checkForm() and checkSafeUser()

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
    if checks():
        email()
    else:
        if not checkUserPazz():
            ans+='Username Already Taken. Try again:<br>'
        if pazz != Rpas:
            ans+='Passwords do not match. Try again:<br>'
        if not checkSafeUser():
            ans+='No Special characters allowed. Try ' + altUser()
        ans+= '''<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
        <table><tr><th>Sign Up!</th></tr>
        <form method="POST" action="signUp.py">
       <tr><td> Email:</td><td> <input type="text" name="user" required>  </td></tr>
       <tr><td> Password:</td><td> <input type="password" name="pazz" required> </td></tr>
       <tr><td> Verify Password:</td><td> <input type="password" name="Rpas" required> </td></tr> 
       <tr><td> <input type="submit"></td></tr></table>
        </form></table><center><br><br><br><br><br><br><br><br><h3>
        Already have an account? Log in <a href="logIn.py">here</a></h3></center>'''
    return ans+bottomHtml


def randNum():
    n=''
    for i in range(4):
      n+=str(random.randrange(10))
    return n
i = randNum()

def email():
  ans=topHtml
  send=True
  TO=user 
  SUBJECT= "TEST"
  TEXT="Your user name is " + user + '.' + "Your verification id is " + i

  gmail_sender="imobilep501@gmail.com"
  gmail_passwd=''

  server= smtplib.SMTP('smtp.gmail.com',587)
  server.ehlo()
  server.starttls()
  server.ehlo
  server.login(gmail_sender, gmail_passwd)

  BODY='\r\n'.join([
       'To: %s' % TO,
       'From: %s' % gmail_sender,
       'Subject: %s' % SUBJECT,
       '',
       TEXT
       ])
  if user[-9:]=='@stuy.edu':
    try:
      server.sendmail(gmail_sender, TO, BODY)
      saveUserPazz()
      ans+='<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>'
      ans+= 'Thank you ' + user + '. Login <a href="logIn.py">here</a>'
      print 'email sent'
    except:
      print 'Error in sending email'
  else:
    print'Please use a stuy.edu email address'
    send=False
  server.quit()
  return send


print makePage()


