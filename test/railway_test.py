import unittest

from railway import Railway


class RailwayTest(unittest.TestCase):
    def test_validate_and_parse_route(self):
        route = None
        self.assertRaises(ValueError, Railway.validate_and_parse_route, route)

        route = ''
        self.assertRaises(ValueError, Railway.validate_and_parse_route, route)

        route = 'A'
        self.assertRaises(ValueError, Railway.validate_and_parse_route, route)

        route = 'A 5'
        self.assertRaises(ValueError, Railway.validate_and_parse_route, route)

        route = 'DED'
        self.assertRaises(ValueError, Railway.validate_and_parse_route, route)

        route = 'zA4'
        self.assertRaises(ValueError, Railway.validate_and_parse_route, route)

        route = 'A$4'
        self.assertRaises(ValueError, Railway.validate_and_parse_route, route)

        route = 'AE5'
        self.assertEqual(Railway.validate_and_parse_route(route), ('A', 'E', 5))

    def test_init_add_routes(self):
        self.assertRaises(TypeError, Railway)

        routes = ['AB1', 'AC2', 'CA4']
        rail = Railway(routes)
        self.assertEqual(rail.routes['A']['B'], 1)
        self.assertEqual(rail.routes['A']['C'], 2)
        self.assertEqual(rail.routes['C']['A'], 4)

        routes = 'DE3, FD7, AG2'
        rail = Railway(routes)
        self.assertEqual(rail.routes['D']['E'], 3)
        self.assertEqual(rail.routes['F']['D'], 7)
        self.assertEqual(rail.routes['A']['G'], 2)

    def test_get_route_distance(self):
        routes = ['AB1', 'AC2', 'CA4']
        rail = Railway(routes)
        self.assertRaises(ValueError, rail.get_route_distance, None, 'A')
        self.assertRaises(KeyError, rail.get_route_distance, 'D', 'A')
        self.assertEqual(rail.get_route_distance('A', 'B'), 1)
        self.assertEqual(rail.get_route_distance('A', 'C'), 2)
        self.assertEqual(rail.get_route_distance('C', 'A'), 4)
        self.assertEqual(rail.get_route_distance('A', 'C', 'A'), 6)
        self.assertEqual(rail.get_route_distance('B', 'C'), None)

    def test_find_routes_by_stops(self):
        routes = ['AB1', 'AC2', 'CA4']
        rail = Railway(routes)
        self.assertRaises(ValueError, rail.find_routes_by_stops, None, 'A', 5)
        self.assertRaises(ValueError, rail.find_routes_by_stops, 'A', 'B', 'Z')
        self.assertRaises(KeyError, rail.find_routes_by_stops, 'D', 'A', 5)
        self.assertEqual(rail.find_routes_by_stops('A', 'A', 3), [(['A', 'C', 'A'], 6)])
        self.assertEqual(rail.find_routes_by_stops('A', 'A', '3'), [(['A', 'C', 'A'], 6)])
        self.assertEqual(rail.find_routes_by_stops('A', 'C', 3), [(['A', 'C'], 2)])
        self.assertEqual(rail.find_routes_by_stops('A', 'C', 4, Railway.FindModes.exact), [])
        self.assertEqual(rail.find_routes_by_stops(
            'A', 'C', 5, Railway.FindModes.exact),
            [(['A', 'C', 'A', 'C', 'A', 'C'], 14)]
        )

    def test_find_routes_by_distance(self):
        routes = ['AB1', 'AC2', 'CA4']
        rail = Railway(routes)
        self.assertRaises(ValueError, rail.find_routes_by_distance, None, 'A', 5)
        self.assertRaises(ValueError, rail.find_routes_by_distance, 'A', 'B', 'Z')
        self.assertRaises(KeyError, rail.find_routes_by_distance, 'D', 'A', 5)
        self.assertEqual(rail.find_routes_by_distance('A', 'B', -1), [])
        self.assertEqual(rail.find_routes_by_distance('A', 'B', 0), [])
        self.assertEqual(rail.find_routes_by_distance('A', 'B', 2), [['A', 'B', 1]])
        self.assertEqual(
            rail.find_routes_by_distance('A', 'C', 14),
            [['A', 'C', 2], ['A', 'C', 'A', 'C', 8]]
        )
        self.assertEqual(
            rail.find_routes_by_distance('A', 'C', 15),
            [['A', 'C', 2], ['A', 'C', 'A', 'C', 8], ['A', 'C', 'A', 'C', 'A', 'C', 14]]
        )
        self.assertEqual(len(rail.find_routes_by_distance('A', 'C', 1000)), 167)

    def test_shortest_route(self):
        routes = ['AB1', 'AC2', 'CA4', 'CD1', 'DA1']
        rail = Railway(routes)
        self.assertRaises(ValueError, rail.shortest_route, None, 'A')
        self.assertEqual(rail.shortest_route('A', 'B'), 1)
        self.assertEqual(rail.shortest_route('B', 'C'), float('inf'))
        self.assertEqual(rail.shortest_route('C', 'A'), 2)
