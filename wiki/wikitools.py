from bs4 import BeautifulSoup
import requests

def random_article_url():
	"""
	Obtener un artículo de wikipedia de forma aleatoria y retornar la URL
	"""
	req = requests.get('https://es.wikipedia.org/wiki/Special:Random')
	soup = BeautifulSoup(req.text, "html.parser")
	title = soup.find("h1", id="firstHeading").string
	content = soup.find("div", id="bodyContent")
	return title, content, req.url

def scrape_article(art_cont):

	for item in art_cont.find_all("sup", class_="reference"):
		item.decompose()
	
	for item in art_cont.find_all("span", class_="mw-editsection"):
		item.decompose()

	try:
		art_cont.find("div", class_="listaref").decompose()
		art_cont.find("span", id="Referencias").parent.decompose()
	except AttributeError:
		pass

	try: 
		art_cont.find("span", id="Enlaces_externos").parent.decompose()
	except AttributeError:
		pass
	try:
		art_cont.find("span", id="Véase_también").parent.decompose()
	except AttributeError:
		pass

	for link in art_cont.find_all("a", class_="extiw"):
		if link.parent is not None:
			link.parent.string = link.string
	
	try:
		art_cont.find("div", class_="mw-authority-control").decompose()
	except AttributeError:
		pass

	art_cont.find("div", class_="catlinks").decompose()

	for link in art_cont.find_all("a", class_="external"):
		res = ""
		for s in link.stripped_strings:
			res += s + " " 
		link.insert_before(res)
		link.decompose()
		
	for photo_container in art_cont.find_all("a", class_="image")	:
		photo_container.parent.contents = photo_container.contents
	return art_cont.prettify()

def get_art(art_url):

	link = f"https://es.wikipedia.org{art_url}"
	req = requests.get(link)
	soup = BeautifulSoup(req.text, "html.parser")
	title = soup.find("h1", id="firstHeading").string
	content = soup.find("div", id="bodyContent")
	return title, content, req.url