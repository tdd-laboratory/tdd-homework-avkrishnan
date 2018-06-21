import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    #Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for a date, we find it.
    def test_dates(self):
        self.assert_extract('I was born on 1965-12-25.', library.dates_iso8601, '1965-12-25')

    # Fourth unit test; prove that months more than 12 and days more than 31 are flagged 
    def test_wrong_dates(self):
        self.assert_extract('I was born on 1965-13-32.', library.dates_iso8601)

    # Fifth unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Sixth unit test; prove that dates such as dd mmm yyyy are handled
    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')

    # Seventh unit test; prove that dates such as dd mmm, yyyy are handled
    def test_dates_fmt2_with_comma(self):
        self.assert_extract('I was born on 25 Jan, 2017.', library.dates_fmt2, '25 Jan 2017')

    # Eighth unit test; prove that dates with timestamps are flagged 
    def test_dates_with_timestamp(self):
        self.assert_extract('I was born on 1965-11-22 05:43:54.2.', library.dates_iso8601)

    # Ninth unit test; prove that dates with timestamps with timezone at end are flagged 
    def test_dates_with_timestamp_with_tz(self):
        self.assert_extract('I was born on 1965-11-22 T05:43:54.2MDT.', library.dates_iso8601)

    # Tenth unit test; prove that dates with timestamps with T delimeter are flagged 
    def test_dates_with_timestamp_with_T(self):
        self.assert_extract('I was born on 1965-11-22 T05:43:54.2.', library.dates_iso8601)



if __name__ == '__main__':
    unittest.main()
