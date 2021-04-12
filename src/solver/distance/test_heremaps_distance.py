from unittest import TestCase
import re
import requests_mock
from src.solver.distance.heremaps_distance import HereMapsDistanceFunction
from src.solver.model.location import Location


class TestHereMapsDistanceFunction(TestCase):

    def test_generate_region_throws_if_empty(self):
        self.assertRaises(ValueError, HereMapsDistanceFunction.generate_region, [])

    def test_generate_region(self):
        locations = [Location(1, 2), Location(1, 3), Location(2, 2)]
        region = HereMapsDistanceFunction.generate_region(locations)
        av_lat = (1 + 1 + 2) / 3
        av_lon = (2 + 3 + 2) / 3
        expected = {
            "type": "circle",
            "center": {"lat": av_lat, "lon": av_lon},
            "radius": 50000
        }
        self.assertEqual(region, expected)

    def test_here_response(self):
        with requests_mock.Mocker() as mocker:
            matcher = re.compile("/matrix")
            mock_body = {
                "matrixId": "{matrixId}",
                "matrix": {
                    "numOrigins": 10,
                    "numDestinations": 1000,
                    "travelTimes": [10, 20, 0, 1, 2, 3, 4, 5, 6],
                    "errorCodes": [0, 0, 0, 0, 0, 0, 0, 0, 0]
                },
                "regionDefinition": {
                    "type": "circle",
                    "center": {"lat": 0.0, "lng": 0.0},
                    "radius": 10000
                }
            }
            mocker.post(
                matcher,
                status_code=200,
                json=mock_body
            )
            locations = [Location(1, 2), Location(1, 3), Location(2, 2)]
            distances = HereMapsDistanceFunction.compute_distances(locations)
            expected = [[10, 20, 0], [1, 2, 3], [4, 5, 6]]
            self.assertEqual(distances, expected)

    def test_here_response_raises(self):
        with requests_mock.Mocker() as mocker:
            locations = [Location(1, 2), Location(1, 3), Location(2, 2)]
            matcher = re.compile("/matrix")
            mocker.post(
                matcher,
                status_code=400,
                json={}
            )
            self.assertRaises(ValueError, HereMapsDistanceFunction.compute_distances, locations)
