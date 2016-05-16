import time, datetime, sqlite3, os, subprocess

def addtodb(gennytime):	
	conn = sqlite3.connect('Canbus.db')
	c = conn.cursor()
	c.execute("INSERT INTO showerthoughts VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (gennytime[0], gennytime[1], gennytime[2], gennytime[3], gennytime[4], gennytime[5], gennytime[6], gennytime[7], gennytime[8]))
	conn.commit()
	conn.close()

gennytime = [502, (time.strftime("%I")), (time.strftime("%M")), 00,00,00,00,00,00]

addtodb(gennytime)
os.system("sudo python Canbussend.py")