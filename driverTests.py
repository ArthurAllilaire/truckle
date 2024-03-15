import unittest
from datetime import date
import os
from drivers import createDatabase, addData, getDrivers, getTable
class TestDatabase(unittest.TestCase):
    def setUp(self) -> None:
        self.DATABASE = 'test.sqlite'
        # Remove any previous database
        if (os.path.exists(self.DATABASE)):
            os.remove(self.DATABASE)
        createDatabase(self.DATABASE)
        addData(self.DATABASE, "driver", date.today(), 200, 7752715719, "Street 15")
        addData(self.DATABASE, "driver", date.today(), 200, 8890123412, "Street 16")
        return super().setUp()

    def testAddDrivers(self) -> None:
        self.assertEqual(
            [(7752715719, 200, date.today().isoformat(), 'Street 15'),
             (8890123412, 200, date.today().isoformat(), 'Street 16')],
            getTable(self.DATABASE, "delivery"))
        
    def testGetDrivers(self) -> None:
        self.assertEqual(
            [(7752715719, 200, 'Street 15'), (8890123412, 200, 'Street 16')],
            getDrivers(self.DATABASE, date.today(), 20)[1])

    def testFullyBookedDriver(self) -> None:
        addData(self.DATABASE, "farmer", date.today(), 50, 123456789, "Street 2", 7752715719)
        # print(getTable(self.DATABASE, "farmers"))
        # Should filter out the 7752715719 as only 150 kg left
        self.assertEqual([(8890123412, 200, 'Street 16')], getDrivers(self.DATABASE, date.today(), 160)[1])

    def tearDown(self) -> None:
        return super().tearDown()
if __name__ == '__main__':
    unittest.main()