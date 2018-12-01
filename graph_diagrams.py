import pylab
import os

picturesFolder = 'pictures/'

def createPngForTestNumberOfNodes(tests, startFrom, endTo, radius):
	numberOfNodes = list(map(lambda x: x[0], tests))
	radiuses = list(map(lambda x: x[1], tests))
	probabilities = list(map(lambda x: x[2], tests))
	meanNumbersOfConnectedComponent = list(map(lambda x: x[3], tests))
	
	pylab.clf()
	pylab.plot(numberOfNodes, probabilities)
	pylab.title('Prawdopodobienstwa spojnosci grafu od liczby wierzcholkow dla r = ' + str(radius))
	pylab.grid(True)
	if not os.path.exists(picturesFolder):
		os.makedirs(picturesFolder)
	fileName = picturesFolder + 'Nodes_' + str(startFrom) + '_' + str(endTo) + '_' + str(radius) + '.png'
	pylab.savefig(fileName)
	print ('Png saved in file: ' + fileName)
	
def createPngForTestRadius(tests, startFrom, endTo, noNodes):
	numberOfNodes = list(map(lambda x: x[0], tests))
	radiuses = list(map(lambda x: x[1], tests))
	probabilities = list(map(lambda x: x[2], tests))
	meanNumbersOfConnectedComponent = list(map(lambda x: x[3], tests))
	
	pylab.clf()
	pylab.plot(radiuses, probabilities)
	pylab.title('Prawdopodobienstwa spojnosci grafu od promienia dla n = ' + str(noNodes))
	pylab.grid(True)
	if not os.path.exists(picturesFolder):
		os.makedirs(picturesFolder)
	fileName = picturesFolder + 'Radius_' + str(startFrom) + '_' + str(endTo) + '_' + str(noNodes) + '.png'
	pylab.savefig(fileName)
	print ('Png saved in file: ' + fileName)