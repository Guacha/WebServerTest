from flask import Flask, render_template, request, jsonify, url_for
from wiki import wikitools
from firebase import db
import os

app = Flask(__name__)

db.init_db_client()


@app.route('/')
def index():
	start_title, start_art, start_url = wikitools.random_article()
	end_title, end_art, end_url = wikitools.random_article()

	return render_template("main.html", inicio=start_title, inicio_url=start_url, final=end_title, final_url=end_url)


@app.route("/test")
def textingxd():
	tit, cont, url = wikitools.get_art("https://es.wikipedia.org/wiki/Ibai_Llanos", full_url=True)
	
	return render_template("game_template.html", article_data=wikitools.scrape_article(cont), title=tit)


@app.route("/startgame")
def newgame():
	return render_template("startgame.html")


@app.route("/<game_id>/wonnered/<attempt_code>", methods=['GET', 'POST'])
def wonnered(game_id, attempt_code):
	if request.method == 'POST':
		name = request.form['username']
		db.set_att_name(game_id, attempt_code, name)
	
	attempt = db.get_attempt(game_id, attempt_code)
	return render_template(
		"wonnered.html",
		clicks=attempt['clicks'],
		min=attempt['time']['m'],
		segs=attempt['time']['s'],
		ms=round(attempt['time']['ms']),
		name=attempt['name'],
		game=game_id)


@app.route('/<game_id>/ingame')
def ingame(game_id):
	game = db.get_game(game_id)
	_, html, url = wikitools.get_art(game['start_url'], full_url=True)
	link = url.split(".org")[1]
	article_content = wikitools.scrape_article(html)
	return render_template("game_template.html", article_data=article_content, title=game["start_name"], objetivo=game["end_name"], url=link)


@app.route('/<game_id>/attempts')
def game_attempts(game_id):
	game = db.get_game(game_id)
	atts = db.get_all_attempts(game_id)
	return render_template('wonners.html', game=game, attempts=atts, code=game_id)


@app.route("/click_on_article", methods=["POST"])
def click_on_article():
	link = request.form["link"]
	title, cont, url = wikitools.get_art(link)
	url = url.split(".org")[1]
	code = request.form["gamecode"][1:-7]
	clicks = request.form["current_clicks"]
	timer = {
		'ms': float(request.form["current_ms"]),
		's': int(request.form["current_s"]),
		'm': int(request.form["current_m"])
	}
	
	if db.get_game(code)["end_url"] == url:
		attempt_code = db.generate_attempt(code, clicks, timer)
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

	return jsonify({"code":game_code, "invite": url_for('invite', game_id=game_code, _external=True)})


@app.route("/random_article", methods=['POST'])
def random_article():
	name, _, link = wikitools.random_article()
	art = {
		"name": name,
		"link": link
	}
	return jsonify(art)


@app.route("/get_game", methods=['POST'])
def get_game():
	code = request.form['code']
	game = db.get_game(code)
	resp = {}
	if game:
		resp = {
			'exists': True,
			'game': game,
			'url': url_for('ingame', game_id=code)
		}
	else:
		resp = {'exists': False}
	return jsonify(resp)

@app.route("/invite/<game_id>")
def invite(game_id):
	return render_template("startgame.html", invite=game_id)


if __name__ == "__main__":
	debug_mode = os.environ.get('DEV', False)
	run_env = os.environ.get('ENV', 'DEPLOY')
	host = "0.0.0.0" if run_env == 'REPLIT' else "127.0.0.1"
	port = 8080 if run_env == 'REPLIT' else 5000
	app.run(debug=debug_mode, host=host, port=port)