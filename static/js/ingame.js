var clicks = 0;
var stopwatch;
var loading = false;


$(document).on("click", "a", function(event) {
	getLink($(this).attr("href"))
});

$(document).ready(function() {
	stopwatch = new Stopwatch(document.getElementById("time"), null);
	stopwatch.start();
});

function getLink(href) {
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
						stopwatch.stop()
						window.location.replace(resp.url)
					} else {
						loadArticle(resp.title, resp.cont)
						scrollTo(0,0)
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