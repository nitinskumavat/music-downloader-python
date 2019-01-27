from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import os
import re

#creating director to add downloaded song
if not os.path.exists('songs'):
    os.makedirs('songs')

def song_name():
    #input string and convert multiple spaces to single space
    song=re.sub(" +", " ", input("Enter song name\n"))
    if not song.strip():
        #strip because user might had entered only white spaces
        print("Input is empty\n")
    else:
        site="http://search.chiasenhac.vn/search.php?s="
        #replace " " with '+' as per website link
        song=song.replace(" ","+")
        site=site+song
        parse_site(site)
    
def parse_site(site):
    page = urlopen(site)
    soup = BeautifulSoup(page,'html.parser')
    #getting the first song form search result
    #to get all song results use findAll
    song = soup.find('a', {'class': 'musictitle'})
    if song.has_attr('href'):
        #getting link of song
        song_link=song['href']
    #converting above to download link 
    down_link=song_link[:-5]+'_download'+song_link[-5:]
    #moving to download page
    parse_download(down_link)

def parse_download(down_link):
    #opening download page
    download_page=urlopen(down_link)
    soup = BeautifulSoup(download_page,'html.parser')
    download_links=()
    #select links that contains download keyword, here we get 3 links thats why storing them in list
    download_links=soup.select("a[href*=downloads]")   
    download(download_links)

def download(download_links):
    #download form 1st link
    link=download_links[0]['href']
    #name to save
    name = download_links[0]['href'].replace("%20"," ").split('/')[-1]
    location='songs\\'+name
    print("downloading.....\n")
    #retrieving and saving
    urllib.request.urlretrieve(link,location)
    print("Download finished\n")
    
   
if __name__=='__main__':
    song_name()
