$(document).ready(function()
{
	$('#letteropen').jsMovie(
	{
		sequence: "#.png",
		folder	: "images/animation/",
		from	: 1,
		to		: 9,
		width	: 1700,
		height	: 1400,
		showPreLoader : true,
		playOnLoad : false,
		loader : {path:"images/animation/loader.png", height:40, width:40, rows:4, columns:4},
		fps : 40
	});
	
	$('#letteropen').jsMovie("play")
});