import mock
import unittest


from knockblock.collections.base import Collection


class TestCollection(unittest.TestCase):

    def setUp(self):
        self.mock_block = mock.Mock()

    def test_schema(self):
        c = Collection(self.mock_block, "crew",
                       ["name", "rank", "salary"],
                       keys=["name", "rank"])
        self.assertEqual(c.key_columns, ("name", "rank"))
        self.assertEqual(c.columns, ("name", "rank", "salary"))

    def test_insert_a_tuple(self):
        c = Collection(self.mock_block, "crew", ["name", "rank"])
        c.insert(("Jean-Luc Picard", "Captain"))
        self.assertEqual(c.values(), [("Jean-Luc Picard", "Captain")])

    def test_get_a_tuple(self):
        c = Collection(self.mock_block, "crew",
                       ["name", "rank", "salary"],
                       keys=["name", "rank"])
        c.insert(("Jean-Luc Picard", "Captain", 400))
        c.insert(("Jeordi LaForge", "Engineer", 50))
        the_captain = c[("Jean-Luc Picard", "Captain")]
        self.assertEqual(the_captain.name, "Jean-Luc Picard")
        self.assertEqual(the_captain.rank, "Captain")
        self.assertEqual(the_captain.salary, 400)

    def test_projection(self):
        c = Collection(self.mock_block, "crew",
                       ["name", "rank", "salary"],
                       keys=["name", "rank"])
        c.insert(("Jean-Luc Picard", "Captain", 400))
        c.insert(("Jeordi LaForge", "Engineer", 50))
        tups = c._project(lambda t: [t.name, t.salary])
        self.assertEqual(len(tups), 2)
        self.assertEqual(len(tups[0]), 2)
        names = map(lambda t: t[0], tups)
        self.assertTrue("Jean-Luc Picard" in names)
        self.assertTrue("Jeordi LaForge" in names)

    def test_get_keys(self):
        c = Collection(self.mock_block, "crew",
                       ["name", "rank", "salary"],
                       keys=["name", "rank"])
        c.insert(("Jean-Luc Picard", "Captain", 400))
        c.insert(("Jeordi LaForge", "Engineer", 50))
        keys = c.keys()
        self.assertTrue(len(keys), 2)
        self.assertTrue(len(keys[0]), 2)
        names = map(lambda k: k[0], keys)
        ranks = map(lambda k: k[1], keys)
        self.assertTrue("Jean-Luc Picard" in names)
        self.assertTrue("Jeordi LaForge" in names)
        self.assertTrue("Captain" in ranks)
        self.assertTrue("Engineer" in ranks)
