import sqlite3
import requests
import time
dbname = 'thermostat.db'

thermostat_address = os.environ["THERMOSTAT_ADDRESS"]

def getEnvData():
	data = requests.get( 'http://'+thermostat_address+'/status')
	print data.text
	datalist = [float(i) for i in data.text.split('|')]
	return datalist

def storeData(temp, hum, desired_temp):
	conn = sqlite3.connect(dbname)
	curs = conn.cursor()
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum, desired_temp))
	conn.commit()
	conn.close()

def main():
	while(1):
		datalist = getEnvData()
		print datalist
		storeData(datalist[0], datalist[2], datalist[3])
		time.sleep(10)

if __name__ == '__main__':
	main()
