class GeoLib:
    def __init__(self, place_name):
        import networkx as nx
        import osmnx as ox
        self.ox = ox
        self.nx = nx
        print(f'Looking for {place_name}...')
        self.place_name = place_name
        try:
            self.place = ox.graph_from_place(place_name,
                                             network_type='walk')
        except Exception as e:
            print(f"City doesn't exist. Msg: {e.message}")

    def plot_city(self):
        self.ox.plot_graph(self.place)

    def get_geo(self, point_name):
        return self.ox.geocode(point_name)

    def get_geo_node(self, direction):
        point_name = f'{direction}, {self.place_name}'
        point = self.get_geo(point_name)
        node = self.ox.nearest_nodes(self.place,
                                     Y=point[0],
                                     X=point[1])
        return node

    def get_route(self, dir_1, dir_2, name=''):
        geo_1 = self.get_geo_node(dir_1)
        geo_2 = self.get_geo_node(dir_2)
        route = self.nx.shortest_path(self.place, geo_1,
                                      geo_2,
                                      weight=name)
        return route

    def get_block(self, street, num_1, num_2):
        dir_1 = f'{street} {num_1}'
        dir_2 = f'{street} {num_2}'
        name = f'{street} {num_1}-{num_2}'
        block = self.get_route(dir_1, dir_2, name)
        return block

    def plot_route(self, route, color, orig_dest_size):
        self.ox.plot_graph_route(self.place, route,
                                 route_color=color,
                                 orig_dest_size=orig_dest_size)

    def plot_routes(self, routes, colors, orig_dest_size=1):
        if type(routes) is not list:
            assert type(colors) is not list
            self.plot_route(routes, colors, orig_dest_size)
        elif len(routes) == 1:
            assert len(colors) == 1
            self.plot_route(routes[0], colors[0], orig_dest_size)
        else:
            self.ox.plot_graph_routes(self.place, routes,
                                    route_colors=colors,
                                    route_linewidth=6,
                                    node_size=0,
                                    bgcolor='k',
                                    orig_dest_size=orig_dest_size)
