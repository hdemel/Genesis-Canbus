import praw, json, sqlite3, time, os, subprocess, datetime

reddit = praw.Reddit("/u/flyingbrownie")
subreddit=reddit.get_subreddit('showerthoughts')

def addtodb(decimallist):	#This function takes the given list and inputs it into the SQL database
	conn = sqlite3.connect('Canbus.db')
	c = conn.cursor()
	c.execute("INSERT INTO showerthoughts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (decimallist[0], decimallist[1], decimallist[2], decimallist[3], decimallist[4], decimallist[5], decimallist[6], decimallist[7], decimallist[8]))
	conn.commit()
	conn.close()

def cleartable():	#This function flushes the SQL database and prepares it for a new list of CAN instructions
	conn = sqlite3.connect('Canbus.db')
	c = conn.cursor()
	query = "DELETE FROM showerthoughts"
	c.execute(query)
	conn.commit()
	conn.close()

def ReadSQL():	#This function transmits the CAN instructions into the CAN network
	conn = sqlite3.connect('Canbus.db')
	c = conn.cursor()
	cursor = c.execute("SELECT ident, a, b, c, d, e, f, g, h FROM showerthoughts")
	for row in cursor:
		ident = str(row[0]).zfill(3)	#The library I use only accepts three digit numbers. This pads the
		a = str(row[1]).zfill(2)		#numbers with extra zeroes using zfill if required
		b = str(row[2]).zfill(2)
		c = str(row[3]).zfill(2)
		d = str(row[4]).zfill(2)
		e = str(row[5]).zfill(2)
		f = str(row[6]).zfill(2)
		g = str(row[7]).zfill(2)
		h = str(row[8]).zfill(2)

		command = "cansend can0 %s#%s.%s.%s.%s.%s.%s.%s.%s" % (ident, a, b, c, d, e, f, g, h)
		print
		command
		os.system(command)
		conn.close()

xmscreen = [6,10,0,0,0,0,40,0,0]	#This variable holds the instruction to draw the XM screen
initializescreen = [480,10,29,52,10,2,1,14,20]	#This variable holds the instruction to "prime" the screen
turnon = [100,'3f',0,0,0,0,0,0,0,]	#This variable holds the instruction to power up the screen



for submission in subreddit.get_top_from_hour(limit=1):	#This retrieves the highest rated "shower thought" of the hour from reddit
	title = submission.title							#and stores it in a variable.
	counter = len(title)/3 + 3	#This determines how many times the screen needs to be redrawn to scroll the whole message across
	userone = submission.author.name	#Still figuring out how to have this list as the "artist" so it shows on my screen
	x = 1	#Counter
	z = 0	#Counter

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
		#os.system("sudo python timeset.py")
		gennytime = [502, (time.strftime("%I")), (time.strftime("%M")), 00, 00, 00, 00, 00, 00]
		addtodb(gennytime)
		if z == 0:
			time.sleep(3)
			z = 1
		title = title[3:]
		x = x+1
		ReadSQL()
	
