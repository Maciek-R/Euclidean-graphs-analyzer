import graph_test_generator as test_generator
import graph_diagrams

def testNodes(startFrom, endTo, step, radius, numberOfTests):
	t1 = test_generator.testNumberOfNodes(startFrom, endTo,step, radius, numberOfTests)
	graph_diagrams.createPngForTestNumberOfNodes(t1, startFrom, endTo, radius)
	
def testRadius(startFrom, endTo, step, numberOfNodes, numberOfTests):
	t2 = test_generator.testRadius(startFrom, endTo, step, numberOfNodes, numberOfTests)
	graph_diagrams.createPngForTestRadius(t2, startFrom*0.1,  endTo*0.1, numberOfNodes)