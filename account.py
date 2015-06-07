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
               
        try:
            retHTML+='''
<form method="POST" action="uploaded/'''+ form['file'].value +'''">
<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
<div id="par2"><select name="file" size="1"><option selected>None</option>
'''         
            for w in readCSV('files/uploaded.txt'):
              if w[0]==user:
                retHTML+='<option>'+w[2]+'/'+w[1]+'</option>'
            retHTML+='''</select><br><br>
             
            <input type="submit" value="Send">
            </form>'''
        except:
          retHTML+='''
<form method="POST" action="account.py?user='''+user+'&id='+id+'''"'>
<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
<div id="par2"><select name="file" class="styled" onChange="document.location = this.value" value="GO"><option selected>None</option>
'''         
          for w in readCSV('files/uploaded.txt'):
              if w[0]==user:
                retHTML+='<option>'+w[2]+'/'+w[1]+'</option>'
          retHTML+='''</select><br><br>
          </form>

<br>
Log out <a href="logIn.py?user=''' + user + '&id=' + id + '''&logOut=True">here</a>.
        '''
    else:
        retHTML+='<h2>Page not found.</h2>'
    return retHTML+bottomHtml


print makePage()

#"account.py?user='''+user+'&id='+id+'''"'
#if "file" in keys:
#          print '''<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
#<h2>Your uploaded files: </h2><div id="par2">
#<a href="uploaded/'''+ form['file'].value +'''">''' +form['file'].value+"</a></div>"
