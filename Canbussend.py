import os, subprocess, sqlite3




def ReadSQL():
	conn = sqlite3.connect('Canbus.db')
	c = conn.cursor()
	cursor = c.execute("SELECT ident, a, b, c, d, e, f, g, h FROM showerthoughts")
	for row in cursor:
		ident = str(row[0]).zfill(3)
		a = str(row[1]).zfill(2)
		b = str(row[2]).zfill(2)
		c = str(row[3]).zfill(2)
		d = str(row[4]).zfill(2)
		e = str(row[5]).zfill(2)
		f = str(row[6]).zfill(2)
		g = str(row[7]).zfill(2)
		h = str(row[8]).zfill(2)

		command = "cansend can0 %s#%s.%s.%s.%s.%s.%s.%s.%s" %(ident, a, b, c, d, e, f, g, h)
		print command
		os.system(command)
	conn.close()

#print 'sending'
ReadSQL()