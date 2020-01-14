# Dawei Li, 001022014

import unittest
import packages.data as data
from packages.hash_table import MyHashTable
from packages.read_xlsx import XlsxReader
from packages.truck import Truck


class TestHashTable(unittest.TestCase):

    def test_add(self):
        self.ht = MyHashTable(size=10)
        self.ht.add(1, "foo")
        self.ht.add(11, "foo2")
        self.ht.add(2, "bar")
        self.assertTrue(len(self.ht.buckets), 10)
        self.assertTrue(self.ht.occupied, 2)
        self.assertEqual(len(self.ht.buckets[1]), 2)
        self.assertEqual(len(self.ht.buckets[2]), 1)

    def test_get(self):
        self.ht = MyHashTable(size=10)
        self.ht.add(1, "foo")
        self.ht.add(11, "foo2")
        self.ht.add(2, "bar")
        self.assertEqual(self.ht.get(1), "foo")
        self.assertEqual(self.ht.get(11), "foo2")
        self.assertEqual(self.ht.get(2), "bar")

    def test_double_size(self):
        self.ht = MyHashTable(size=4)
        self.ht.add(1, "foo")
        self.assertEqual(len(self.ht.buckets), 4)
        self.ht.add(11, "foo2")
        self.assertEqual(len(self.ht.buckets), 8)
        self.ht.add(2, "bar")
        self.assertEqual(len(self.ht.buckets), 8)


class TestMain(unittest.TestCase):
    def test_read_package_data(self):
        data.init()
        self.assertEqual(len(data.package_data.buckets), 100)
        package1 = data.package_data.get(1)
        self.assertEqual(package1.get("address"), "195 W Oakland Ave")
        self.assertEqual(package1.get("weight"), 21)
        self.assertEqual(package1.get("deadline").hour, 10)
        self.assertEqual(package1.get("deadline").minute, 30)

    def test_read_delivery_data(self):
        data.init()
        distance1 = data.distance_data.get(("1060 Dalton Ave S", "4001 South 700 East"))
        self.assertEqual(distance1, 7.2)
        distance2 = data.distance_data.get(("6351 South 900 East", "3595 Main St"))
        self.assertEqual(distance2, 5.2)


class TestTruck(unittest.TestCase):
    def test_load_truck(self):
        truck = Truck()
        self.assertTrue(truck.is_empty())
        truck.load_truck(1, "package 1 details")
        self.assertEqual(truck.package_count, 1)
        self.assertFalse(truck.is_empty())


if __name__ == '__main__':
    unittest.main()
