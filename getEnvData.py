#!/usr/bin/env python
import sqlite3
import requests
import time
import os
dbname = 'thermostat.db'

thermostat_address = os.environ["THERMOSTAT_ADDRESS"]

def getEnvData():
	data = requests.get( 'http://'+thermostat_address+'/status')
	#print data.text
	datalist = [float(i) for i in data.text.split('|')]
	return datalist

def storeData(temp, hum, desired_temp, is_heating):
	conn = sqlite3.connect(dbname)
	curs = conn.cursor()
	#print "saving:", temp, hum, desired_temp, is_heating
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?), (?), (?))", (temp, hum, desired_temp, is_heating))
	conn.commit()
	conn.close()

def main():
	datalist = getEnvData()
	storeData(datalist[0], datalist[2], datalist[4], datalist[3])

if __name__ == '__main__':
	main()
