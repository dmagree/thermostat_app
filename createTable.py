import sqlite3

def createTable():

	with sqlite3.connect('thermostat.db') as conn:
		curs = conn.cursor()
		curs.execute("DROP TABLE IF EXISTS DHT_data")
		curs.execute("CREATE TABLE DHT_data(timestamp DATETIME, temp NUMERIC, hum NUMERIC, desired_temp NUMERIC)")


if __name__ == '__main__':
	createTable()