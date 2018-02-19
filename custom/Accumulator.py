import numpy as np;
from sklearn.decomposition import PCA;

####################################################
# CLASS: DistributionAccumulator
# Stores the PCA related details for each body part
#
# PCA: The PCA object that contains transform details
# dist_mean: Mean of each pca component
# dist_var : Variance of each pca_component
# mean_pos : mean position in global coordinate
#			 needed while back transforming the part
#
#
####################################################
class DistributionAccumulator(object):
	
	#Initialize the variables
	def __init__(self,pca_,d_mean,d_var,mean_):
		self.pca=pca_;
		self.dist_mean=d_mean;
		self.dist_var=d_var;
		self.mean_pos=mean_;

	#Sample a global point directly from the distribution
	def sample_global(self):
		t_points = np.random.normal(self.dist_mean,self.dist_var);
		data_points = self.pca.inverse_transform(t_points) + self.mean_pos;
		rows = len(data_points)/3;
		return np.reshape(data_points,(rows,3));
		
	#Sample a point from this distribution in the PCA domain
	def sample_raw(self):
		t_points = np.random.normal(self.dist_mean,self.dist_var);
		return t_points;
	
	#Given a synthetic point, return its global coordinate equivalent
	def get_global(self,t_points):
		t_points = np.array(t_points).reshape(-1),
		data_points = self.pca.inverse_transform(t_points) + self.mean_pos;
		rows = data_points.size/3;
		return np.reshape(data_points,(rows,3));
		

