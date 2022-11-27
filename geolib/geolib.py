from random import randint


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
            self.place = self.ox.graph_from_place(place_name, network_type='walk')
        except Exception as e:
            print(f"City doesn't exist. Msg: {e.message}")
        print('Gotcha!')
        self.streets = self._get_streets()

    def get_city_html(self, color="#A0A0A0"):
        return self.ox.plot_graph_folium(self.place,
                                         popup_attribute="name",
                                         weight=1,
                                         color=color,
                                         opacity=0.4)

    def plot_city(self):
        return self.ox.plot_graph(self.place)

    def get_geo(self, point_name):
        return self.ox.geocode(point_name)

    def get_geo_node(self, direction):
        point_name = f'{direction}, {self.place_name}'
        point = self.get_geo(point_name)
        node = self.ox.nearest_nodes(self.place,
                                     Y=point[0],
                                     X=point[1])
        return node

    def street_replacement(self, street):
        msg = f"\"{street}\" doesn't found, do you mean:\n"
        for sn in self.streets.keys():
            if street in sn:
                msg += f'  - "{sn}"?\n'
        return msg

    def get_block(self, street, num_1, num_2, color):
        assert street in self.streets.keys(), self.street_replacement(street)
        dir_1 = f'{street} {num_1}'
        dir_2 = f'{street} {num_2}'
        block = {}
        block['route'] = self.get_route(dir_1, dir_2)
        block['name'] = f'{street} {num_1}-{num_2}'
        block['color'] = color
        return block

    def get_route(self, dir_1, dir_2):
        geo_1 = self.get_geo_node(dir_1)
        geo_2 = self.get_geo_node(dir_2)
        route = self.nx.shortest_path(self.place, geo_1,
                                      geo_2)
        return route

    def get_block_iter(self, street, num_1, num_2, color,
                       loops=3, step=10):
        block = {}
        block['route'] = None
        block['name'] = f'{street} {num_1}-{num_2}'
        block['color'] = color
        assert street in self.streets.keys(), self.street_replacement(street)
        for ll in range(loops):
            if num_1 < num_2:
                dir_1 = f'{street} {num_1 + (ll * step)}'
                dir_2 = f'{street} {num_2 - (ll * step)}'
            else:
                dir_1 = f'{street} {num_2 + (ll * step)}'
                dir_2 = f'{street} {num_1 - (ll * step)}'
            try:
                route = self.get_route(dir_1, dir_2)
                if len(route) <= 3:
                    block['route'] = route
                    break
                # else:
                #     print(f'l: {ll}: {len(route)}')
            except Exception as e:
                # if e.message.find('Nomination could not') :
                break
        return block

    def get_route_html(self, route, route_map, color):
        colors = {'r': '#ff0000',
                  'g': '#00ff00',
                  'b': '#0000ff',
                 }
        if color == 'random':
            bands = 3
            rand_int = [randint(16, 255) for _ in range(bands)]
            rand_hex = [format(r, '#04x').replace('0x', '') for r in rand_int]
            rand_color = '#'
            for c in rand_hex:
                rand_color += c
            colors['random'] = rand_color

        assert color in colors.keys()
        return self.ox.plot_route_folium(self.place, route,
                                         popup_attribute='name',
                                         route_map=route_map,
                                         color=colors[color],
                                         opacity=0.5)

    def get_route_html2(self, route, route_map):
        return self.ox.plot_graph_folium(self.place, route,
                                         graph_map=route_map,
                                         color='#00ff00',
                                         opacity=0.5)

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

    def _get_streets(self, skip=['Rotonda']):
        G = self.ox.graph_from_address(self.place_name,
                                       dist=2000,
                                       network_type='walk')
        G = self.ox.get_undirected(G)
        streets = {}
        for _, edge in self.ox.graph_to_gdfs(G, nodes=False).fillna('').iterrows():
            street_name = edge['name']
            street_name = street_name if type(street_name) is list else [street_name]
            for sn in street_name:
                if sn != '' and sn not in streets.keys() and sn not in skip:
                    streets[sn] = {}
                else:
                    # add min, max
                    pass
        return streets
