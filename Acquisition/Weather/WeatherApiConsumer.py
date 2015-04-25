import urllib2
import json
from datetime import date, timedelta

class WeatherApiConsumer:
	def __init__(self, date, countyName):
		self._date = date
		self._countyName = countyName
		
	def getPrecipitationInInches(self):
		url = 'http://api.wunderground.com/api/cc7750cde6c9a984/history_'+ str(self._date) +'/q/CA/'+ str(self._countyName) +'.json'
		response = urllib2.urlopen(url)
		jsonString = response.read()
		parsedJson = json.loads(jsonString)
		dailySummary = parsedJson['history']['dailysummary'][0]
		rain = dailySummary['precipi']
		response.close()
		return rain

def main():
	fileName = 'weatherData.txt'
	yesterday = date.today() - timedelta(days=1)
	dateString = yesterday.strftime('%Y%m%d')
	consumer = WeatherApiConsumer(dateString, 'Anaheim')
	
	appender = open(fileName, 'a')
	reader = open('CountyNames.txt', 'r')

	if reader.mode == 'r' and appender.mode == 'a':
		competeListing = reader.readlines()
		for line in competeListing:
			stringList = line.split(',')
			key = stringList[0]
			valueList = stringList[1].split('\n')
			value = valueList[0]
			consumer._countyName = value.lstrip(' ').replace(' ', '_')
			data = consumer.getPrecipitationInInches()
			formattedLine = dateString + ", " + value + ", "  + data + "\n"
			print formattedLine 
			appender.write(formattedLine)

	appender.close()
	reader.close()

if __name__ == "__main__": main()