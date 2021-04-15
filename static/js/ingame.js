var clicks = 0;
var stopwatch;
var loading = false;
var articleHistory = [];

$(document).on("click", "a", function(event) {
	var tag = $(this)
	var text = tag.text().trim();
	var href = tag.attr("href");

	

	getLink(href);
	$("#rewindButton").prop("disabled", false);
	$("#restartButton").prop("disabled", false);
	$("#historyButton").prop("disabled", false);
});

$(document).ready(function() {
	stopwatch = new Stopwatch(document.getElementById("time"), null);
	stopwatch.start();
});

$("#rewindButton").on("click", function(e) {
	getLink(articleHistory.pop().href, false);
	if (articleHistory.length >= 1) {
		updateHistory();
	} else {
		$("#rewindButton").prop("disabled", true);
		$("#historyButton").prop("disabled", true);
	};
	
});

$("#restartButton").on("click", function(e) {
	con = confirm("¿Seguro deseas reiniciar esta partida?");
	if (con) {
		location.reload();
	};
});

function getLink(href, sendToHistory = true) {
	if (!loading) {
		if (href.indexOf("/wiki/") != -1) {
			event.preventDefault()
			$("#clicks").text("# Clicks: " + (++clicks))
			loadingAnimation();
			$.ajax({
				url: '/click_on_article',
				data: {
					"link": href,
					"gamecode": window.location.pathname, 
					"current_clicks": clicks,
					"current_ms": stopwatch.ms,
					"current_s": stopwatch.s,
					"current_m": stopwatch.m
					},
				type: 'POST',
				success: function(resp) {
					if (resp.wonnered) {
						articleHistory.push(href)
						stopwatch.stop()
						window.location.replace(resp.url)
					} else {
						loadArticle(resp.title, resp.cont);
						scrollTo(0,0);
						if (sendToHistory) {
							toHistory(resp.title, resp.url);
							updateHistory();
						}
					}
				},
				error: function(err) {
					console.log(err);
				}
			});
		} else if(href.startsWith("#")) {
			// Do nothing
		}	else {
			event.preventDefault()
			alert("Este link te sacará de Wikipedia, y es inválido dentro del juego");
		}
	}
}

function loadingAnimation() {
	loading = true;
	var cont_tag = $("#art-cont")
	var tit_tag = $("#art-title")
	tit_tag.empty()
	tit_tag.append("Cargando...")
	cont_tag.empty()
	cont_tag.append("<div class='col align-self-center text-center'><div class='spinner-border' role='status'><span class='sr-only'></span></div></div>")
}

function loadArticle(title, content) {
	var cont_tag = $("#art-cont")
	var tit_tag = $("#art-title")
	tit_tag.empty()
	tit_tag.append(title)
	cont_tag.empty()
	cont_tag.append(content)
	$("title").text("WikiGame - " + title)
	loading = false;
}

function toHistory(title, href) {
	historyObject = {
		'title': current_title,
		'href': current_url
	};
	current_title = title;
	current_url = href;

	articleHistory.push(historyObject);
}

function updateHistory() {
	tag = $("#historyList");
	tag.empty();

	articleHistory.forEach(link => tag.append(`<li><a class='dropdown-item text-muted' href='${link.href}'>${link.title}</a></li>`))	
}