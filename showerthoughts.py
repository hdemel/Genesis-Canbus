import praw, json, sqlite3, time, os, subprocess

f = open('showerthoughts.txt', 'w')
reddit = praw.Reddit("/u/_Tuna_")
subreddit=reddit.get_subreddit('showerthoughts')

def addtodb(decimallist):	
	conn = sqlite3.connect('Canbus.db')
	c = conn.cursor()
	c.execute("INSERT INTO showerthoughts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (decimallist[0], decimallist[1], decimallist[2], decimallist[3], decimallist[4], decimallist[5], decimallist[6], decimallist[7], decimallist[8]))
	conn.commit()
	conn.close()

def cleartable():
	conn = sqlite3.connect('Canbus.db')
	c = conn.cursor()
	query = "DELETE FROM showerthoughts"
	c.execute(query)
	conn.commit()
	conn.close()

xmscreen = [6,10,0,0,0,0,40,0,0]
initializescreen = [480,10,29,52,10,1,1,14,20]
turnon = [100,'3f',0,0,0,0,0,0,0,]



for submission in subreddit.get_top_from_hour(limit=1):
	#print i
	#print len(submission.title)
	title = submission.title
	counter = len(title)
	userone = submission.author.name
	#print userone	
	cleartable()
	length = hex(len(title)).lstrip("0x")
	initializescreen[7] = length
	addtodb(turnon)
	addtodb(xmscreen)
	addtodb(initializescreen)
	i = 2
	k = 21
	decimalsplit = [480,00,00,00,00,00,00,00,00]
	print title
	split = list(title)
	for j in split:
		if i <= 8:
			val = ord(j)
			val = hex(val).lstrip("0x")
			##print val
			decimalsplit[i] = val
			i = i+1
		if i > 8:
			##newval = ord(j)
			##newval = hex(newval).lstrip("0x")
			decimalsplit[1] = k
			addtodb(decimalsplit)
			#print decimalsplit
			decimalsplit = [480,00,00,00,00,00,00,43,10]
			#decimalsplit[2] = val
			i = 2
			k = k+1
	decimalsplit[1] = k
	addtodb(decimalsplit)
	k = k+1
	decimalsplit = [480,00,00,00,00,00,00,00,00]
	decimalsplit[1] = k
	decimalsplit[2] = 46
	addtodb(decimalsplit)
	##print decimalsplit
	##time.sleep(1)
	os.system("sudo python timeset.py")
	time.sleep(0.5)
	##print decimalsplit
	