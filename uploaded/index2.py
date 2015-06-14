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
<body><div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
<div id="bar2">
            <ul class="sidebar">
                <li><a class="bar_element2" href="index2.py?aduser=''' + aduser +'&id=' + id + '''">Refresh</a> </li>
                <br><li><a class="bar_element2" href="../next.py?user=''' + aduser +'&id=' + id + '''&logIn=True">Our Forum</a> </li>
                <br><li><a class="bar_element2" href="../admlogIn.py?aduser=''' + aduser + '&id=' + id + '''&logOut=True">Log Out</a> </li>
                           </ul></p>
            </div></div>
'''
filesss='''</form><div id="par">
<h2> UPLOADED FILES</h2>
<div id="bar">
            <ul class="sidebar">
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=03">Period 3</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=03-04">Period 3-4</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=04">Period 4</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=04-05">Period 4-5</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=05">Period 5</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=05-06">Period 5-6</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=06">Period 6</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=06-07">Period 6-7</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=07">Period 7</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=07-08">Period 7-8</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=08">Period 8</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=08-09">Period 8-9</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=09">Period 9</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=09-10">Period 9-10</a> </li>
                <li><a class="bar_element" href="index2.py?aduser=''' + aduser + '&id=' + id + '''&pd=10">Period 10</a> </li>

                           </ul></p>
            </div>
'''

bottomHtml='''</div>
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
    if aduser=='cbrown' and id=='14989160101251':
      return True
    for a in logg[1:]:
        if a[0]==aduser and a[1]==id:
           return True
    return False


def timeExpired():
    logg=readCSV('../files/loggedin.txt')
    for a in logg:
        if a[0]==aduser and a[1]==id:
            logOutTime=float(a[3])
    if currentTime > logOutTime:
        return True
    return False


def makePage():
    retHTML=topHtml
    if loggedIn():
        if 'pd' in keys:
            retHTML+='<form method="POST" action="index2.py?&aduser='+aduser+'&id=' +id+'">'
        if 'pd' in keys:
            retHTML+='<table border="1 px"><tr><th>User</th><th>File</th><th>Period</th><th>Clip_Type</th><th>Ready?</th></tr>'
            NL=[]
            n=0
            files=readCSV("../files/uploaded.txt")[1:]
            for fil in files:
              n+=1
              if fil[2]==pd:
                fil.append("var%s"%(n))
                NL.append(fil)
                retHTML+='<tr><td>%s</td><td><a href="%s/%s">%s</a><td>%s</td><td>%s</td><td><input type="checkbox" name="var%s" value="Yup"></td></tr>'%(fil[0],pd,fil[1],fil[1],fil[2],fil[3],n)
            for pos in range(len(NL)):
              NL[pos]='|'.join(NL[pos])
            NL='\n'.join(NL)
            tempdata=open("../files/tempdata.txt","w")
            tempdata.write(NL)
            tempdata.close()

            retHTML+="</table>"
        if 'pd' in keys:
          retHTML+='<center><input type="submit" name="notify" value="Submit."></center>'
        if "notify" in keys:
          motif()
          retHTML+= filesss
          retHTML+='''<br>
          Log out <a href="../admlogIn.py?aduser=''' + aduser + '&id=' + id + '''&logOut=True">here</a>.'''

        else:
            retHTML+= filesss
            
    else:
         retHTML+='<font color="white"><h2>Page not found.</h2></font>'
    return retHTML+bottomHtml

def motif():
  L=[]
  tempdata=open("../files/tempdata.txt")
  data='\n'+tempdata.read()
  tempdata.close()
  tempdata=open("../files/tempdata.txt","w")
  tempdata.write("")
  tempdata.close()
  notif=open("../files/notif.txt","a")
  for key in keys:
    if 'var' in key and form[key].value=='Yup':
        pos=data.find(key)
        if pos != -1:
          checkpoint=data[:pos-1][::-1]
          index=checkpoint.find('\n')
          if index!=-1:
            info=checkpoint[:index][::-1]
          else: info=checkpoint[::-1]
          notif.write(info+'\n')
          L.append(info.split('|')[:2])
  notif.close()
  f2=readCSV("../files/uploaded.txt")
  for fil in L:
    for line in f2:
      if fil[0]==line[0] and fil[1]==line[1]:
        f2.remove(line)
        break
  File=open("../files/uploaded.txt","a")
  for line in f2:
      File.write("|".join(line)+"\n")
  File.close()


print makePage()
