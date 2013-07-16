import unittest
from steamgames import Games

class Tests(unittest.TestCase):

	def test_sanity_of_values(self):
		test_id = 220
		test_name = "Half-Life 2"
		test_success = True
		test_type = "game"
		test_header_image = "http://cdn3.steampowered.com/v/gfx/apps/220/header.jpg?t=1369255063"
		test_website = "http://www.half-life2.com"
		test_currency = "USD"
		test_platforms = {"windows": True, "mac": True}

		games = Games()
		hl2 = games.get_info_for([test_id], 'us').next()
		self.assertEqual(str(test_id),hl2.appid)
		self.assertEqual(test_name,hl2.name)
		self.assertEqual(test_success,hl2.success)
		self.assertEqual(test_type,hl2.type)
		self.assertEqual(test_header_image,hl2.header_image)
		self.assertEqual(test_website,hl2.website)
		self.assertEqual(test_currency,hl2.currency)
		self.assertEqual(test_platforms,hl2.platforms)



if __name__ == '__main__':
	unittest.main()