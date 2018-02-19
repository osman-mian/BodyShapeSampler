import cPickle as pkl
import numpy as np

from solution.visualize_point_cloud import visualize_point_cloud
from smpl_utils import load_smpl
from time import sleep
from os.path import join


#Our Headers
from custom.Accumulator import DistributionAccumulator;
from custom.PCA_Parts import PCA_Parts;
from custom.condense import SaveStats,SaveStats_coord

####################################################
#
# Function: Main
# Generates body parts from SMPL and does PCA on them
# Parameters tuned to accomodate time of learning and 
# goodness of results.
#
####################################################
def main():

	MAYAVI = True
	gender = 'male'
	data_path = './data/'
    
	if not MAYAVI:
		from body.mesh.meshviewer import MeshViewers
		mv = MeshViewers(shape=[1,2])
	else:
		from mayavi.mlab import triangular_mesh, figure
		mv = figure(size=(800,800))
    
	smpl = load_smpl(gender=gender)
	tm = visualize_point_cloud(smpl.r, smpl.f, mv=mv)
	
	#Load from the "condensed parts" and not the actual SMPL parts
	labels = pkl.load(open(join(data_path, 'condensed_partnames_per_vertex.pkl')))
	indices = pkl.load(open('./custom/pkls/vertices_per_part.pkl'))

	unique_labels = list(set(labels))
	print("Set the view angle as desired in gui")
	import ipdb; ipdb.set_trace();

	parts={};
	creatorFlag= True		
	if(creatorFlag==True):												#Creates distributions over local body parts
		creator(smpl,labels,indices,unique_labels,gender); 				
	else:																#Sample each part independentl and display
		loaded = pkl.load(open(join('./custom/pkls/',gender+'_part_priors.pkl')))
		samples=10;
		for i in xrange(samples):
			verts = np.copy(smpl.r)
			faces = smpl.f
			for lab in unique_labels:
				#Preparator code
				part_indices = indices[lab]			
				mask = np.in1d(faces, part_indices)
				mask = (mask.reshape(faces.shape[0],3))
				mask = (mask.all(axis=1))
				mask_real = (np.argwhere(mask == True))
				face_vertices = (np.squeeze(faces[mask_real,:]))
				print 'Sampling init done'
				
				print 'Sampling: ',lab
				parts[lab]=loaded[lab].sample();						#Sample the body part
				verts[part_indices]=parts[lab];							#Assign to the vertices
			
			#Optional: See how well the parts are on the boders. (Ideally=0.0)
			#print getScore(parts['leftArm'],parts['leftHand'],indices['leftArm'],indices['leftHand']);
			
			print 'Mesh Generated'
			visualize_point_cloud(verts, faces, mv=mv)
			import ipdb;ipdb.set_trace();	
		
	return;

def getScore(verts1,verts2,ind1,ind2):
	common_verts = np.intersect1d(ind1,ind2);										#find common indexes
	i1 = [];
	i2 = [];
	
	for common in common_verts:														#for each common index
		i1.append([index for index,value in enumerate(ind1) if value == common][0]) #find the corresponding index of that index in indices
		i2.append([index for index,value in enumerate(ind2) if value == common][0])
		
	
	return np.linalg.norm(verts1[i1]-verts2[i2]);									 #subtract values at corresponding indexes, find the norm


def creator(smpl,labels,indices,unique_labels,gender,mv=None):
	
	zz =3
	jumps=1;
	
	first_frame=False
	
	accumulators={};																#dictionary to store prior distributions
	PCA_coord_matrix = {};															#dictionary to store the synthetic points for each part after the PCA
	
	for lab in unique_labels:
		data_mat=np.array([]);
		part_indices = indices[lab];  
		
		#Experiment restricted to first 5 betas of the SMPL model only
		betas1 = np.arange(-zz, zz, jumps)
		betas2 = np.arange(-zz, zz, jumps)
		betas3 = np.arange(-zz, zz, jumps)
		betas4 = np.arange(-zz, zz, jumps)
		betas0 = np.arange(-2,2,1);
		
		print betas0.size * betas1.size * betas2.size *betas3.size * betas4.size, " combinations"
		
		verts = smpl.r
		faces = smpl.f
		
		#extract the faces that show the currenty body part
		mask = np.in1d(faces, part_indices)
		mask = (mask.reshape(faces.shape[0],3))
		mask = (mask.all(axis=1))
		mask_real = (np.argwhere(mask == True))
		face_vertices = (np.squeeze(faces[mask_real,:]))


		#Stack all instances togehter to form a matrix
		for beta0 in betas0:
			smpl.betas[0]=beta0;
			for beta4 in betas4:
				smpl.betas[4]=beta4;
				for beta1 in betas1:
					smpl.betas[1]=beta1;
					for beta2 in betas2:
						smpl.betas[2]=beta2;
						for beta3 in betas3:
							smpl.betas[3]=beta3;
							verts = smpl.r
							faces = smpl.f
							if len(data_mat)==0:
								data_mat = np.reshape( verts[part_indices], (1,-1));
							else:
								data_mat = np.vstack( (data_mat,np.reshape( verts[part_indices], (1,-1))));

						

		[pca,t_points,means] = PCA_Parts(data_mat); 								#Do a PCA on this part
		
		local_mean = np.mean(t_points,axis=0);
		local_var = np.var(t_points,axis=0);
		PCA_coord_matrix[lab] = np.vstack((t_points,local_mean))
		PCA_coord_matrix[lab] = np.vstack((PCA_coord_matrix[lab],local_var))
		
		accumulators[lab]=DistributionAccumulator(pca,local_mean,local_var,means);
		print 'Saved: ',lab
		
	
	print 'Saving Distributions...'
	SaveStats(accumulators,gender);
	SaveStats_coord(PCA_coord_matrix,gender);

	print 'Done'


main()
