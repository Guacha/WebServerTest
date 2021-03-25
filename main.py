from flask import Flask, render_template, request, jsonify
from wiki import wikitools

app = Flask(__name__)


@app.route('/')
def index():
	start_title, start_art, start_url = wikitools.random_article_url()
	end_title, end_art, end_url = wikitools.random_article_url()

	return render_template("main.html", inicio=start_title, inicio_url=start_url, final=end_title, final_url=end_url)

@app.route('/test')
def test():
	return render_template("game_template.html")

@app.route("/startgame")
def newgame():
	start_title, start_url = wikitools.random_article_url()
	end_title, end_url = wikitools.random_article_url()

	return render_template("startgame.html", a="a")


@app.route('/ingame')
def random_art():
	title, html, link = wikitools.random_article_url()
	article_content = wikitools.scrape_article(html)
	return render_template("game_template.html", article_data=article_content, title=title)


@app.route("/click_on_article", methods=["POST"])
def click_on_article():
	link = request.form["link"]
	title, cont, url = wikitools.get_art(link)
	cont = wikitools.scrape_article(cont)
	return jsonify({"title": title, "cont": cont, "url": url})


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=8080)