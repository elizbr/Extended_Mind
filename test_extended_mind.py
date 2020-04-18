import extended_mind


## Test 1 
extended_mind.format_album_query('High Violet') == "https://pitchfork.com/search/?query=%20high%20violet"
extended_mind.format_album_query('Sunbather') == "https://pitchfork.com/search/?query=sunbather"



## Test other 
'''
radiohead = spotipy_call('Radiohead')
add_artist_to_sql(radiohead.jjson())
'''
