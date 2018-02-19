import numpy as np;
from Sampler import GibbsSampler;

####################################################################
# CLASS: ConditionalDistribution
# Samples a point after conditioning over the joint Distribution
#
# sigma: variance matrix of the conditional distribution
#
# pre_mew: incomplete mean for the conditioned distribution
#		   final mean depends on the observed value X2 so final mean
#		   is calculated on the fly together with mu1 and mu2
#		   using formula: mu1 + pre_mew*(x-mu2)
#
# mu1 : mean for the variable to be sampled
# mu2 : mean for the observed variable 
#
#
####################################################################
class ConditionalDistribution(object):
	
	#Initialize the variables
	def __init__(self,sig,p_mew,mew1,mew2):
		self.sigma=sig;
		self.pre_mew=p_mew.reshape((p_mew.shape[0],-1));
		self.mu1 = mew1;
		self.mu2 = mew2;

	#Given a variable x2 that was observed, Return a sample 
	#from the new distribution conditioned on the observed value
	def getSample(self,x2,iterations=200):
		
		diff = x2-self.mu2;
		final_mew = self.mu1 + self.pre_mew.dot(diff);
		final_sig = self.sigma;
		
		sampler = GibbsSampler(final_mew,final_sig,iterations);
		pt=sampler.SampledPoint();										#sample a point from this distribution
		return pt.reshape(-1);
