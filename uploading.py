#!/usr/bin/env python
print """\
Content-Type: text/html\n
<html><body>
</body></html>
""" 
import cgi, os
import commands
import cgitb
cgitb.enable()

form = cgi.FieldStorage()
keys=form.keys()

ip=os.environ["REMOTE_ADDR"]

if "user" in keys:
    user=form['user'].value 
if "id" in keys:
    id=form['id'].value
rm=form['rm'].value
# A nested FieldStorage instance holds the file
fileitem = form['file']
pd=form['pd'].value
fl=form['fl'].value

def readCSV(csv):
    text=open(csv).read().strip()
    log=text.split('\n')
    logList=[]
    for a in log:
        logList.append(a.split(','))
    return logList

# Test if the file was uploaded
def loggedIn():
    logg=readCSV('files/loggedin.txt')
    for a in logg:
        if a[0]==user and a[1]==id and a[2]==ip:
            return True
    return False


if loggedIn():
  if fileitem.filename:
     bool=True
   # strip leading path from file name to avoid directory traversal attacks
     fname = os.path.basename(fileitem.filename)
     if ' ' in fname or '/' in fname or ',' in fname or '@' in fname or '#' in fname or '%' in fname or '$' in fname:
       print 'Bad characters in file name. Rename pls.'
     open('uploaded/'+pd+'/'+fname, 'wb').write(fileitem.file.read())
     if 'Microsoft Word'not in commands.getoutput("file uploaded/"+pd+"/"+fname) and 'Microsoft Office Word' not in commands.getoutput("file uploaded/"+pd+"/"+fname)and'HTML' not in commands.getoutput("file uploaded/"+pd+"/"+fname)and'ASCII text' not in commands.getoutput("file uploaded/"+pd+"/"+fname) and 'UTF' not in commands.getoutput("file uploaded/"+pd+"/"+fname)and 'PDF' not in commands.getoutput("file uploaded/"+pd+"/"+fname):
       message= 'File type not accepted'
       os.remove("uploaded/"+pd+'/'+fname)
       bool=False
     elif bool:
       size= commands.getoutput("du -h "+ "uploaded/"+pd+'/'+fname)
       if 'M' in size:
         K= size[:size.find('M')]
         if float(K) > 60:
           message= 'File size not accepted'
           os.remove("uploaded/"+pd+'/'+fname)
           bool=False
         else:
           message = 'The file "' + fname + '" was uploaded successfully'
           open('files/uploaded.txt','a').write(','.join([user,fname,pd,rm])+'\n')
       else: 
         message = 'The file "' + fname + '" was uploaded successfully'
         open('files/uploaded.txt','a').write(','.join([user,fname,pd,rm])+'\n')
       
  else:
     message = 'No file was uploaded'
else:
  message= 'Log in to view'
  
print message
print '''<br><br>
Go Back <a href="main.py?user=''' + user + '&id=' + id + '''&logIn=True">here</a>.
'''





