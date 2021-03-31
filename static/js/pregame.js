$(document).ready(function() {
	shuffleArticle($("#start"), $("#sURL"));
	shuffleArticle($("#end"), $("#eURL"));
});

$("#swapButton").on("click", function() {
	var curr_aux = $("#start").val();
	var curr_URL_aux = $("#sURL").attr("href");
	$("#start").val($("#end").val());
	$("#sURL").attr("href", $("#eURL").attr("href"));
	$("#end").val(curr_aux);
	$("#eURL").attr("href", curr_URL_aux);
});

$("#lockInButton").click(function() {
	$("#lockInButton").prop("disabled", true);
	$("#swapButton").prop("disabled", true);
	$(".shuffleButton").prop("disabled", true);
	$.ajax({
		url: "/gen_new_game",
		data: {
			"start_name": $("#start").val(),
			"start_url": $("#sURL").attr("href"),
			"end_name": $("#end").val(),
			"end_url": $("#eURL").attr("href")
		},
		type: 'POST',
		success: function(resp) {
			game_code = resp.code
			$("#gameCodeField").val(game_code)
			$("#startButton").attr("href", "/" +  game_code + "/ingame")
			$("#startButton").prop("disabled", false)
		}
	})
});

function shuffleArticle(field, anchor){
	field.val('')
	anchor.attr("href", '')
	$("#lockInButton").prop("disabled", true)
	var link = undefined, name = undefined;
	$.ajax({
		url: '/random_article',
		data: {},
		type: 'POST',
		success: function(resp) {
			link = resp.link;
			name = resp.name;
			field.val(name)
			anchor.attr("href", link)
			$("#lockInButton").prop("disabled", false)
		},
		error: function(err) {
			console.log(err)
		}
	})
	
};

