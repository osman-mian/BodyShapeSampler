import numpy as np;


###############################################################################
# CLASS: DistributionManager
# 
# Generates a (partial) conditional distribution 
# over multivariate data using the formula of conditioning
# over a gaussian.
#
# Algorithm: http://fourier.eng.hmc.edu/e161/lectures/gaussianprocess/node7.html
#
###############################################################################
class DistributionManager(object):
	
	def __init__(self):
		gg=1;
		
	def GetDistribution(self,data_part1,data_part2):

		#import ipdb; ipdb.set_trace();
		mu1 = data_part1[-2]					#For compactness we stored mew as 2nd last value of our data
		mu2 = data_part2[-2]
		sigma1 = data_part1[-1]					#For compactness we stored sigma as the last value of our data
		sigma2 = data_part2[-1]
		
		self.vals1=mu1.shape[0];				#number of components for current
		self.vals2=mu2.shape[0];				#number of components for condtioning
		
		#import ipdb; ipdb.set_trace();
		self.S11 = np.diag(sigma1);		
		self.S22 = np.diag(sigma2);
		self.S22 = np.linalg.inv(self.S22);
		self.S12 = np.empty((self.vals1,self.vals2))*0;

		self.mew1= mu1;
		self.mew2= mu2;							#initialize empty mews

		p1 = data_part1[0:-2,:]
		p2 = data_part2[0:-2,:]
		

		for i in range(self.vals1):
			for j in range(self.vals2):
				self.S12[i,j]= np.mean( (p1[:,i]-self.mew1[i]) * (p2[:,j]-self.mew2[j]) );
		
		self.S21 = self.S12.T;
		#import ipdb; ipdb.set_trace();
		
		#Sigma can be determined directly using the data.
		#Only a part of mew can be computed since the final mew depends on the observed value of variable
		self.final_sigma =	self.S11  - ((self.S12).dot(self.S22)).dot(self.S21)
		self.pre_mu 	 =  (self.S12.dot(self.S22));

		#return the sigma_finalized, plus the remaining 3 components that will calculate the final mew after a variable is observed
		return [self.final_sigma,self.pre_mu,self.mew1,self.mew2]
	
	
	
	def Covariance(self,x,y,ux,uy):
		x_ = x - ux;
		y_ = y - uy;
		return np.mean(x_*y_);
		
		
