from railway import Railway

route = 'AB5, BC4, CD8, DC8, DE6, AD5, CE2, EB3, AE7'

def print_menu():
    print('')
    print('Please make a selection from the options below.')
    print('1: The standard set of ten outputs, as given in the problem')
    print('2: Find the total distance of a given route')
    print('3: Find the number of trips between specified stations with a specified maximum number of stops')
    print('4: Find the number of trips between specified stations with a specified exact number of stops')
    print('5: Find the length of the shortest route between two specified stations')
    print('6: Find the number of different routes between specified stations with a specified maximum distance')
    print('M: Display this menu')
    print('X: Exit the Kiwiland railway system')

while True:
    print('Welcome to the Kiwiland railway system!')
    print('Our latest railway map is: {}'.format(route))
    change_graph = input('Is this correct? Y/N: ')
    if change_graph.upper() == 'Y':
        break
    else:
        route = input('Please enter the latest railway map: ')

rail = Railway(route)
print_menu()

while True:
    print('')
    menu_selection = input('Your selection: ').upper()
    if menu_selection == '1':
        print('Output #1: {}'.format(rail.get_route_distance('A', 'B', 'C') or 'NO SUCH ROUTE'))
        print('Output #2: {}'.format(rail.get_route_distance('A', 'D') or 'NO SUCH ROUTE'))
        print('Output #3: {}'.format(rail.get_route_distance('A', 'D', 'C') or 'NO SUCH ROUTE'))
        print('Output #4: {}'.format(rail.get_route_distance('A', 'E', 'B', 'C', 'D') or 'NO SUCH ROUTE'))
        print('Output #5: {}'.format(rail.get_route_distance('A', 'E', 'D') or 'NO SUCH ROUTE'))
        print('Output #6: {}'.format(len(rail.find_routes_by_stops('C', 'C', 3))))
        print('Output #7: {}'.format(len(rail.find_routes_by_stops('A', 'C', 4, Railway.FindModes.exact))))
        print('Output #8: {}'.format(rail.shortest_route('A', 'C')))
        print('Output #9: {}'.format(rail.shortest_route('B', 'B')))
        print('Output #10: {}'.format(len(rail.find_routes_by_distance('C', 'C', 30))))
    elif menu_selection == '2':
        origin = input('Please enter the origin station: ')
        next_stop = input('Please enter the destination station: ')
        stops = [next_stop]
        while True:
            next_stop = input('Please enter the next destination station, or ! to stop: ')
            if next_stop == '!':
                break
            else:
                stops.append(next_stop)
        distance = rail.get_route_distance(origin, *stops)
        if not distance:
            print('NO SUCH ROUTE')
        else:
            print('The distance along route {}-{} is: {}'.format(origin, '-'.join(stops), distance))
    elif menu_selection == '3':
        origin = input('Please enter the origin station: ')
        destination = input('Please enter the destination station: ')
        stops = input('Please enter the maximum total number of stops: ')
        routes = rail.find_routes_by_stops(origin, destination, int(stops))
        if not routes or len(routes) == 0:
            print('NO SUCH ROUTE')
        else:
            print('There are {} routes: {}'.format(len(routes), ['-'.join(route[0]) + ' ({})'.format(route[1]) for route in routes]))
    elif menu_selection == '4':
        origin = input('Please enter the origin station: ')
        destination = input('Please enter the destination station: ')
        stops = input('Please enter the exact total number of stops: ')
        routes = rail.find_routes_by_stops(origin, destination, int(stops), Railway.FindModes.exact)
        if not routes or len(routes) == 0:
            print('NO SUCH ROUTE')
        else:
            print('There are {} routes: {}'.format(len(routes), ['-'.join(route[0]) + ' ({})'.format(route[1]) for route in routes]))
    elif menu_selection == '5':
        origin = input('Please enter the origin station: ')
        destination = input('Please enter the destination station: ')
        shortest_route = rail.shortest_route(origin, destination)
        if shortest_route == float('inf'):
            print('NO SUCH ROUTE')
        else:
            print('The shortest route between {} and {} is {}'.format(origin, destination, shortest_route))
    elif menu_selection == '6':
        origin = input('Please enter the origin station: ')
        destination = input('Please enter the destination station: ')
        distance = input('Please enter the maximum total distance: ')
        routes = rail.find_routes_by_distance(origin, destination, int(distance))
        print('There are {} routes: {}'.format(len(routes), ['-'.join(route[:-1]) + ' ({})'.format(route[-1]) for route in routes]))
    elif menu_selection == 'M':
        print_menu()
    elif menu_selection == 'X':
        print('Goodbye!')
        break
    else:
        print('Invalid selection. Please try again.')
