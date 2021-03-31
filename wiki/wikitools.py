from bs4 import BeautifulSoup
import requests

def random_article():
	"""
	Obtener un artículo de wikipedia de forma aleatoria y retornar la URL
	"""
	req = requests.get('https://es.wikipedia.org/wiki/Special:Random')
	soup = BeautifulSoup(req.text, "html.parser")
	title = soup.find("h1", id="firstHeading").string
	content = soup.find("div", id="bodyContent")
	return title, content, req.url

def scrape_article(art_cont):
	
	for item in art_cont.find_all("span", class_="mw-editsection"):
		item.decompose()
	
	try:
		art_cont.find("div", class_="mw-authority-control").decompose()
	except AttributeError:
		pass
		
	for photo_container in art_cont.find_all("a", class_="image")	:
		photo_container.parent.contents = photo_container.contents
	return art_cont.prettify()

def get_art(art_url, full_url=False):

	link = f"https://es.wikipedia.org{art_url}" if not full_url else art_url
	req = requests.get(link)
	soup = BeautifulSoup(req.text, "html.parser")
	title = soup.find("h1", id="firstHeading").string
	content = soup.find("div", id="bodyContent")
	return title, content, req.url