#!/usr/bin/python
print "Content-Type: text/html\n"
print ""


import cgi, cgitb, os
cgitb.enable()
form =cgi.FieldStorage()
keys=form.keys()
print keys
ip=os.environ["REMOTE_ADDR"]
if "user" in keys:
    user=form['user'].value
if 'logOut' in keys:
    logOuts=True
if "id" in keys:
    id=form['id'].value

topHtml='''<!DOCTYPE html>
    <html>
   <title>Create a note</title>
   <link rel="icon" href="http://stuy.enschool.org/favicon.ico" type="image/x-icon">
   <link rel="stylesheet" type="text/css" href="style.css"> 
    <script type="text/javascript" src="js/tinymce.min.js"></script>
    <script type="text/javascript">
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

def save_note():
    note_title = form["fname"].value
    os.chdir("/home/students/2017/szeting.lau/public_html/project/users/")
    note_title += ".txt"
    note_body = form["body"].value
    note = open(note_title, "w")
    note.write(note_body)
    note.close()
    ret= '''Note saved! Click <a href="main.py?user='''+user+'&id=' +id+'''&logIn=True">here</a> to go back
           '''
    return ret

if loggedIn():
  print save_note()
else:
  print topHtml+'''</script><body><div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
<center><h2>Please log in</h2></center>
</body></html>'''
