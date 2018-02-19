import numpy as np;

#################################################################
# CLASS: GibbsSampler
# Samples a point from a distribution using Gibbs Sampling
#
# mew: the mean vector for the distribution to be sampled from
# sigma: covariance matrix for the distribution to be sampled from
# iters : specifies how many iterations should be performed
#
#################################################################
class GibbsSampler(object):

	#Initialize the variables
	def __init__(self,mew,sigma,iters):
		self.mu=mew.reshape((-1,mew.shape[0]));
		self.sig=sigma;
		self.iterations=iters;


	#Gibbs Sampler
	#Sample 1 component at a time. While keeping the rest constant
	def SampledPoint(self):
		
		#initialize a point randomly
		point= np.random.rand(self.mu.shape[0],self.mu.shape[1])*np.diag(self.sig).reshape((-1,self.mu.shape[1]))+ np.array(self.mu);		
		
		for i in range(self.iterations):								#repeat over a number of iterations provided
			for j in range (self.mu.shape[1]):							#go over all the variables one at a time while keeping the rest constant

				S11=self.sig[j][j].reshape(1,1);						#S11 is just a single entry 1x1
				S22= np.delete(self.sig,j,0);							#remove jth row and column from the current matrix to get the conditioning sdevs
				S22= np.delete(S22,j,1);								#S22 is a n-1 x n-1 matrix
				S22= np.linalg.pinv(S22);								#invert it because inverted form is used in conditioning formula
				S12= np.delete(self.sig[j,:],j,0);						#all cols of jth row except jth col will be S12 (n-1 x 1) S21 is just S12.T
				S12= S12.reshape(-1,S12.shape[0]);						#all cols of jth row except jth col will be S12 (n-1 x 1) S21 is just S12.T
				#import ipdb; ipdb.set_trace();

				
				mu1=self.mu[0][j].reshape(1,1);							#mu1 is the jth mean , the (sub)variable that is being sampled
				mu2=np.delete(self.mu[0],j,0).reshape(-1,1);			#mu2 is rest of the mean vector
				x2=np.delete(point[0],j,0).reshape(-1,1);				#x2 is the sampled point without the jth component since latter has to be sampled
				#if j==0:
					#print 'Res: ',(x2-mu2).T;
				#import ipdb; ipdb.set_trace();
				
				new_mu  = mu1 + (S12.dot(S22)).dot((x2-mu2))			#define the new distribution mean
				new_sig = S11 - (S12.dot(S22)).dot(S12.T);				#define the new distribution sigma
				
				ne=np.random.normal(new_mu,np.absolute(new_sig)); 		#sample a point from this conditioned dist
				point[0,j] = ne;										#assign
				
		return point;													#return once iterations have been completed


####################################################
# CLASS: DummySampler
# Does nothing
####################################################
class DummySampler(object):
	
	def __init__(self,dims):
		self.dimensions=dims;
		
	def SampledPoint(self):
		return np.random.rand(1,self.dimensions);
