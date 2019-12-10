import unittest
from finalproj import *
DBNAME = COMDB

class TestDatabase(unittest.TestCase):

    def test_mentions_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''SELECT Mentions FROM Mentions
                WHERE Country = "Jordan"'''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0][0], 3)

        sql = '''
            SELECT Mentions FROM Mentions
            WHERE Country="Jamaica"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0][0], 13)

        conn.close()


    def test_countries_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''SELECT Region FROM Countries
                WHERE EnglishName = "Algeria"'''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0][0], "Africa")

        sql = '''
            SELECT EnglishName FROM Countries
            WHERE Alpha2="AF"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 1)
        self.assertEqual(result_list[0][0], 'Afghanistan')

        conn.close()

    def test_stories_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''SELECT Contents FROM Stories
                WHERE Title = "World AIDS Day 2019 message from UNAIDS Executive Director Winnie Byanyima"'''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 1)

        sql = '''
            SELECT Title FROM Stories
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 102)

        conn.close()


class TestCrawl(unittest.TestCase):

    def test_unaids_scrape(self):
        try:
            test = scrape_unaids()
            self.assertEqual(len(test), 109)
            self.assertTrue(test, 'Niger')
        except:
            self.fail()


class TestPlotly(unittest.TestCase):
    def test_map(self):
        try:
            test = plot_mention_freq()
        except:
            self.fail()

    def test_scatter(self):
        try:
            test = plot_mention_pop()
        except:
            self.fail()

    def test_wordcloud(self):
        try:
            test = word_cloud()
        except:
            self.fail()

    def test_pie(self):
        try:
            test = pie_chart('Region')
        except:
            self.fail()

unittest.main()
