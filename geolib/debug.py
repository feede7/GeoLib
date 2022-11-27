from random import randint

from geolib import GeoLib

city = GeoLib('San Justo, Buenos Aires, Argentina')

G = city.place
m1 = G.copy()
m1 = city.place

streets = city.streets.keys()
zero = 0
up_to = 4000

routes = []streets.keys()

l_s = len(streets)
for i, street in enumerate(streets):
    print(f'{i}/{l_s}: {street}')
    for h in range((up_to - zero) // 100):
        a = zero + h*100
        b = zero + (h + 1)*100
        c = city.get_block_iter(street, a, b, 'random')
        if c['route'] is not None:
            routes.append(c)

errors = []
m2 = city.get_city_html()
for r in routes:
    try:
        m2 = city.get_route_html(r['route'], m2, r['color'])
    except Exception:
        errors.append(f" - Route {r['name']} doesn't exist")

filepath = "data/graph.html"
m2.save(filepath)
if len(errors) > 0:
    print('Error list:')
    for e in errors:
        print(e)
