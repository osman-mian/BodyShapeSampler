import numpy as np;
from sklearn.decomposition import PCA


####################################################
# Function: PCA_Parts
# Computes the PCA over the given data.
#
####################################################
def PCA_Parts(data_mat):
	print 'Data: ',data_mat.shape
	comps = 0.98											#choose the required variance% of data to decide PCA components 
	means = np.mean(data_mat,axis=0) 						#store menn of each column here
	mean_pts = np.copy(data_mat); 							#store mean subtracted points here
	
	
	for mm in range(data_mat.shape[1]):		      			#iterate over columns
		mean_pts [:,mm] = data_mat[:,mm] - means[mm]; 		#subtract mean from each point

	
	pca = PCA(n_components=comps, svd_solver='auto');     	#init PCA
	pca.fit(mean_pts); 				      					#find a fit
	t_points=pca.transform(mean_pts);		      			#generate alphas (synthetic points)
	print 'Synthetic: ',t_points.shape;	
	return [pca,t_points,means];
	



''' This area for testing only 
		
print "Data shape: ",data_mat.shape;
print "Means shape: ",means.shape;
print "MeanPts shape: ",mean_pts.shape;
print "Components Shape: ",pca.components_.shape;
print "Transformed Shape: ",t_points.shape;


print "Components Shape: ",pca.components_.shape;
print pca.components_;
print t_points;
import ipdb; ipdb.set_trace();
#'''		
