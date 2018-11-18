import pylab
import os

picturesFolder = 'pictures/'

def createPngForTestNumberOfNodes(tests, startFrom, endTo, radius):
	numberOfNodes = list(map(lambda x: x[0], tests))
	radiuses = list(map(lambda x: x[1], tests))
	probabilities = list(map(lambda x: x[2], tests))
	meanNumbersOfConnectedComponent = list(map(lambda x: x[3], tests))
	
	pylab.plot(numberOfNodes, probabilities)
	pylab.title('Prawdopodobienstwa spojnosci grafu od liczby wierzcholkow dla r = ' + str(radius))
	pylab.grid(True)
	if not os.path.exists(picturesFolder):
		os.makedirs(picturesFolder)
	pylab.savefig(picturesFolder + str(startFrom) + '_' + str(endTo) + '_' + str(radius) + '.png')