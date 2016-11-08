import numpy as np

class Point:
	visited = False
	group = "BRAK"
	iloscSasiadow = 0

	def __init__(self,coord):
		if (len(coord) == 0):
			self.x = np.random.random()
			self.y = np.random.random()
			self.coord = []
			self.coord.append(self.x)
			self.coord.append(self.y)
		else:
			self.x = coord[0]
			self.y = coord[1]
			self.coord = coord

def dbscan_pklasa(points, minPts = 10, eps = 0.1):
	groupNo = 0
	for point in points:
		if point.visited == True :
			continue
		point.visited = True
		neighbourPts = getNeighbour(point, points , eps)
		if len(neighbourPts) <= minPts :
			point.group = "NOISE" 
		else:
			groupNo+=1
			expandCluster(point, neighbourPts, groupNo, eps, minPts, points)		
	return groupNo
		
def getNeighbour(point,points,eps):
	neighbour = []
	for potNeig in points:
		if (dist(potNeig , point) < eps) and (point != potNeig):
			neighbour.append(potNeig)
	point.iloscSasiadow = len(neighbour)
	return neighbour

def dist(p1 , p2):
	dist = 0.0
	for i in range(len(p1.coord)):
		dist = dist + ( p1.coord[i] - p2.coord[i] ) ** 2
	return dist ** (1/2)
	
def expandCluster(point, neighbour, groupNo, eps, minPts, points):
	point.group = "CLUSTER" + str(groupNo)
	cluster = []
	cluster.extend(neighbour)
	
	while( len(cluster) > 0 ):
		newPoint = cluster[0]
		if (newPoint.visited == False):
			newPoint.visited = True
			newPointNeigh = getNeighbour(newPoint, points, eps)
			if ( len(newPointNeigh) >= minPts):
				cluster.extend(newPointNeigh)
		if (newPoint.group == "BRAK" or newPoint.group == "NOISE"):
			newPoint.group = "CLUSTER" + str(groupNo)
		del cluster[0]
	
''' TWORZENIE LOSOWYCH PUNKTOW '''		
punkty = []
for x in range(300):
	punkty.append(Point([]))		
		

'''punkty.append(Point(0.99,3))
punkty.append(Point(1.04,3.09))
punkty.append(Point(1,3))
punkty.append(Point(1.04,3))
punkty.append(Point(1.13,3))'''

iloscClustrow = dbscan_pklasa(punkty)
print(iloscClustrow)


##############################################################################
# Plot result
import matplotlib.pyplot as plt

colors = plt.cm.Spectral(np.linspace(0, 1, iloscClustrow))
group = 1

for col in colors:
	for pkt in punkty:
		if (pkt.group == "CLUSTER"+str(group)):
			size = 8
			if(pkt.iloscSasiadow > 10):
				size = 16
			plt.plot(pkt.x,pkt.y, 'o', markerfacecolor=col, markeredgecolor='k', markersize=size)
	group+=1

x = []
y = []
for pkt in punkty:
	if (pkt.group == "NOISE"):
		x.append(pkt.x)
		y.append(pkt.y)
plt.plot(x,y, 'o', markerfacecolor="black", markeredgecolor='k', markersize=4)
	
plt.title('Number of clusters: %d' % iloscClustrow)
plt.show()