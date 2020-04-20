import unittest

from utilities.lists import flatten_list, remove_outliers, split_into_chunks


class ListsTest(unittest.TestCase):

    def test_flatten_list(self) -> None:
        list = [["A", "B"], ["C"], "D", "E", "F"]
        flat_list = flatten_list(list_of_list=list)
        self.assertEquals(flat_list, ["A", "B", "C", "D", "E", "F"])

    def test_remove_outliers(self) -> None:
        values = [1, 1.1, 0.8, 0.9, 10, 1.15, 1.05, 1.06]
        without_outlier = remove_outliers(X=values, t=2.0)
        self.assertNotIn(10, without_outlier)

    def test_split_into_chunks(self) -> None:
        long_list = list(range(0, 100))
        batches = split_into_chunks(long_list, chunks_size=25)
        self.assertEqual(len(batches), 4)
        self.assertEqual(batches[0], list(range(0, 25)))
