import unittest

from railway import Railway


class RailwaySampleDataTest(unittest.TestCase):
    def setUp(self):
        routes = "AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7"
        self.rail = Railway(routes)

    def test_distances(self):
        self.assertEqual(self.rail.get_route_distance('A', 'B', 'C'), 9)
        self.assertEqual(self.rail.get_route_distance('A', 'D'), 5)
        self.assertEqual(self.rail.get_route_distance('A', 'D', 'C'), 13)
        self.assertEqual(self.rail.get_route_distance('A', 'E', 'B', 'C', 'D'), 22)
        self.assertEqual(self.rail.get_route_distance('A', 'E', 'D'), None)

    def test_find_routes_by_stops(self):
        self.assertEqual(len(self.rail.find_routes_by_stops('C', 'C', 3)), 2)
        self.assertEqual(len(self.rail.find_routes_by_stops('A', 'C', 4, Railway.FindModes.exact)), 3)

    def test_find_shortest_route(self):
        self.assertEqual(self.rail.shortest_route('A', 'C'), 9)
        self.assertEqual(self.rail.shortest_route('B', 'B'), 9)

    def test_find_routes_by_distance(self):
        self.assertEqual(len(self.rail.find_routes_by_distance('C', 'C', 30)), 7)
