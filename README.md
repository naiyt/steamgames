steamgames
==========

This is a script that will either provide a Games object for every appid currently in the Steam store, or will create a Games object for a specific list of appids that you pass in.

Pre-reqs
========

* Python 2.7
* A computer
* You don't even need a Steam API key!

Usage
=====

Usage is simple. You create a Games object, which in turn can return you either all of the appids in the form of Game objects, or a list of appids as Game objects. These are returned as generators that you can iterate through as needed. appid's are fetched from the API in chunks of 200 at a time. Since they are retrieved through a generator, this means that every 200 appids you'll have to wait a few seconds while the next chunk is retrieved from Steam.

Basics:
------

    from steamgames import Games
    games = Games()
    all_games = games.get_all('us') # all_games is a generator that will yield all appids from Steam
    for game in all_games:
        do_something_with_game(game)

Available data members of the Game object:
-----------------------------------------

* appid
* categories - The categories the appid is in (if any)
* currency - The currency returned (e.g., "USD")
* description - The appid's description
* discount_percent - The percentage the product has been discounted
* discounted_price - The current discounted price
* price - The game's normal, full price
* header_image - The URL to the appid's header image
* name - The appid's name
* packages - Info on any packages the appid is in
* platforms - Available platforms
* success - whether this appid was succesfully retrieved
* supported_langues
* type - e.g., "game", "trailer", "demo"
* website 

Examples:
========

First, setup your Games object:
    
    from steamgames import Games
    games = Games()

Find all games with a price less than $5.00:

    all_games = games.get_all('us')
    less_than_5 = []
    for game in all_games
        if game.price: # Some appids have no price (things like trailers and demos are included)
            if game.price < 5.00:
                less_than_5.append(game)

Find the price of all games on Steam:

    all_games = games.get_all('us')
    total = 0.0
    for game in all_games:
        if game.price:
            total += game.price

Find ONLY games (no demos, trailers, etc):

    all_games = games.get_all('us')
    for game in all_games:
        if game.type == 'game':
            do_things_with_game(game)


Find games in packages:
    
    all_games = games.get_all('us')
    for game in all_games:
        if game.packages:
            print game.packages

Retrieve info on a list of appids

     appids = [1,2,3,4]
     some_games = games.get_info_for(appids, 'us')
     for game in some_games:
         do_things_with_games(game)

TODO:
====

* Setup unit tests
* Make sure everything we would want from the Games object is included. (The JSON returned has some more properties, that you may or may not want.)
* Initial setup is kind of slow for some reason (I think the chunking is slow or something)
* Document the different country codes
