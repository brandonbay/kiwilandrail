from enum import Enum
from re import match


class Railway:
    """
    A class representing a Railway

    Attributes
    ----------
    routes : dict
        An adjacency matrix describing a directed weighted graph of the route map.
        The outer key is the origin station, the inner key is the destination station, and the innermost value is the
        distance between the two stations.

    FindModes : enum
        An enum of the allowed modes for the method find_routes_by_stops.

    Methods
    -------
    validate_and_parse_route(route)
        Validates that a route string is in the correct AB1 format and parses it

    add_routes(route_list)
        Adds a list of routes to the route map

    get_route_distance(origin, *destinations)
        Calculates the distance of a given route

    find_routes_by_stops(origin, destination, stops, mode=FindModes.max)
        Finds all the routes between two stations with a given number of stops

    find_routes_by_distance(origin, destination, max_distance)
        Finds all the routes between two stations with a given maximum distance between them

    shortest_route(origin, destination)
        Finds the shortest route between two stations
    """
    routes = {}
    FindModes = Enum('FindModes', 'max exact')

    def __init__(self, routes):
        """
        Parameters
        ----------
        routes : list or str
            The route graph, provided as a list, e.g. ['AB1', 'BC2', 'AC3'],
            or as a string, e.g. 'AB1, BC2, AC3'
        """
        if isinstance(routes, str):
            route_list = [route.strip() for route in routes.split(',')]
        elif isinstance(routes, list):
            route_list = [route.strip() for route in routes]
        else:
            raise ValueError('Routes must be supplied as a list of strings or as a comma-separated string')

        self.add_routes(route_list)

    @classmethod
    def validate_and_parse_route(cls, route):
        """
        Parameters
        ----------
        route : str
            The route, provided as a string, e.g. 'AB1'

        Returns
        -------
        origin : str
            The origin station, provided as a single-character string, e.g. 'A'

        destination : str
            The destination station, provided as a single-character string, e.g. 'B'

        distance : int
            The distance between stations, provided as a single-character string, e.g. 1

        Raises
        ------
        ValueError
            If the route does not match the correct format
        """

        if not route or len(route) < 3:
            raise ValueError('Malformatted route: format is "OD#" where O = origin, D = destination, # = distance')

        origin = route[0]
        destination = route[1]
        distance = int(route[2:])

        if not match(r'[A-Z]', origin) or not match(r'[A-Z]', destination):
            raise ValueError('Station name must be an uppercase letter')

        return origin, destination, distance

    def add_routes(self, route_list):
        """
        Parameters
        ----------
        route_list : list
            The routes, provided as a list of strings, e.g. ['AB1', 'BC2', 'AC3']
        """
        for route in route_list:
            origin, destination, distance = self.validate_and_parse_route(route)

            if origin not in self.routes:
                self.routes[origin] = dict()
            if destination not in self.routes:
                self.routes[destination] = dict()
            self.routes[origin][destination] = distance

    def get_route_distance(self, origin, *destinations):
        """
        Parameters
        ----------
        origin : str
            The origin station, provided as a string, e.g. 'A'

        destinations : str
            One or more destination stations, provided as strings, e.g. 'B', 'C'

        Returns
        -------
        distance : int
            The total distance along the route, or None if the route does not exist

        Raises
        ------
        ValueError
            If one of the stations is not supplied as an argument

        KeyError
            If the origin station is not in the route matrix
        """
        destination = destinations[0]

        if not origin or not destination:
            raise ValueError('Argument not supplied')

        if origin not in self.routes:
            raise KeyError('Origin station not found')

        if destination not in self.routes[origin]:
            return None
        else:
            distance = self.routes[origin][destination]

        if len(destinations) > 1:
            next_stop_distance = self.get_route_distance(destination, *destinations[1:])
            if not next_stop_distance:
                return None
            return distance + next_stop_distance
        else:
            return distance

    def find_routes_by_stops(self, origin, destination, stops, mode=FindModes.max):
        """
        Parameters
        ----------
        origin : str
            The origin station, provided as a string, e.g. 'A'

        destination : str
            The destination station, provided as a string, e.g. 'B'

        stops : int
            The number of stops desired between stations

        mode : FindMode
            The mode by which to consider stops.
            If the mode is FindModes.max, the stops argument will be considered an upper limit.
            If the mode is FindModes.exact, the stops argument will be considered the only allowable number of stops.

        Returns
        -------
        routes : list
            The collection of matching routes, including all stops and distance.
            List is empty if there are no such routes.

        Raises
        ------
        ValueError
            If one of the stations is not supplied as an argument, or if stops is not an int

        KeyError
            If the origin station is not in the route matrix
        """
        if not origin or not destination:
            raise ValueError('Argument not supplied')

        if not isinstance(stops, int):
            try:
                stops = int(stops)
            except:
                raise ValueError('Argument `stops` is not a number')

        if origin not in self.routes:
            raise KeyError('Origin station not found')

        routes = []

        if (mode == self.FindModes.max and stops >= 1) or (mode == self.FindModes.exact and stops == 1):
            if destination in self.routes[origin]:
                path = ([origin, destination], self.routes[origin][destination])
                routes.append(path)
                return routes
            if mode == self.FindModes.exact:
                return []

        if stops != 1 and len(self.routes[origin]) == 0:
            return []

        for next_stop in self.routes[origin]:
            subroutes = self.find_routes_by_stops(next_stop, destination, stops-1, mode)
            if len(subroutes) > 0:
                for subroute in subroutes:
                    path, subroute = subroute
                    path.insert(0, origin)
                    route = (path, self.routes[origin][next_stop] + subroute)
                    routes.append(route)
        return routes

    def find_routes_by_distance(self, origin, destination, max_distance):
        """
        Parameters
        ----------
        origin : str
            The origin station, provided as a string, e.g. 'A'

        destination : str
            The destination station, provided as a string, e.g. 'B'

        max_distance : int
            The maximum distance to find paths, reduced in recursive calls.
            Note that this is a strict less-than comparison - routes with distance equal to this limit will not return.

        Returns
        -------
        routes : list
            The collection of matching routes, including all stops and distance.
            List is empty if there are no such routes.

        Raises
        ------
        ValueError
            If one of the stations is not supplied as an argument, or if the max_distance is not an int

        KeyError
            If the origin station is not in the route matrix
        """
        if not origin or not destination:
            raise ValueError('Argument not supplied')

        if not isinstance(max_distance, int):
            try:
                max_distance = int(max_distance)
            except:
                raise ValueError('Argument `max_distance` is not a number')

        if origin not in self.routes:
            raise KeyError('Origin station not found')

        routes = []
        for stop in self.routes[origin]:
            distance = self.routes[origin][stop]
            if stop == destination and distance < max_distance:
                routes.append([origin, stop, distance])
            if max_distance - distance > 0:
                subroutes = self.find_routes_by_distance(stop, destination, max_distance - distance)
                if len(subroutes) > 0:
                    for subroute in subroutes:
                        if not subroute:
                            continue
                        route = [origin]
                        route.extend(subroute)
                        route[-1] += distance
                        routes.append(route)
        return routes

    def shortest_route(self, origin, destination):
        """
        Parameters
        ----------
        origin : str
            The origin station, provided as a string, e.g. 'A'

        destination : str
            The destination station, provided as a string, e.g. 'B'

        Returns
        -------
        shortest_distance : int
            The minimum distance between the two specified stations

        Raises
        ------
        ValueError
            If one of the stations is not supplied as an argument

        KeyError
            If the origin station is not in the route matrix
        """
        if not origin or not destination:
            raise ValueError('Argument not supplied')

        if origin not in self.routes:
            raise KeyError('Origin station not found')

        shortest_distance = float('inf')
        nodes_to_visit = []

        if destination in self.routes[origin]:
            shortest_distance = self.routes[origin][destination]

        nodes_to_visit.extend([(origin, stop, 0) for stop in self.routes[origin]])
        while len(nodes_to_visit) > 0:
            o, d, distance_to_origin = nodes_to_visit.pop()
            distance = self.routes[o][d] + distance_to_origin
            if distance < shortest_distance:
                for stop in self.routes[d]:
                    nodes_to_visit.extend([(d, stop, distance) for stop in self.routes[d]])
                if d == destination:
                    shortest_distance = min(shortest_distance, distance)

        return shortest_distance
