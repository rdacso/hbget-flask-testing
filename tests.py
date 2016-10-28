import unittest

from party import app
from model import db, example_data, connect_to_db
from flask import session



class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = "key"



    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        #setting variable result to a get result that displays the homepage
        result = self.client.get('/')
        #check to see if party details is not displayed
        self.assertNotIn("Party Details", result.data)
        #check to see if 'please rsvp' is displayed
        self.assertIn('Please RSVP', result.data)




    def test_rsvp(self):
        #post data to allow test to login to party details page
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        #check to see that 'please rsvp' is not displayed
        self.assertNotIn("Please RSVP", result.data)
        #check to see that 'party details' is displayed
        self.assertIn("Party Details", result.data)


class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["RSVP"] = True

    def tearDown(self):
        """Do at end of every test."""  

        db.session.close()
        db.drop_all()

    def test_games(self):
        #FIXME: test that the games page displays the game from example_data()
        result = self.client.get("/games")
        self.assertIn("twister", result.data)


if __name__ == "__main__":
    unittest.main()
