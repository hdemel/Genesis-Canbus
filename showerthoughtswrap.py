import praw, json, sqlite3, time, os, subprocess

f = open('showerthoughts.txt', 'w')
reddit = praw.Reddit("/u/flyingbrownie")
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
initializescreen = [480,10,29,52,10,2,1,14,20]
turnon = [100,'3f',0,0,0,0,0,0,0,]



for submission in subreddit.get_top_from_hour(limit=1):
	title = submission.title
	counter = len(title)/3 + 3
	userone = submission.author.name
	x = 1
	z = 0

	while x <= counter:
		cleartable()
		usedtitle = title[:23]
		length = 30
		hexlength = hex(length).lstrip("0x")
		
		initializescreen[7] = hexlength
		addtodb(turnon)
		addtodb(xmscreen)
		addtodb(initializescreen)
		i = 2
		k = 21
		decimalsplit = [480,00,20,20,20,20,20,20,20]
		print usedtitle
		split = list(usedtitle)
		for j in split:
			if i <= 8:
				val = ord(j)
				val = hex(val).lstrip("0x")
				decimalsplit[i] = val
				i = i+1
			if i > 8:
				decimalsplit[1] = k
				addtodb(decimalsplit)
				decimalsplit = [480,20,20,20,20,20,20,20,20]
				i = 2
				k = k+1
		decimalsplit[1] = k
		addtodb(decimalsplit)
		while k < 24:
			decimalsplit = [480,20,20,20,20,20,20,20,20]
			k = k + 1
			decimalsplit[1] = k
			addtodb(decimalsplit)
		decimalsplit = [480, 25, 20, 43, 10, '2f', 72, '2f', 73]
		addtodb(decimalsplit)
		split = list(userone)
		k = 26
		i = 7
		decimalsplit = [480, 26, 63, '6f', 77, 65, 72, 74, 68]
		addtodb(decimalsplit)
		decimalsplit = [480, 27, '6f', 75, 67, 68, 74, 0, 0]
		addtodb(decimalsplit)
		#decimalsplit = [480, 28, 20, 20, 20, 0, 0, 0, 0]
		#addtodb(decimalsplit)
		# for j in split:
		# 	if i <= 8:
		# 		val = ord(j)
		# 		val = hex(val).lstrip("0x")
		# 		decimalsplit[i] = val
		# 		i = i+1
		# 	if i > 8:
		# 		decimalsplit[1] = k
		# 		addtodb(decimalsplit)
		# 		decimalsplit = [480,20,20,20,20,20,20,20,20]
		# 		i = 2
		# 		k = k+1
		# decimalsplit[1] = k
		# addtodb(decimalsplit)
		os.system("sudo python timeset.py")
		if z == 0:
			time.sleep(3)
			z = 1
		title = title[3:]
		x = x+1
	
