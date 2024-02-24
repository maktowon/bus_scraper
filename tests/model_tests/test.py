import unittest
from src.models.models import Location, Stop, InvalidLongitudeException, InvalidLatitudeException


class TestLocation(unittest.TestCase):
    def test_valid_location(self):
        # Test valid longitude and latitude
        longitude = 10.0
        latitude = 20.0
        location = Location(longitude, latitude)
        self.assertEqual(location.longitude, longitude)
        self.assertEqual(location.latitude, latitude)

    def test_invalid_longitude_too_low(self):
        # Test invalid longitude (too low)
        with self.assertRaises(InvalidLongitudeException):
            Location(-200.0, 30.0)  # Longitude out of range

    def test_invalid_longitude_too_high(self):
        # Test invalid longitude (too high)
        with self.assertRaises(InvalidLongitudeException):
            Location(200.0, 30.0)  # Longitude out of range

    def test_invalid_latitude_too_low(self):
        # Test invalid latitude (too low)
        with self.assertRaises(InvalidLatitudeException):
            Location(50.0, -100.0)  # Latitude out of range

    def test_invalid_latitude_too_high(self):
        # Test invalid latitude (too high)
        with self.assertRaises(InvalidLatitudeException):
            Location(50.0, 200.0)  # Latitude out of range


class TestStop(unittest.TestCase):
    def test_stop_equality(self):
        # Test equality of two stops
        location1 = Location(10.0, 20.0)
        location2 = Location(10.0, 20.0)
        stop1 = Stop("Stop1", location1, "Post1", "Street1", "Group1")
        stop2 = Stop("Stop1", location2, "Post1", "Street1", "Group1")
        self.assertEqual(stop1, stop2)

    def test_stop_hash(self):
        # Test hash value of a stop
        location = Location(10.0, 20.0)
        stop = Stop("Stop1", location, "Post1", "Street1", "Group1")
        self.assertEqual(hash(stop), hash(("Stop1", 10.0, 20.0, "Post1", "Street1", "Group1")))


if __name__ == '__main__':
    unittest.main()
