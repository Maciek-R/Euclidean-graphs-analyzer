import pylab
import os
from mpl_toolkits import mplot3d
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

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
	
def createPngForTestNodesAndRadius(tests):
	numberOfNodes = list(map(lambda x: x[0], tests))
	radiuses = list(map(lambda x: x[1], tests))
	probabilities = list(map(lambda x: x[2], tests))
	meanNumbersOfConnectedComponent = list(map(lambda x: x[3], tests))
	
	fileName = picturesFolder + '3D' + '.png'
	createPng3D(numberOfNodes, radiuses, probabilities, fileName)
	
def createPng(axisX, axisY, fileName, title):
	if not os.path.exists(picturesFolder):
		os.makedirs(picturesFolder)
	pylab.clf()
	pylab.plot(axisX, axisY)
	pylab.title(title)
	pylab.grid(True)
	pylab.savefig(fileName)
	print ('Png saved in file: ' + fileName)
	
def createPng3D(axisX, axisY, axisZ, fileName):
	if not os.path.exists(picturesFolder):
		os.makedirs(picturesFolder)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(axisX, axisY, axisZ, c='r', marker='o')
	ax.set_xlabel('Number of nodes')
	ax.set_ylabel('Radius')
	ax.set_zlabel('Probability')
	plt.savefig(fileName)