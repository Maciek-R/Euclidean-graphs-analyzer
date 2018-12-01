import pylab
import os

picturesFolder = 'pictures/'

def createPngForTestNumberOfNodes(tests, startFrom, endTo, radius):
	numberOfNodes = list(map(lambda x: x[0], tests))
	radiuses = list(map(lambda x: x[1], tests))
	probabilities = list(map(lambda x: x[2], tests))
	meanNumbersOfConnectedComponent = list(map(lambda x: x[3], tests))
	
	fileName = picturesFolder + 'Nodes_' + str(startFrom) + '_' + str(endTo) + '_' + str(radius) + '.png'
	createPng(numberOfNodes, probabilities, fileName, 'Prawdopodobienstwa spojnosci grafu od liczby wierzcholkow dla r = ' + str(radius))
	
	for i in range(len(numberOfNodes)):
		meanNumbersOfConnectedComponent[i] = meanNumbersOfConnectedComponent[i] / numberOfNodes[i]
	
	fileName = picturesFolder + 'ConnectedN_' + str(startFrom) + '_' + str(endTo) + '_' + str(radius) + '.png'
	createPng(numberOfNodes, meanNumbersOfConnectedComponent, fileName, 'Procent liczby skladowych spojnych od liczby wierzcholkow dla r = ' + str(radius))
	
def createPngForTestRadius(tests, startFrom, endTo, noNodes):
	numberOfNodes = list(map(lambda x: x[0], tests))
	radiuses = list(map(lambda x: x[1], tests))
	probabilities = list(map(lambda x: x[2], tests))
	meanNumbersOfConnectedComponent = list(map(lambda x: x[3], tests))
	
	fileName = picturesFolder + 'Radius_' + str(startFrom) + '_' + str(endTo) + '_' + str(noNodes) + '.png'
	createPng(radiuses, probabilities, fileName, 'Prawdopodobienstwa spojnosci grafu od promienia dla n = ' + str(noNodes))
	
	fileName = picturesFolder + 'ConnectedR_' + str(startFrom) + '_' + str(endTo) + '_' + str(noNodes) + '.png'
	createPng(radiuses, meanNumbersOfConnectedComponent, fileName, 'Liczba skladowych spojnych od promienia dla n = ' + str(noNodes))
	
def createPng(axisX, axisY, fileName, title):
	if not os.path.exists(picturesFolder):
		os.makedirs(picturesFolder)
	pylab.clf()
	pylab.plot(axisX, axisY)
	pylab.title(title)
	pylab.grid(True)
	pylab.savefig(fileName)
	print ('Png saved in file: ' + fileName)