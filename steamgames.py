"""
steamgames.py
Copyright 2013, Nate Collings
http://github.com/naiyt/steamgames

A small API wrapper intended to retrieve all available store information
for either a specific appid, or all appids.

Thanks for this SteamDB.info blog post for the idea on the best way to do this:
http://steamdb.info/blog/5/

This should give you all of the same info that, say, SteamCalculator's script does
(https://github.com/spezifanta/SteamCalculator-Scripts), but it's much more efficient and
can return much more info.

"""

import urllib2
import urllib
import json
from time import sleep


class Base:
	def retry(self, url, time, retries):
		"""If a url is unavaible, retries it "retries" number of times, with "time" space between tries"""
		print "{} was unreachable, retrying {} number of times".format(url, retries)
		for num in range(retries):
			try:
				return urllib2.urlopen(url)
			except:
				sleep(time)
		print "Couldn't reach {} after {} retries. Moving to next.".format(url, retries)

	def open_url(self, url):
		try:
			return urllib2.urlopen(url)
		except urllib2.URLError as e:
			print 'URLError = {}'.format(str(e.reason))
		except urllib2.HTTPError as e:
			print 'HTTPError = {}'.format(str(e.code))
			return retry(self, url, 5, 5)
		except ValueError:
			print 'Not a proper url: {}'.format(url)

	def chunks(self, params, number):
		"""Breaks a list into a set of equally sized chunked lists, with remaining entries in last list"""
		for i in xrange(0, len(params), number):
			yield params[i:i+number]


class Games(Base):
	def __init__(self,num=None):
		"""
		Num is how many we can check against the Steam API per iteration. Defaults to 200,
		as I've had good success querying the API for 200 appids at a time.

		"""

		if num is None:
			self.num = 200
		else:
			self.num = num
		self.appids_names = self.get_ids_names()

	def _create_url(self, appids, cc):
		"""Given a list of appids, creates an API url to retrieve them"""
		appids = [str(x) for x in appids]
		list_of_ids = ','.join(appids)
		data = {'appids': list_of_ids, 'cc': cc, 'l': 'english', 'v': '1'}
		url_vals = urllib.urlencode(data)
		return "http://store.steampowered.com/api/appdetails/?{}".format(url_vals)

	def _get_urls(self, appids, cc):
		"""Returns urls for all of appids"""
		list_of_ids = list(self.chunks(appids,self.num))
		all_urls = []
		for x in list_of_ids:
			all_urls.append(self._create_url(x, cc))
		return all_urls

	def get_all(self, cc):
		urls = self._get_urls(self.appids_names.keys(), cc)
		for url in urls:
			print "Opening a new page of games..."
			curr_games = self._get_games_from(url)
			for game in curr_games:
				yield game

	def _get_games_from(self, url):
		page = json.loads(self.open_url(url).read())
		for appid in page:
			yield Game(page[appid], appid)


	def get_appids_info(self, cc, appids):
		"""Given a list of appids, returns their Game objects"""
		pass

	def get_ids_names(self):
		"""Returns all appids in the store as a dictionary mapping appid to game_name"""
		url = self.open_url("http://api.steampowered.com/ISteamApps/GetAppList/v2")
		url_info = json.loads(url.read())
		all_ids = {}
		for app in url_info['applist']['apps']:
			all_ids[app['appid']] = app['name']
		return all_ids
		

	def get_id(self, game_name):
		"""Given a game name, returns it's appid"""
		pass

	def get_name(self, appid):
		"""Given an appid, returns just it's game name"""
		pass


class Game(Base):
	def __init__(self, game_json, appid):
		if 'success' in game_json:
			try:
				print "{}: {}".format(appid, str(game_json['data']['price_overview']['initial']/100))
			except:
				print "Fail"
		else:
			print "Error! Can't read a game."
		