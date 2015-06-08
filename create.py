#!/usr/bin/python
print "Content-Type: text/html\n"
print ""


import cgi, cgitb, os
cgitb.enable()
form =cgi.FieldStorage()
keys=form.keys()
user='test'
id='test'
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

def create_note():
    form="""
    tinymce.init({
    selector: "textarea",
    theme: "modern",
    width: 730,
    height: 400,
    plugins: [
        "advlist autolink link image lists charmap print preview hr anchor pagebreak spellchecker",
        "searchreplace wordcount visualblocks visualchars code fullscreen media nonbreaking",
        "insertdatetime table contextmenu directionality emoticons template paste textcolor"
    ],
    content_css: "css/content.css",
    toolbar: "insertfile undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | l ink image | print preview media fullpage | forecolor backcolor emoticons",
});
</script><body><center>
<div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
<h1>Remember to save your notes!</h1>
<form method="post" action="save.py?user="""+user+'&id='+id+'''">
    <input type="text" name="fname" size="100" placeholder="Title." required>
    <textarea name="body" style="width:100%"></textarea>
    <button type="submit" formaction="main.py" onclick="return confirm('Exit w/o saving?')">Go back</button>
    <input type="submit" value="Save note">
</form></center></body>
</html>'''
    return topHtml+form

if loggedIn():
  print create_note()
else:
  print topHtml+'''</script><body><div id="header"><h1><font color="#00BFFF">Stuy</font><font color="#ffffff"> Prints</font></h1></div>
<center><h2>Please log in</h2></center>
</body></html>'''
