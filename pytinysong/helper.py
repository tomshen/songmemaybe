from pytinysong.request import TinySongRequest

def formattedSearch(query):
	if query == "":
		return "<p>You didn't enter a search query. Please go back to the original window and enter a search query.</p>"
	song_request = TinySongRequest(api_key='164b76e7347518c2e737ca2ebc2b7830')
	songs = song_request.search(query)
	html_list = "<ul>\n"
	for song in songs:
		html_list += "<li>\n" + song.song_name + "\n<ul>\n<li>Artist: " + song.artist_name + "</li>\n<li>Song ID: " + str(song.song_id) + "</li>\n</ul>\n</li>\n"
	html_list += "</ul>"
	return html_list
	
def searchToText(query):
	f = open('output.html', 'w')
	f.write('<html>\n<head>\n<title>TinySong Search Results</title>\n</head>\n<body>\n')
	f.write(formattedSearch(query))
	f.write('\n</body>\n</html>')