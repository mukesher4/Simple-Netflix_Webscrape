import requests
from bs4 import BeautifulSoup

user_input = str(input("Enter Show : "))

dork = f"site:netflix.com {user_input}"
query = f"https://www.google.com/search?q={dork}"

google_resp = requests.get(query)
google_soup = BeautifulSoup(google_resp.text, 'html.parser')

results=google_soup.find_all("a")

for r in results:
	if (r.get('href')[:30])=="/url?q=https://www.netflix.com":
		URL = r.get('href')[7:r.get('href').find('&')]
		break

resp = requests.get(URL)
soup = BeautifulSoup(resp.text, 'html.parser')

Show_Title = soup.find("h1", {"class":"title-title"}).text
seasons = soup.find_all("div",{"class":"season"})

e = {Show_Title: {}}

for s_index,s in enumerate(seasons,1):
	e[Show_Title][f"S{s_index}"]={}
	episodes = s.find("ol",{"class":"episodes-container"})

	for e_index,episode in enumerate(episodes,1):
		e[Show_Title][f"S{s_index}"][e_index]={}
		try:
			e[Show_Title][f"S{s_index}"][e_index]["Title"]=episode.find("h3","episode-title").text.split(".")[1][1:]
		except:
			e[Show_Title][f"S{s_index}"][e_index]["Title"]=episode.find("h3","episode-title").text	
		e[Show_Title][f"S{s_index}"][e_index]["Duration"]=episode.find("span",{"class":"episode-runtime"}).text

print(e)