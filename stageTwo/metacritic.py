from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import csv
#import sys
#import json

if __name__ == '__main__':
    fieldnames = ['name', 'genre', 'actor', 'director', 'duration', 'date_released', 'score']
    with open('metacritic_data.csv', mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        root = ["https://www.metacritic.com/browse/movies/genre/date/action?view=condensed&page=", "https://www.metacritic.com/browse/movies/genre/date/documentary?view=condensed&page="]
        for rooti in range(2):
            if rooti == 0:
                limitindex = 64
            else:
                limitindex = 36
            for i in range(limitindex):
                print(rooti, i)
                site= root[rooti] + str(i)
                hdr = {'User-Agent': 'Mozilla/5.0'}
                req = Request(site,headers=hdr)
                html = urlopen(req).read().decode('utf-8')
                soup = BeautifulSoup(html, features='lxml')
                all_h3 = soup.find_all("div")
                for one_h3 in all_h3:
                    #try:
                    if one_h3.get('class') is not None and one_h3.findChildren("h3" , recursive=False) == [] and one_h3.get('class')[0] == 'basic_stat' and one_h3.get('class')[1] == 'product_title':
                        links = one_h3.find_all('a')
                        for link in links:
                            info = {}
                            target = 'https://www.metacritic.com'+link.get('href')
                            #print('Go to target: '+target)
                            req = Request(target,headers=hdr)      
                            sub_html = urlopen(req).read().decode('utf-8')
                            
                            #print(sub_html)
                            sub_soup = BeautifulSoup(sub_html, features = 'lxml')
                            director = sub_soup.find('div', {'class': "director"})
                            if director is not None:
                                director = director.get_text().split('\n')[2].replace(" and ", "&")
                            else:
                                director = 'null'
                            #print(director)
                            
                            genres = sub_soup.find('div', {'class': "genres"})
                            if genres is not None:
                                genres = ''.join(genres.get_text().split('\n')[3].split(' ')).replace(",", "&")
                            else:
                                genres = 'null'
                            #print(genres)
                            
                            runtime = sub_soup.find('div', {'class': "runtime"})
                            if runtime is not None:
                                runtime = runtime.get_text().split('\n')[2]
                            else:
                                runtime = 'null'
                            #print(runtime)
                            
                            actors = sub_soup.find('div', {'class': "summary_cast details_section"})
                            if actors is not None:
                                actors = ''.join(re.split("  +", actors.get_text().split('\n')[3])).replace(",", "&")
                            else:
                                actors = 'null'
                            #print(actors)
                            
                            date = sub_soup.find('span', {'class': "release_date"})
                            if date is not None:
                                date_letter = date.get_text().split('\n')[2].replace(", ", " ")
                                date_sp = date_letter.split()
                                if date_sp[0] in months:
                                    date_sp[0] = str(months.index(date_sp[0])+1)
                                    date = '/'.join(date_sp)
                                else:
                                    date = 'null'
                            else:
                                date = 'null'
                            #print(date)
                            
#                            userscore = sub_soup.find('div', {'class': re.compile("metascore_w user larger movie *")})
#                            if userscore is not None:
#                                userscore = userscore.get_text().split('\n')[0]
#                            else:
#                                userscore = 'null'
#                            #print(userscore)
                            
                            metascore = sub_soup.find('div', {'class': re.compile("metascore_w larger movie *")})
                            if metascore is not None:
                                metascore = metascore.get_text().split('\n')[0]
                            else:
                                metascore = 'null'
                            #print(metascore)
                            
                            name = sub_soup.find('div', {'class': "product_page_title oswald"})
                            name = name.get_text().split('\n')[1]
                            print(name)
                            #['name', 'genre', 'actor', 'director', 'duration', 'datePublished', 'score']
                            if runtime.lower() == 'tbd' or runtime.lower() == 'tba':
                                runtime = 'null'
                            if name.lower() == 'tbd' or name.lower() == 'tba':
                                name = 'null'
                            if genres.lower() == 'tbd' or genres.lower() == 'tba':
                                genres = 'null'
                            if actors.lower() == 'tbd' or actors.lower() == 'tba':
                                actors = 'null'
                            if date.lower() == 'tbd' or date.lower() == 'tba':
                                date = 'null'
                            if metascore.lower() == 'tbd' or metascore.lower() == 'tba':
                                userscore = 'null'
                            if director.lower() == 'tbd' or director.lower() == 'tba':
                                director = 'null'
        #                    if name == 'Blazing Samurai':
                            info['duration'] = runtime
                            info['name'] = name
                            info['genre'] = genres
                            info['actor'] = actors
                            info['date_released'] = date
                            info['score'] = metascore
                            info['director'] = director
                            writer.writerow(info)    
                    
            #except KeyboardInterrupt:
            #    sys.exit()
            #except:
            #    print("An exception occurred while processing ", one_h3)
        				



