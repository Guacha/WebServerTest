var clicks = 0;

$(document).on("click", "a", function(event) {
	event.preventDefault()
	$.ajax({
		url: '/click_on_article',
		data: {"link": $(this).attr("href")},
		type: 'POST',
		success: function(resp) {
			var cont_tag = $("#art-cont")
			var tit_tag = $("#art-title")
			tit_tag.empty()
			tit_tag.append(resp.title)
			cont_tag.empty()
			cont_tag.append(resp.cont)
			$("#clicks").text("# Clicks: " + (++clicks))
		},
		error: function(err) {
			console.log(err);
		}
	});
});