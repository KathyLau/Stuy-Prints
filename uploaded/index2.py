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

if "aduser" in keys:
    aduser=form['aduser'].value 
if "id" in keys:
    id=form['id'].value
if "pd" in keys:
    pd=form['pd'].value
  
topHtml='''<!DOCTYPE HTML><html>
<head>
   <title>Main Page</title>
   <link rel="stylesheet" type="text/css" href="style2.css"> 
</head>
<body><div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>'''

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
filesss='''
<h2> UPLOADED FILES</h2>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=03">Period 3</a><br>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=04">Period 4</a><br>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=05">Period 5</a><br>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=06">Period 6</a><br>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=07">Period 7</a><br>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=08">Period 8</a><br>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=09">Period 9</a><br>
<a href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=10">Period 10</a><br>

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
        logList.append(a.split('|'))
    return logList

def loggedIn():
    logg=readCSV('../files/loggedin.txt')
    for a in logg[1:]:
        if a[0]==aduser and a[1]==id and a[2]==ip:
            return True
    return False


def timeExpired():
    logg=readCSV('../files/loggedin.txt')
    for a in logg:
        if a[0]==aduser and a[1]==id and a[2]==ip:
            logOutTime=float(a[3])
    if currentTime > logOutTime:
        return True
    return False


def makePage():
    retHTML=topHtml
    if loggedIn():
        if timeExpired():
            retHTML+='''<h2>The time limit on your account has expired. 
                            Please click <a href="../admlogIn.py?aduser=''' + aduser + '&id=' + id +'''&logOut=True">here</a> 
                            to relogin.</h2>
            '''
        if 'pd' in keys:
          retHTML+='<form method="POST" action="index2.py?&aduser='+aduser+'&id=' +id+'">'
        if 'pd' in keys and pd=='03':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='03':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="03/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"
            retHTML+="</table>"
        elif 'pd' in keys and pd=='04':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='04':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="04/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"
            retHTML+="</table>"
        elif 'pd' in keys and pd=='05':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='05':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="05/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"
            retHTML+="</table>"
        elif 'pd' in keys and pd=='06':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='06':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="06/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"
            retHTML+="</table>"
        elif 'pd' in keys and pd=='07':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='07':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="07/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"
            retHTML+="</table>"
        elif 'pd' in keys and pd=='08':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='08':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="08/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"
            retHTML+="</table>"
        elif 'pd' in keys and pd=='09':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='09':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="09/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"

            retHTML+="</table>"
        elif 'pd' in keys and pd=='10':
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            for i in readCSV('../files/uploaded.txt')[1:]:
              if i[2]=='10':
                retHTML+='<tr><td>'+i[0]+ '</td><td>'+'<a href="10/' + i[1] + '">'+i[1]+'</a>' + "<td>"+i[2]+"</td>" +"<td>"+i[3]+"</td><td><input type='checkbox' name='ready' value='Yup'></td></tr>"
            retHTML+="</table>"
        if 'pd' in keys:
          retHTML+='<center><input type="submit" name="fred" value="Submit."></center>'

        else:
            retHTML+= filesss
            retHTML+='''<br>
            Log out <a href="../admlogIn.py?aduser=''' + aduser + '&id=' + id + '''&logOut=True">here</a>.

        '''
    else:
        retHTML+='<h2>Page not found.</h2>'
    return retHTML+'</form>'+bottomHtml


print makePage()



print makePage()
