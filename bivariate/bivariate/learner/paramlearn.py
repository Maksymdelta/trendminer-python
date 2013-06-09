from IPython import embed
import spams
from pylab import *
import logging;logger = logging.getLogger("root")

class LambdaSearch(object):
	"""
	Given an a cost function calculate the
	lambda which gives the best error

	errorfunc - is a bivariate.evaluator.lineareval.LinearEvaluator
				which given an expected Y and an X and calculated W
	"""
	def __init__(self, 
		errorfunc
	):
		super(LambdaSearch, self).__init__()
		self.errorfunc = errorfunc
	
	"""

	spamsfunc - is a bivariate.learner.spamsfunc.SpamsFunctions 
			   which given an X and Y can learn a weighting
	lambda_rng - the range of lambdas to search
	x_parts - the x_parts for this fold, each holds (days*tasks) in the columns
	y_parts - the y_parts for this fold, holds the Y for each task for each day in the diag
	"""
	def optimise(self,spamsfunc, lambda_rng, x_parts, y_parts):
		min_err = None
		min_lambda = None
		for lmbda_i in range(len(lambda_rng)):
			lmbda = lambda_rng[lmbda_i]
			logger.debug("... Testing lambda %2.5f (%d/%d)"%(lmbda,lmbda_i,len(lambda_rng)))
			spamsfunc.params['lambda1'] = lmbda
			theta_new,bias = spamsfunc.call(
				x_parts.train, 
				y_parts.train
			)
			err = self.errorfunc.evaluate(
				x_parts.val_param,
				y_parts.val_param,
				theta_new,
				bias
			)
			if min_err is None or err < min_err:
				min_err = err
				min_lambda = lmbda
			# logger.debug("Lambda = %2.5f, Error = %2.5f"%(lmbda,err)) 
		logger.debug("Lambda = %2.5f, Error = %2.5f"%(min_lambda,min_err)) 
		spamsfunc.params['lambda1'] = min_lambda
		return min_lambda



