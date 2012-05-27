/*$(function(){


	function onAjaxSuccess(result){
		$(".content").append("<h1>" + result.success + "</h1>");
		$(".content").append("<h3>" + result.msg + "</h3>");
		$(".content").show();
	}

	$(".content").hide();
	$("#header").click(function(){
		$(".content").html("<div align='center'><img src='loading.gif'></div>");
		$(".content").show();
	});

	$("#form").submit(function(){
		$.ajax({
			url: "cgi-bin/sa.py",
			type: "POST",
			contentType: "multipart/form-data",
			data: {asd: "dasdasdsad", ad: "asdsw22"},
			success: onAjaxSuccess
		});

		return false;
	});

});*/

