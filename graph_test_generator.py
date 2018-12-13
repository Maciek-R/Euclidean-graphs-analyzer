from graph_generator import *
from functools import reduce

def testNumberOfNodes(start_from, end_to, step, radius, numberOftests):
	tests = []
	numberOfNodesToTest = []
	
	for noTest in range(start_from, end_to, step):
		numberOfNodesToTest.append(noTest)
	
	for noNodes in numberOfNodesToTest:
		tests.append(test(numberOftests, noNodes, radius, False))
		
	return tests
	
def testRadius(start_from, end_to, step, numberOfNodes, numberOftests):
	tests = []
	numberOfRadiusesToTest = []
	
	for noTest in range(start_from, end_to, step):
		numberOfRadiusesToTest.append(noTest*0.1)
	
	for radius in numberOfRadiusesToTest:
		tests.append(test(numberOftests, numberOfNodes, radius, False))
		
	return tests
	
def testNumberOfNodesAndRadius(start_nodes_from, end_nodes_to, step_nodes, start_radius_from, end_radius_to, step_radius, numberOftests):
	tests = []
	nodesAndRadiusesToTest = []
	
	for numNode in range(start_nodes_from, end_nodes_to, step_nodes):
		for numRadius in range(start_radius_from, end_radius_to, step_radius):
			nodesAndRadiusesToTest.append((numNode, numRadius*0.1))
	
	for numNodes, numRadius in nodesAndRadiusesToTest:
		tests.append(test(numberOftests, numNodes, numRadius, False))
		
	return tests

def test(numberOfTestsForOneGraph, numberOfNodes, radius, debug = True):
	print('Test with n = ' + str(numberOfNodes) + ' r = ' + str(radius*0.1))
	numberOfTests = numberOfTestsForOneGraph
	numberOfConsistentGraphs = 0
	numberOfMaxConnectedComponents = [0] * numberOfTests
	
	for noTest in range(numberOfTests):
		graph = generateGraph(numberOfNodes, radius)
		if(graph.isConsistent()):
			numberOfConsistentGraphs = numberOfConsistentGraphs + 1
			numberOfMaxConnectedComponents[noTest] = len(graph.nodes)
		else:
			numberOfMaxConnectedComponents[noTest] = graph.countMaxSizeOfConnectedComponent()
			
	p = numberOfConsistentGraphs/numberOfTests
	mean = reduce(lambda x, y: x + y, numberOfMaxConnectedComponents)/numberOfTests
	if(debug == True):
		print('Prawdopodobienstwo spojnosci sieci dla: ')
		print('n = ' + str(numberOfNodes) + ' r = ' + str(radius))
		print('Liczba testow: ' + str(numberOfTests))
		print('Prawdopodobienstwo: ' + str(p))
		print('Srednia maksymalna liczba wspolnych skladowych: ' + str(mean))
		
	return (numberOfNodes, radius, p, mean)