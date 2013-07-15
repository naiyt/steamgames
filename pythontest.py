from steamgames import Games
games = Games()
all = games.get_all('us')
total_price = 0.00
"""for game in all:
	name = game.name.encode('ascii', 'ignore')
	if game.type == 'game':
		print "{}: {}: {}".format(game.appid, name, game.price)
		total_price += game.price
print "All games in Steam would cost you {}!".format(total_price)"""

some_games = games.get_appids_info([80, 620, 644], 'US')
for game in some_games:
	name = game.name.encode('ascii', 'ignore')
	if game.type == 'game':
		print "{}: {}: {}".format(game.appid, name, game.price)
