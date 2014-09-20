#!/usr/bin/python2

# -*- coding: utf-8 -*-
# bugfix 30/05/2012
import BeautifulSoup
import datetime
import locale
import httplib
import urllib
import sys
import os
import codecs
import getpass

# Change the output directory to what you want
OUTPUT_DIR = "/home/tap/backup/myopera/blog_backup" + os.path.sep

# If you have more than 5000 post in your blog, change it
MAX_POST = "5000"


# html template
html = """<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>%s</title>
  </head>
  <body>
    <h1>%s</h1>
    <h3>%s</h3>
    %s
  </body>
</html>"""

# Functions to display download progress
opener = urllib.FancyURLopener({})

def _reporthook(numblocks, blocksize, filesize, url=None):
    chars = "-\|/"
    sys.stdout.write("\b"*13 + "Downloading " + chars[numblocks % 4])
    sys.stdout.flush()

def geturl(url, dst, data=None):
    url = "http://my.opera.com" + url
    if sys.stdout.isatty():
        opener.retrieve(url, dst,
                        lambda nb, bs, fs, url=url: _reporthook(nb,bs,fs,url),
                        data)
        sys.stdout.write('\n')
    else:
        opener.retrieve(url, dst)
        
# I don't like urllib but httplib failed getting complete image files
def savefile(url):
    fpath = httplib.urlsplit(url)[2]
    fname = fpath.rsplit("/", 1)[1]
    spath = "files"
    if fname.find(".") != -1:
        ext = fname.rsplit(".", 1)[1]
        if ext.lower() in ["gif", "jpg", "jpeg", "png", "bmp", "tiff", "svg"]:
            spath = "images"
    spath += os.path.sep + fname
    try:
        opener.retrieve(url, filename=OUTPUT_DIR + spath)
    except IOError, err:
        fdlog = open("logfile.txt", "a+")
        fdlog.write("Fetching " + url + " raised\n")
        fdlog.write(err.__str__())
        fdlog.write("\n")
        fdlog.close()
    return spath


# MyOpera operations
class myopera:
    headers = {"Content-type": "text/xml", "Accept": "text/plain"}
    url = ""
    username = ""
    password = ""
    blogid = ""
    host = "my.opera.com"
    path = ""
    furl = ""
    blogname = ""

    blogger_body = """<?xml version="1.0"?>
<methodCall>
  <methodName>%s</methodName>
  <params>
    <param><value><string></string></value></param>
    <param><value><string>%s</string></value></param>
    <param><value><string>%s</string></value></param>
  </params>
</methodCall>"""
    
    def login(self, uname, pwd):
        self.username = uname
        self.password = pwd
        self.path = "/%s/blog/api/" % uname
        self.furl = "http://files.myopera.com/%s/" % uname
        
    def setInfo(self, d):
        self.blogid = d[u"blogid"]
        self.blogname = d[u"blogName"]
        self.headers["Referer"] = d[u"url"]
        opener.addheader("Referer", d[u"url"])
        self.url = d[u"url"] + "api/"
        split = httplib.urlsplit(self.url)
        self.host = split[1]
        self.path = split[2]
        
    def sendreq(self, body):
        conn = httplib.HTTPConnection(self.host)
        conn.request("POST", self.path, body, self.headers)
        response = conn.getresponse()
#        print response.status, response.reason
        data = response.read()
        conn.close()
        return data
        
    def getUserBlogs(self):
        req = self.blogger_body % ("blogger.getUsersBlogs", self.username, self.password)
        return self.sendreq(req)

    def getUserInfo(self):
        req = self.blogger_body % ("blogger.getUserInfo", self.username, self.password)
        return self.sendreq(req)

    def getRecentPosts(self, nb_posts=10, outputfile=None):
        body = """<?xml version="1.0" encoding="utf-8"?>
<methodCall>
  <methodName>metaWeblog.getRecentPosts</methodName>
  <params>
    <param>
      <value>
  <int>%s</int>
      </value>
    </param>
    <param>
      <value>
  <string>%s</string>
      </value>
    </param>
    <param>
      <value>
  <string>%s</string>
      </value>
    </param>
    <param>
      <value>
  <int>%s</int>
      </value>
    </param>
  </params>
</methodCall>"""
        req = body % (self.blogid, self.username, self.password, str(nb_posts))
        geturl(self.url, outputfile, req)
#        return self.sendreq(req)
        return True

    def getCategoryList(self):
        body = """<?xml version="1.0" encoding="utf-8"?>
<methodCall>
  <methodName>mt.getCategoryList</methodName>
  <params>
    <param>
      <value>
  <int>%s</int>
      </value>
    </param>
    <param>
      <value>
  <string>%s</string>
      </value>
    </param>
    <param>
      <value>
  <string>%s</string>
      </value>
    </param>
  </params>
</methodCall>"""
        req = body % (self.blogid, self.username, self.password)
        return self.sendreq(req)


# Return index table of all needles found in haystack
def findall(haystack, needle):
    i = -1
    l = []
    while True:
        i = haystack.find(needle, i + 1)
        if i == -1:
            break
        l.append(i)
    return l

# extrack bbcode
def extract(haystack, tags, closing=None):
    tags_index = {}
    for tag in tags:
        for x in findall(haystack, "[" + tag):
            if x not in tags_index.keys():
                tags_index[x] = tag

    if closing == None and len(tags) == 1:
        tag_end   = findall(haystack, "[/" + tags[0] + "]")
    else:
        tag_end   = findall(haystack, "[/" + closing + "]")
    bkt_end = findall(haystack, "]")
    
    tag_start = tags_index.keys()
    tag_start.sort()
    
    d = []
    for i in tag_start:
        nexts = [x for x in tag_start if x > i + 1]
        ends = [x for x in tag_end if x > i+1]
        closes = [x for x in bkt_end if x > i+1]
        url = None
        content = None
        decal = len(tags_index[i]) + 1

        
        if closes == []:
            print "error"
        else:
            close = closes[0]

        if ends != []: # found a [/tag] closing tag
            end = ends[0]
            if nexts != []: # found a next [tag] opening tag
                next = nexts[0]
                
                if end < next: # match the current opening tag
                    url = haystack[i + decal : close]
                    content = haystack[close + 1 : end]
                elif end > next: # doesn't match, no content
                    url = haystack[i + decal : close]
            else: # no next [tag] opening tag
                url = haystack[i + decal : close]
                content = haystack[close + 1 : end]

        else: # no [/tag] closing tag
            url = haystack[i + decal : close]
        
        if url == "":
            url = None
        d.append((tags_index[i], url, content))
    return d

# <member> = tuple name / value
def processMember(memberTag):
    d={}
    k = memberTag.find("name").next
    if memberTag.find("value").findChild(text=None) == None:
        v = memberTag.find("value").findChild(text=True).strip()
    else:
        v = memberTag.find("value").findChild(text=None).next.strip()
    d[k] = v
    if k == u"userid":
        return {}
    return d
    
def processPost(structTag):
    post_data = {}
    for x in structTag.findAll("member"):
        post_data.update(processMember(x))
    return post_data

# Taken from http://code.activestate.com/recipes/168639/
class progressBar:
  prev_percent = 0

  def __init__(self, minValue = 0, maxValue = 10, totalWidth=12):
    self.progBar = "[]"   # This holds the progress bar string
    self.min = minValue
    self.max = maxValue
    self.span = maxValue - minValue
    self.width = totalWidth
    self.amount = 0       # When amount == max, we are 100% done 
    self.updateAmount(0)  # Build progress bar string

  def updateAmount(self, newAmount = 0):
    if newAmount < self.min: newAmount = self.min
    if newAmount > self.max: newAmount = self.max
    self.amount = newAmount

    # Figure out the new percent done, round to an integer
    diffFromMin = float(self.amount - self.min)
    percentDone = (diffFromMin / float(self.span)) * 100.0
    percentDone = round(percentDone)
    percentDone = int(percentDone)
    if percentDone > self.prev_percent:
        self.prev_percent = percentDone
        sys.stdout.flush()

    # Figure out how many hash bars the percentage should be
    allFull = self.width - 2
    numHashes = (percentDone / 100.0) * allFull
    numHashes = int(round(numHashes))

    # build a progress bar with hashes and spaces
    self.progBar = "[" + '#'*numHashes + ' '*(allFull-numHashes) + "]"

    # figure out where to put the percentage, roughly centered
    percentPlace = (len(self.progBar) / 2) - len(str(percentDone)) 
    percentString = str(percentDone) + "%"

    # slice the percentage into the bar
    self.progBar = self.progBar[0:percentPlace] + \
            percentString + self.progBar[percentPlace+len(percentString):]

  def __str__(self):
    return str(self.progBar)

print "###############################"
print "# MyOpera blog backup utility #"
print "#    devloop   -   08/2010    #"
print "###############################"
print "Enter your MyOpera credentials"
op = myopera()
op.login(raw_input("Username: "), getpass.getpass(prompt="Password: "))

print "Login..."
BeautifulSoup.BeautifulStoneSoup.NESTABLE_TAGS["value"]=["param","data","member"]
buff = op.getUserBlogs()
if buff.find("faultCode") != -1:
    print "Error occured :"
    print buff
    sys.exit()

soup = BeautifulSoup.BeautifulStoneSoup(buff)
structs = soup.findAll("struct")
blog_info = processPost(structs[0])
op.setInfo(blog_info)
#print op.getUserInfo()

op.getRecentPosts(MAX_POST, "backup.xml")

fd = open("backup.xml")
buff = fd.read()
fd.close()
print "Data dumped!"

# To get the correct locale
lang = locale.setlocale(locale.LC_ALL, '')


sys.stdout.write("Parsing xml data... ")
sys.stdout.flush()
soup = BeautifulSoup.BeautifulStoneSoup(buff)
print "done"
structs = soup.findAll("struct")

# Prepare the new internal links and folders
url_rewrite = {}
sys.stdout.write("Creating directories... ")
sys.stdout.flush()
os.makedirs(OUTPUT_DIR + "files")
os.makedirs(OUTPUT_DIR + "images")
for x in structs:
    post = processPost(x)
    t = datetime.datetime.strptime(post[u"dateCreated"],"%Y%m%dT%H:%M:%S")

    path = t.strftime("%Y!%m!%d!").replace("!", os.path.sep)
    if not os.path.isdir(OUTPUT_DIR + path):
        os.makedirs(OUTPUT_DIR + path)
    path += post[u"link"].rsplit('/', 1)[1]
    path += ".html"
    url_rewrite[post[u"link"]] = path
print "done"

print "Fetching blog entries..."
up = os.path.sep.join([".."]*3) + os.path.sep
i = 0
prog = progressBar(0, len(structs), 77)

index_body = ""
current_month = ""

for x in structs:
    post = processPost(x)
    buff = post[u"description"]
#    print post[u"link"].rsplit('/', 1)[1]

    for t, k, v in extract(buff, ["IMG=", "IMGLEFT=", "IMGRIGHT="], "IMG"):
        before = ""
        after = ""
        if v == None:
            #buff = buff.replace("["+t+"="+k+"]", "<img src=\""+k+"\" />")
            before = "["+t+k+"]"
            if k.startswith(op.furl):
                if k not in url_rewrite.keys():
                    u = savefile(k)
                    url_rewrite[k] = u
                    k = up + u
            after = "<img src=\""+k+"\" />"
        else:
            before = "["+t+k+"]"+v+"[/IMG]"
            if k.startswith(op.furl):
                if k not in url_rewrite.keys():
                    u = savefile(k)
                    url_rewrite[k] = u
                    k = up + u
            after = "<img src=\"" + k + "\" /> " + v
        buff = buff.replace(before, after)
        
    for t, k, v in extract(buff, ["URL=", "URL"], "URL"):
        before = ""
        after = ""
        if k == None:
            if v == None:
                print "error"
                continue

            else: # [URL]v[/URL]
                before = "["+t+"]"+v+"[/URL]"
                if v in url_rewrite.keys():
                    v = up + url_rewrite[v]
                    
                elif v.startswith(op.furl):
                    u = savefile(v)
                    url_rewrite[v] = u
                    v = up + u
                after = "<a href=\""+v+"\">"+v+"</a>"
        else:
            if v == None: # [URL=k]
                before = "["+t+k+"]"
                if k in url_rewrite.keys():
                    k = up + url_rewrite[k]
                    
                elif k.startswith(op.furl):
                    u = savefile(k)
                    url_rewrite[k] = u
                    k = up + u
                after = "<a href=\""+k+"\">"+k+"</a>"
                
            else: # [URL=k]v|/URL]
                before = "["+t+k+"]"+v+"[/URL]"
                if k in url_rewrite.keys():
                    k = up + url_rewrite[k]
                    
                elif k.startswith(op.furl):
                    u = savefile(k)
                    url_rewrite[k] = u
                    k = up + u
                if v in url_rewrite.keys():
                    v = up + url_rewrite[v]
                after = "<a href=\""+k+"\">"+v+"</a>"

        buff = buff.replace(before, after)
        
    for t, k, v in extract(buff, ["EMAIL=", "EMAIL"], "EMAIL"):
        if k == None:
            if v == None:
                print "error"
                continue
            else:
                buff = buff.replace("["+t+"]"+v+"[/EMAIL]", "<a href=\"mailto:"+v+"\">"+v+"</a>")
        else:
            if v == None:
                buff = buff.replace("["+t+k+"]", "<a href=\"mailto:"+k+"\">"+k+"</a>")
            else: # [URL=k]v|/URL]
                buff = buff.replace("["+t+k+"]"+v+"[/EMAIL]", "<a href=\"mailto:"+k+"\">"+v+"</a>")
                
                        
    buff = buff.replace("[I]","<i>").replace("[/I]","</i>")
    buff = buff.replace("[B]","<b>").replace("[/B]","</b>")
    buff = buff.replace("[U]","<u>").replace("[/U]","</u>")
    buff = buff.replace("[QUOTE]","<blockquote>").replace("[/QUOTE]","</blockquote>")
    buff = buff.replace("[CODE]","<pre>").replace("[/CODE]","</pre>")
    buff = buff.replace("\n", "<br />")
# TODO : [VIDEO] and [ALIGN] (left, center, right, justify)
    
    for t, k, v in extract(buff, ["LIST=", "LIST"], "LIST"):
        if v == None:
            continue
        
        elems = v.split("[*]")[1:]
        if k == "a": # Alphabetical list
            rstr = "<ol class=\"alpha\"><li>" + "</li><li>".join(elems) + "</li></ol>"
            buff = buff.replace("[LIST=a]"+v+"[/LIST]", rstr)
        elif k == "1": # Numerical list
            rstr = "<ol><li>" + "</li><li>".join(elems) + "</li></ol>"
            buff = buff.replace("[LIST=1]"+v+"[/LIST]", rstr)
        else: #Unordered list
            rstr = "<ul><li>" + "</li><li>".join(elems) + "</li></ul>"
            buff = buff.replace("[LIST]"+v+"[/LIST]", rstr)
            
    t = datetime.datetime.strptime(post[u"dateCreated"],"%Y%m%dT%H:%M:%S")
    if lang.startswith("French"):
        clockdate = t.strftime("Le %A %d %B %Y ") # French
        clocktime = t.strftime(" %H:%M")
        clock  = unicode(clockdate, locale.getlocale()[1])
        clock += unichr(224)
        clock += unicode(clocktime, locale.getlocale()[1])
    else:
        clock = unicode(t.strftime("%A %c").capitalize(), locale.getlocale()[1])
        
    if current_month != t.strftime("%B %Y"):
        current_month = t.strftime("%B %Y")
        index_body += "<h3>%s</h3>\n" % (
            unicode(current_month.capitalize(), locale.getlocale()[1]))
    
    index_body += "%02d - <a href=\"%s\">%s</a><br />\n" % (
                    t.day, url_rewrite[post[u"link"]], post[u"title"])
    
    page = html % (post[u"title"], post[u"title"], clock, buff)
    fd = codecs.open(OUTPUT_DIR + url_rewrite[post[u"link"]],"w","utf-8")
    fd.write(page)
    fd.close()
    i += 1
    prog.updateAmount(i)
    print prog, "\r",

page = html % (op.blogname, op.blogname, u"Blog Archive", index_body)
fd = codecs.open(OUTPUT_DIR + "index.html","w","utf-8")
fd.write(page)
fd.close()
print "\nBackup done"

if os.path.isfile("logfile.txt"):
    print "Some errors occured. Please check logfile.txt."
