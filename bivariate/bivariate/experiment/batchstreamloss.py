import time
import logging as logger
import os
from pylab import *
from bivariate.learner.batchbivariate import BatchBivariateLearner
from bivariate.generator.billmatlabgenerator import *
from bivariate.evaluator.rootmeaneval import *

DATA_ROOT="/home/ss/Dropbox/TrendMiner/deliverables/year2-18month"\
					+"/Austrian Data"
EXPERIMENTS_ROOT=os.sep.join([DATA_ROOT,"batchStreamLossExperiments"])
EXPERIMENT_NAME="batch_%d"%(time.time()*1000)
EXPERIMENT_ROOT=os.sep.join([EXPERIMENTS_ROOT,EXPERIMENT_NAME])
MATLAB_DATA=os.sep.join([DATA_ROOT,"data.mat"])

NSTEPS = 20

def prepareExperiment():
	os.makedirs(EXPERIMENT_ROOT)

def runExperiment():
	spamsDict = {
		"numThreads": 1, 
		"lambda1": 0.0001,
		"bivar_it0": 3, 
		"bivar_max_it": 10,
		"max_it":500,
		"tol":1e-3,
		"intercept":True, 
	}
	spamsDict['compute_gram'] = True
	spamsDict["loss"] = "square"
	spamsDict["regul"] = "l1l2"
	learner = BatchBivariateLearner(**spamsDict)
	gen = BillMatlabGenerator(MATLAB_DATA,98,True)
	evaluator = RootMeanSumSquareEval(learner)
	for i in range(20):
		X,Y = gen.generate()
		if learner.w is not None and learner.u is not None:
			loss = evaluator.evaluate(X,Y)
			logger.info("New Item Seen: %d"%i)
			logger.info("Loss: %2.5f"%loss)
			logger.info("W sparcity: %2.2f"%learner._wsparcity())
			logger.info("U sparcity: %2.2f"%learner._usparcity())
			logger.info("Bias: %s"%learner.bias)
			logger.info("The predictions:")
			for t in range(Y.shape[1]):
				dotproduct = learner.u[:,t:t+1].T.dot(X.T).dot(learner.w[:,t:t+1])[0,0]
				withoutbias = dotproduct
				dotproduct += learner.bias[0,t]
				logger.info("task=%d,y=%2.5f,v=%2.5f,vb=%2.5f,rse=%2.5f"%(
					t,Y[0,t],dotproduct,withoutbias,
					sqrt(pow(Y[0,t]-dotproduct,2))
				))
			# calculate loss of Y for new X
			pass
		learner.process(X,Y)

if __name__ == '__main__':
	runExperiment()