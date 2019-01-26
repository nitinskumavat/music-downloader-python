from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import os

#creating director to add downloaded song
if not os.path.exists('songs'):
    os.makedirs('songs')

#link for website
site="http://search.chiasenhac.vn/search.php?s="
song=input("Enter song name")
song=song.replace(" ","+")
site=site+song
page = urlopen(site)
soup = BeautifulSoup(page,'html.parser')

song_result = soup.findAll('div', {'class': 'tenbh'}) #find all songs 
song = soup.find('a', {'class': 'musictitle'})#find all music 


if song.has_attr('href'):
    song_link=song['href'] #getting links of songs

down_link=song_link[:-5]+'_download'+song_link[-5:] #converting to download link

 
d_page=urlopen(down_link)
soup2 = BeautifulSoup(d_page,'html.parser')

download_links=()
download_links=soup2.select("a[href*=downloads]")#select links that contains download keyword
for links in download_links:
    print(links['href'])

name = download_links[0]['href'].replace("%20"," ").split('/')[-1]#getting name for downloaded song
print(name)
#download file form second link
link=download_links[0]['href']
location='songs\\'+name
urllib.request.urlretrieve(link,location)

