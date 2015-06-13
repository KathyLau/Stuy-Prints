#!/usr/bin/env python
print "Content-type: text/html\n"
print '''<html><head>
   <link rel="icon" href="http://stuy.enschool.org/favicon.ico" type="image/x-icon">
<link rel="stylesheet" type="text/css" href="style.css"></head><body>
    <script type="text/javascript" src="js/tinymce.min.js"></script>
    <script type="text/javascript">'''
import cgi, os
import commands
import cgitb
cgitb.enable()
posted=False
form = cgi.FieldStorage()
keys=form.keys()
print keys

ip=os.environ["REMOTE_ADDR"]

if "user" in keys:
    user=form['user'].value 
if "id" in keys:
    id=form['id'].value
if 'post' in keys:
    post=form['post'].value
    posted=True
if 'postNum' in keys:
    postNum=form['postNum'].value

def readCSV(csv):
    text=open(csv).read().strip()
    log=text.split('\n')
    logList=[]
    for a in log:
        logList.append(a.split('|'))
    return logList

# Test if the file was uploaded
def loggedIn():
    logg=readCSV('files/loggedin.txt')
    for a in logg:
        if a[0]==user and a[1]==id and a[2]==ip:
            return True
    return False

def writeCSVline(L):
    return "|".join(L) + '\n'


import datetime   
n=str(datetime.datetime.now())[:-7]



def printPost():
    ans=''
    if posted:
      ans='Your comment has been posted.'
    ans+= '''
tinymce.init({
    selector: "textarea",
    theme: "modern",
    width: 730,
    height: 100,
    plugins: [
        "advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code fullscreen media nonbreaking",
        "insertdatetime table contextmenu directionality emoticons template paste textcolor"
    ],
    content_css: "css/content.css",
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | l ink image | print preview media fullpage | forecolor backcolor emoticons",
});
</script>
<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
 <div id="bar" style="float: right">
            <ul class="sidebar">
                <li><a class="bar_element" href="forum.py?user=''' + user +'&id=' + id + '''&logIn=True">Home</a> </li>
                <br><li><a class="bar_element" href="rules.py?user=''' + user +'&id=' + id + '''&logIn=True">Rules</a> </li>
                <br><li><a class="bar_element" href="next.py?user=''' + user +'&id=' + id + '''&logIn=True">Questions?</a> </li>
                <br><li><a class="bar_element" href="main.py?user=''' + user +'&id=' + id + '''&logIn=True">Upload Something</a> </li>
                <br><li><a class="bar_element" href="account.py?user=''' + user +'&id=' + id + '''&logIn=True">View Uploads</a> </li>
                <br><li><a class="bar_element" href="logIn.py?user=''' + user + '&id=' + id + '''&logOut=True">Log Out</a> </li>
                           </ul></p>
            </div>
                <form method="POST" action="next.py?user=''' + user + '&id=' + id +'&postNum='+postNum+'''&logIn=True">
                    <textarea name="post" style="width:60% height:20%"></textarea>
                  <input type="submit" name="Submit" value="Post">
                </form>
           '''   
    if posted:
      f=open('files/posts.txt','a')
      f.write(user+'|'+post+'|'+n+ '|'+str(postNum)+'\n')
      f.close()
      f=open('files/posts.txt')
      data=f.read()
      f.close()
      pos=data.find('\n')
      data=str(postNum)+data[pos:]
      f=open('files/posts.txt','w')
      f.write(data)
      f.close()
    print ans






def printPage():
    ans=''
    if posted:
      ans='Your post has been posted.'
    ans+= '''
tinymce.init({
    selector: "textarea",
    theme: "modern",
    width: 730,
    height: 100,
    plugins: [
        "advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code fullscreen media nonbreaking",
        "insertdatetime table contextmenu directionality emoticons template paste textcolor"
    ],
    content_css: "css/content.css",
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | l ink image | print preview media fullpage | forecolor backcolor emoticons",
});
</script>
<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
 <div id="bar" style="float: right">
            <ul class="sidebar">
                <li><a class="bar_element" href="forum.py?user=''' + user +'&id=' + id + '''&logIn=True">Home</a> </li>
                <br><li><a class="bar_element" href="rules.py?user=''' + user +'&id=' + id + '''&logIn=True">Rules</a> </li>
                <br><li><a class="bar_element" href="next.py?user=''' + user +'&id=' + id + '''&logIn=True">Questions?</a> </li>
                <br><li><a class="bar_element" href="main.py?user=''' + user +'&id=' + id + '''&logIn=True">Upload Something</a> </li>
                <br><li><a class="bar_element" href="account.py?user=''' + user +'&id=' + id + '''&logIn=True">View Uploads</a> </li>
                <br><li><a class="bar_element" href="logIn.py?user=''' + user + '&id=' + id + '''&logOut=True">Log Out</a> </li>
                           </ul></p>
            </div>
                <form method="POST" action="next.py?user=''' + user + '&id=' + id + '''&logIn=True">
                    <textarea name="post" style="width:60% height:20%"></textarea>
                  <input type="submit" name="Submit" value="Post">
                </form>
           '''   
    if posted:
      postNum=int(readCSV('files/posts.txt')[0][0])
      f=open('files/posts.txt','a')
      f.write(user+'|'+post+'|'+n+ '|'+str(postNum)+'\n')
      postNum+=1
      f.close()
      f=open('files/posts.txt')
      data=f.read()
      f.close()
      pos=data.find('\n')
      data=str(postNum)+data[pos:]
      f=open('files/posts.txt','w')
      f.write(data)
      f.close()
    print ans

f=open('files/posts.txt','r')
p=f.readlines()

blacklist=[]

def printPageCont():
   try:
     for w in p[2:]:
       a=w.split('|')
       if a[3] not in blacklist:
         print '<div id="par3"><h3>'+a[1]+'</h3><BR>' + a[0]+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+a[2]+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'\
           +'View the whole post<a href="next.py?user='+user+'&id='+id+'&postNum='+a[3]+'&logIn=True">here</a><BR>'+'<HR></div>'
         blacklist.append(a[3]) 
       else: pass
   except: print ''


#def printPageCont():
#  try:
#    for w in p[2:]:
#      a=w.split('|')
#      print '<div id="par3"><h3>'+a[1]+'</h3><BR>' + a[0]+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+a[2]+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'\
#           +'View the whole post<a href="next.py?user='+user+'&id='+id+'&postNum='+a[3]+'&logIn=True">here</a><BR>'+'<HR></div>' 
#  except: print''

def printPostCont():
  try:
    for w in p[2:]:
      a=w.split('|')
      if str(a[3].strip('\n'))==str(postNum):
        print '<div id="par3"><h3>'+a[1]+'</h3><BR>' + a[0]+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'+a[2]+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'\
           +'<BR>'+'<HR></div>' 
  except: print''

f.close()

if loggedIn() and ('postNum' not in keys):
  printPage()
  printPageCont()
elif loggedIn() and ('postNum' in keys):
  printPost()
  printPostCont()
else:
  print "please login"




print '''<br><br>
Go Back <a href="forum.py?user=''' + user + '&id=' + id + '''&logIn=True">here</a>.
'''
print "</body></html>"




