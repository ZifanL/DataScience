from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import csv
import re

TIME_PATTERN1 = re.compile("([0-9]+)\s*h\s*([0-9]+)\s*min")
TIME_PATTERN2 = re.compile("([0-9]+)\s*h")
TIME_PATTERN3 = re.compile("([0-9]+)\s*min")

DATE_PATTERN = re.compile("([0-9]+)\s*([a-zA-Z]+)\s*([0-9]+)")

months = {'January':'1', 'February':'2', 'March':'3', 'April':'4', 'May':'5', 'June':'6', 'July':'7', 'August':'8', 'September':'9', 'October':'10', 'November':'11', 'December':'12'}

def toMin(duration):
	match1 = TIME_PATTERN1.search(duration)
	if match1 is not None:
		hour = match1.group(1)
		minute = match1.group(2)
		return str(int(hour)*60+int(minute))+' min'
	match2 = TIME_PATTERN2.search(duration)
	if match2 is not None:
		hour = match2.group(1)
		return str(int(hour)*60)+' min'
	match3 = TIME_PATTERN3.search(duration)
	if match3 is not None:
		minute = match3.group(1)
		return minute+' min'
	return 'null'

def toDate(input):
	match = DATE_PATTERN.search(input)
	if match is None:
		return 'null'
	day = match.group(1)
	month = match.group(2)
	year = match.group(3)
	return months[month]+'/'+day+'/'+year



if __name__ == '__main__':

	with open('imdb_data.csv', mode='w') as csv_file:
		fieldnames = ['name', 'genre', 'actor', 'director', 'duration', 'date_released', 'score']
		writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
		writer.writeheader()

		for i in range(120):
			print('page: '+str(i))
			imdb = 'https://www.imdb.com/search/title?genres=action&start='+str(1+i*50)+'&explore=title_type,genres&ref_=adv_nxt'
			html = urlopen(imdb).read().decode('utf-8')
			#print(html)
			soup = BeautifulSoup(html, features='lxml')
			all_h3 = soup.find_all("h3")

			print('-------------------------------------------------')
			for one_h3 in all_h3:
				if one_h3.get('class') is not None and one_h3.get('class')[0] == 'lister-item-header':
					links = one_h3.find_all('a')
					for link in links:
						info = {}
						target = 'https://www.imdb.com'+link.get('href')
						print('Go to target: '+target)
						sub_html = urlopen(target).read().decode('utf-8')
						#print(sub_html)
						sub_soup = BeautifulSoup(sub_html, features = 'lxml')

						times = sub_soup.find_all('time')
						if len(times) == 0:
							info['duration'] = 'null'
						else:
							time = times[0]
							info['duration'] = toMin(time.get_text().strip())

						dates = sub_soup.find_all('a',{'title':'See more release dates'})
						if len(dates) == 0:
							info['date_released'] = 'null'
						else:
							date = dates[0]
							info['date_released'] = toDate(date.get_text())


						details = sub_soup.find_all('script', {'type': "application/ld+json"})
						assert len(details) == 1
						for detail in details:
							js = json.loads(detail.get_text())
							
							if 'name' in js:
								info['name'] = js['name']
							else:
								info['name'] = 'null'

							if 'genre' in js:
								genre_str = ''
								for genre in js['genre']:
									genre_str += genre
									genre_str += '&'
								genre_str = genre_str.rstrip('&')
								info['genre'] = genre_str
							else:
								info['genre'] = 'null'

							if 'actor' in js:
								actor_str = ''
								if type(js['actor']) is list:
									for actor in js['actor']:
										actor_str += actor['name']
										actor_str += '&'
									actor_str = actor_str.rstrip('&')
								if type(js['actor']) is dict:
									actor_str = js['actor']['name']
								info['actor'] = actor_str
							else:
								info['actor'] = 'null'
			

							if 'director' in js:
								director_str = ''
								if type(js['director']) is list:
									for director in js['director']:
										director_str += director['name']
										director_str += '&'
									director_str = director_str.rstrip('&')
								if type(js['director']) is dict:
									director_str = js['director']['name']
								info['director'] = director_str
							else:
								info['director'] = 'null'

							if 'aggregateRating' in js and 'ratingValue' in js['aggregateRating']:
								info['score'] = js['aggregateRating']['ratingValue']
							else:
								info['score'] = 'null'

							if '@type' in js and js['@type'] == 'Movie':
								writer.writerow(info)




