class GeoLib:
    def __init__(self, place_name, log=False):
        import networkx as nx
        import osmnx as ox
        self.ox = ox
        self.nx = nx
        self.ox.config(use_cache=True, log_console=log)
        print(f'Looking for {place_name}...')
        self.place_name = place_name
        try:
            self.place = self.ox.graph_from_place(place_name,
                                                  network_type='walk')
        except Exception as e:
            print(f"City doesn't exist. Msg: {e.message}")
        self.streets = self._get_streets()

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

    def street_replacement(self, street):
        msg = f"\"{street}\" doesn't found, do you mean:\n"
        for sn in self.streets:
            if street in sn:
                msg += f'  - "{sn}"?\n'
        return msg

    def get_block(self, street, num_1, num_2):
        assert street in self.streets, self.street_replacement(street)
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

    def _get_streets(self):
        G = self.ox.graph_from_address(self.place_name,
                                       dist=2000,
                                       network_type='walk')
        G = self.ox.get_undirected(G)
        streets = []
        for _, edge in self.ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows():
            street_name = edge['name']
            if type(street_name) is list:
                for sn in street_name:
                    if sn != '' and sn not in streets:
                        streets.append(sn)
            else:
                if street_name != '' and street_name not in streets:
                    streets.append(street_name)
        return streets
