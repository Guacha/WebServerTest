from flask import Flask, render_template, request, jsonify, url_for
from wiki import wikitools
from firebase import db

app = Flask(__name__)

db.init_db_client()

@app.route('/')
def index():
	start_title, start_art, start_url = wikitools.random_article()
	end_title, end_art, end_url = wikitools.random_article()

	return render_template("main.html", inicio=start_title, inicio_url=start_url, final=end_title, final_url=end_url)

@app.route('/test')
def test():
	return render_template("game_template.html")

@app.route("/startgame")
def newgame():
	return render_template("startgame.html")


@app.route("/<game_id>/wonnered/<attempt_code>")
def wonnered(game_id, attempt_code):
	
	pass


@app.route('/<game_id>/ingame')
def random_art(game_id):
	game = db.get_game(game_id)
	_, html, _ = wikitools.get_art(game['start_url'], full_url=True)
	article_content = wikitools.scrape_article(html)
	return render_template("game_template.html", article_data=article_content, title=game["start_name"], objetivo=game["end_name"])


@app.route("/click_on_article", methods=["POST"])
def click_on_article():
	link = request.form["link"]
	title, cont, url = wikitools.get_art(link)
	code = request.form["gamecode"][1:-7]
	clicks = request.form["current_clicks"]
	ms = request.form["current_ms"]
	s = request.form["current_s"]
	m = request.form["current_m"]
	
	if db.get_game(code)["end_url"] == url:
		attempt_code = db.generate_attempt(code, clicks, (m,s,ms))
		return {"wonnered": True, "url": f"{url_for('wonnered', attempt_code=attempt_code, game_id=code)}"}
		
	cont = wikitools.scrape_article(cont)
	return jsonify({"title": title, "cont": cont, "url": url, "wonnered": False})


@app.route("/gen_new_game", methods=['POST'])
def generate_game():
	start_name = request.form["start_name"]
	start_url = request.form["start_url"]
	end_name = request.form["end_name"]
	end_url = request.form["end_url"]

	game_code = db.gen_game(start_name, start_url, end_name, end_url)

	return jsonify({"code": game_code})


@app.route("/random_article", methods=['POST'])
def random_article():
	name, _, link = wikitools.random_article()
	art = {
		"name": name,
		"link": link
	}
	return jsonify(art)


if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port=8080)