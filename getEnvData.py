#!/usr/bin/env python
import sqlite3
import requests
import datetime, time
import os

print datetime.datetime.now()
dbname = os.environ.get('THERMOSTAT_DB','thermostat.db')
#print dbname

thermostat_address = os.environ["THERMOSTAT_ADDRESS"]

def getEnvData():
	data = requests.get( 'http://'+thermostat_address+'/status', timeout=1.0)
	print data.text
	datalist = [float(i) for i in data.text.split('|')]
	return datalist

def storeData(temp, hum, desired_temp, is_heating):
	conn = sqlite3.connect(dbname)
	curs = conn.cursor()
	print "saving:" 
        print "  temp:      ", temp
        print "  hum:       ", hum
        print "  des temp:  ", desired_temp 
        print "  is_heating:", is_heating
        curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?), (?), (?))", 
		(temp, hum, desired_temp, is_heating))
	conn.commit()
	conn.close()

def main():
	try:
		datalist = getEnvData()
	except requests.exceptions.Timeout:
		print "request timed out"
		return
	except requests.exceptions.RequestException:
		print "Other exception"
		return
	storeData(datalist[0], datalist[2], datalist[4], datalist[3])

if __name__ == '__main__':
	main()
