from urlcheck import urlcheck
import unittest
import youtube_dl


true_urls = ('https://youtu.be/KMU0tzLwhbE', 'http://youtu.be/KMU0tzLwhbE', 'youtu.be/KMU0tzLwhbE', 'https://www.youtube.com/watch?v=KMU0tzLwhbE')

false_urls = ('google.com', 'Wooo I hacked the bot', 'https://www.youtube.com/watch?v=KMUdffddsfs')

class TestUrlCheck(unittest.TestCase):

    def test_url_true(self):
        for val in true_urls:
            self.assertTrue(urlcheck(val))
    def test_url_false(self):
        for val in false_urls:
            self.assertFalse(urlcheck(val))
            

if __name__ == '__main__':
    unittest.main()


