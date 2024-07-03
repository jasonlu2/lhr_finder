import unittest
from term_project import convert_time_to_int, binary_search, get_link

class TestMarathonResults(unittest.TestCase):
    def test_convert_time_to_int(self):
        # Test convert_time_to_int function
        self.assertEqual(convert_time_to_int("21:30.0"), 21300)
        self.assertEqual(convert_time_to_int("1:34:50.5"), 134505)

    def test_binary_search(self):
        # Test binary_search function
        mock_data = [21200, 21300, 21400]

        self.assertEqual(binary_search(mock_data, "21:30.0"), 2)
        self.assertEqual(binary_search(mock_data, "21:00.0"), 1)

    def test_get_link(self):
        # Test get_link function
        test_link_1 = "https://mychiptime.com/searchevent.php?id=10557"
        test_link_2 = "https://mychiptime.com/searchevent.php?id=10555"

        self.assertEqual(get_link("5k", "undergrad"), (test_link_1, ".d01:nth-child(8)"))
        self.assertEqual(get_link("10", "none"), -1)
        self.assertEqual(get_link("10k", "faculty/staff"), test_link_2)

# Run the tests
if __name__ == '__main__':
    unittest.main()
