from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import os
import re


#creating director to add downloaded song
if not os.path.exists('songs'):
    os.makedirs('songs')

def check_status(link):
    try:
        html=urlopen(link)
        return 1
    except:
        return 0

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
    if check_status(site)==1:
        page = urlopen(site)
        soup = BeautifulSoup(page,'html.parser')
        #getting the first song form search result
        #to get all song results use findAll
        song = soup.findAll('a', {'class': 'musictitle'})
        print("Enter the song number\n")
        for i in range(5):
            s = song[i]['href']  
            lang=s.split("/")[4]#getting language from link
            song_name=s.split("/")[6].split("~")[0]
            singer_name=s.split("/")[6].split("~")[1]
            print("%d) %s, %s, %s" %(i+1,lang,song_name,singer_name))
        n=input("\nWaiting for input: ")
        n=n.strip()
        if n is 'r':
            song_name()
        elif n is '1' or n is '2' or n is '3' or n is '4' or n is '5':
            if song[int(n)-1].has_attr('href'):
                #getting link of song
                song_link=song[int(n)-1]['href']
            down_link=song_link[:-5]+'_download'+song_link[-5:]
            #moving to download page
            parse_download(down_link)
            
        else:
            print("Invlaid input\n ")
    else:
        print("Http error or Srever not found\n")


def parse_download(down_link):
     #opening download page
    if check_status(down_link)==1:       
        download_page=urlopen(down_link)
        soup = BeautifulSoup(download_page,'html.parser')
        download_links=()
        #select links that contains download keyword, here we get 3 links thats why storing them in list
        download_links=soup.select("a[href*=downloads]")   
        download(download_links)
    else:
        print("Http error or Srever not found\n")
        

def download(download_links):
    #download form 1st link
    link=download_links[0]['href']
    #name to save
    name = download_links[0]['href'].replace("%20"," ").split('/')[-1]
    location='songs\\'+name
    print("downloading.....\n")
    #retrieving and saving
    urllib.request.urlretrieve(link,location)
    print("Download complete!\n")
    
   
if __name__=='__main__':
    song_name()
