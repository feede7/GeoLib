from random import randint

from geolib import GeoLib

city = GeoLib('San Justo, Buenos Aires, Argentina')

# G = city.get_city_html()
G = city.place
m1 = G.copy()
m1 = city.place

folium = True

nodes = city.ox.graph_to_gdfs(G, edges=False)
print(len(nodes))

# valen en San Justo
# matheu = city.get_block('Matheu', 2500, 2200)
# junin = city.get_block('Montañeses', 4600, 4700)

matheu = city.get_block('Matheu', 2500, 2200, 'r')
junin = city.get_block('Montañeses', 3600, 3700, 'b')
# nodes_in_polygon = nodes[nodes.within(matheu['geometry'])]
# print(len(nodes_in_polygon))

# routes = [matheu, junin]
routes = [junin, matheu]
errors = []
if folium:
    # m2 = city.get_route_html(matheu, color=randint(0x20, 0x20000))
    m2 = None
    for r in routes:
        try:
            m2 = city.get_route_html(r['route'], m2, r['color'])
        except Exception:
            errors.append(f" - Route {r['name']} doesn't exist")

    # m2 = city.get_route_html(junin)
    # m2 = city.get_route_html(matheu, route_map=m2)

    # m2 = None
    # for r in routes:
    #     m2 = city.get_route_html(r, route_map=m2, color=randint(0x20, 0x20000))

    filepath = "data/graph.html"
    m2.save(filepath)
    if len(errors) > 0:
        print('Error list:')
        for e in errors:
            print(e)
    # print(ax)
else:
    city.plot_route(junin, 'r', 1)
