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
			$("#gameCodeField").val(resp.invite)
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

function getGame(game_code) {
	$("#searchButton").prop("disabled", true);
	$("#searchCodeArea").prop("disabled", true);
	$.ajax({
		url: '/get_game',
		data: {'code': game_code},
		type: 'POST',
		success: function(response) {
			if (response.exists) {
				$("#searchCodeArea").removeClass("is-invalid");
				$("#inviteSrc").text(response.game.start_name)
				$("#inviteDest").text(response.game.end_name)
				$("#startInviteButton").removeClass("disabled")
				$("#startInviteButton").attr("href", response.url)
			} else {
				$("#searchButton").prop("disabled", false);
				$("#searchCodeArea").toggleClass("is-invalid");
				$("#searchCodeArea").prop("disabled", false);
			}
		}
	})
};

$("#searchButton").click(function(event) {
	getGame($("#searchCodeArea").val());
})

function disableNewGame() {

}
