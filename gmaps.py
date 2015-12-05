import requests, json, math, time
import numpy as np
import matplotlib.pyplot as plt

magny_coords = (48.742858,2.087692)
#https://maps.googleapis.com/maps/api/distancematrix/json?
#origins=Chateaufort+France|
#{41.85,87.65}&
#destinations=Gennevilliers+France|
#Osny+France&
#mode=driving&
#language=en-UK&
#arrival_time=1451462400

#https://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&key=YOUR_API_KEY

key='AIzaSyCDvH_uX4_Q_u4j60hJLv2t-kPcenfWQoY'
key2 = "AIzaSyD45UNxHE2IawL2RIbdzM2iewz64gHI5PE"

def build_grid(coords, scales, numsteps):
   deltas = [(x, y) for x in range(-numsteps[0], numsteps[0])\
             for y in range(-numsteps[1], numsteps[1])]
   deltas = filter(lambda x: x[0] != 0 and x[1] != 0, deltas)
   return map(lambda a: (coords[0] + a[0]*scales[0],
                         coords[1] + a[1]*scales[0]), deltas)


def build_circle(center, radius, density):
   num = math.ceil(2 * math.pi * radius / density)
   deltas = []
   for i in range(num):
      deltas.append((radius * math.cos(2 * math.pi * i / num), radius * math.sin(2 * math.pi * i / num)))
   coords = map(lambda x: (round(x[0] + center[0], 6), round(x[1] + center[1], 6)), deltas)
   return coords

def build_circles(center, max_radius, density):
   res = []
   radiuses = map(lambda x: x * density, range(1, math.ceil(max_radius/density)))
   for r in radiuses:
      res.extend(list(build_circle(center, r, density)))
   return res


#b = build_circles((0, 0), 10, 1)
#plt.scatter(list(map(lambda x: x[0], b)), list(map(lambda x: x[1], b)), alpha=0.5)
#plt.show()

def grid_to_csv(grid):
   res = "longtitude,latitude\n"
   lines = map(lambda x: str(round(x[1],6)) + "," + str(round(x[0], 6)), grid)
   res += "\n".join(lines)
   return res

def couple_to_string(couple):
    return "{" + str(round(couple[0], 6)) + "," + str(round(couple[1], 6)) + "}"

def list_to_string(list):
    return "|".join(map(couple_to_string, list))

#print(list(build_grid(magny_coords, (0.1, 0.2), (10, 10))))

#+ "&arrival_time=" + str(timestamp)

def build_request(origins, destinations, timestamp):
    req = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="\
          + list_to_string(origins) + "&destinations="\
          + list_to_string(destinations) + "&mode=driving" \
          + "&language=fr-FR&key=" + key
    return req

def build_request_to(origins, destination, timestamp):
    req = "https://maps.googleapis.com/maps/api/distancematrix/json?origins="\
          + list_to_string(origins) + "&destinations="\
          + destination + "&mode=driving" \
          + "&language=fr-FR&key=" + key
    return req

#def build_rgeo_request(coords):
#    return "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(coords[0]) + "," + str(coords[1]) + "&language=en-UK&key=" + key2

def build_rgeo_request(coords):
   return "http://api-adresse.data.gouv.fr/reverse/?lat=" + str(round(coords[0], 6)) + "&lon=" + str(round(coords[1], 6))


def build_rgeo_requests(center, max_radius, density):
   coords = build_circles(center, max_radius, density)
   requests = map(build_rgeo_request, coords)
   return requests


def request_with_pause(reqs, pause):
   res = []
   for request in reqs:
      r = requests.get(request)
      time.sleep(pause)
      res.append(r.text)
   return res


def filter_results(results):
   r = map(json.loads, results)
   r = filter(lambda x: x['features'] != [], r)
   return map(lambda x: x['features'][0]['properties']['label'], r)

res = request_with_pause(build_rgeo_requests((48.742858,2.087692), .2, .05), .1)
for i in filter_results(res):
   print(i)
#rg = build_rgeo_requests((48.742858,2.087692), 30, 3)
#for i in rg:
#   print(i)
#print(build_rgeo_request((48.742858,2.087692)))


#req = build_request(build_grid(magny_coords, (.05, .05), (2, 2)), [magny_coords], 1451462400)
#print(req)

#req_to = build_request_to(build_grid(magny_coords, (1.5, 1.5), (2, 2)), "1+rue+Genevieve+Aube+Chateaufort+France", 1451462400)

#print(grid_to_csv(build_grid(magny_coords, (.05, .05), (2, 2))))



#req_geo =  requests.post('http://api-adresse.data.gouv.fr/reverse/csv/',
#                         data = {'data' : grid_to_csv(build_grid(magny_coords, (1.5, 1.5), (2, 2)))})
#r = requests.get(req_to)
#r = requests.get(build_rgeo_request(magny_coords))
#print(r.status_code)
#print(r.text)

#print(req_geo.status_code)
#print(req_geo.text)

#r = requests.get(build_rgeo_request((48.742858,2.087692)))
#print(r.status_code)
#print(json.decode(r.text))
