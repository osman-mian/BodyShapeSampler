from os.path import join
import cPickle as pkl
import numpy as np
from solution.visualize_point_cloud import visualize_point_cloud
from smpl_utils import load_smpl
from math import pi
import chumpy as ch
from time import sleep
from custom.Accumulator import PairwiseAccumulator;
from custom.scorer import AreaScore,PerimeterScore;


def SaveStats(neighbourhood,gender):
	with open(join('./custom/pkls/',gender+'_part_pairwise.pkl'),'wb') as file_:
		pkl.dump(neighbourhood,file_);
		
def SaveFaces(faces_dict):
	with open('./custom/pkls/common_faces.pkl','wb') as file_:
		pkl.dump(faces_dict,file_);	


def extract_neighbours():
	
	neighbourhood = {}
	
	#neighbourhood['head'] = dict.fromkeys(['upperBody']);
	neighbourhood['leftHand'] = dict.fromkeys(['leftArm']);
	neighbourhood['leftArm'] = dict.fromkeys(['leftHand','upperBody']);
	neighbourhood['upperBody'] = dict.fromkeys(['leftArm']);
	
	#neighbourhood['rightHand'] = dict.fromkeys(['rightArm']);
	#neighbourhood['rightArm'] = dict.fromkeys(['rightHand','upperBody']);
	#neighbourhood['leftFoot'] = dict.fromkeys(['leftThigh']);
	#neighbourhood['leftThigh'] = dict.fromkeys(['leftFoot','lowerBody']);
	#neighbourhood['rightFoot'] = dict.fromkeys(['rightThigh']);
	#neighbourhood['rightThigh'] = dict.fromkeys(['rightFoot','lowerBody']);
	#neighbourhood['lowerBody'] = dict.fromkeys(['upperBody','leftThigh','rightThigh']);
	#neighbourhood['upperBody'] = dict.fromkeys(['lowerBody','head','leftArm','rightArm']);
	
	for parts in neighbourhood:
		for neighbours in neighbourhood[parts]:
			neighbourhood[parts][neighbours]=PairwiseAccumulator();
			
	return neighbourhood;


def main():
	MAYAVI = True
	gender = 'female'
	data_path = './data/'
    
	if not MAYAVI:
		from body.mesh.meshviewer import MeshViewers
		mv = MeshViewers(shape=[1,2])
	else:
		from mayavi.mlab import triangular_mesh, figure
		#mv = figure(size=(800,800))
    
    # smpl
	smpl = load_smpl(gender=gender)


	labels = pkl.load(open(join(data_path, 'condensed_partnames_per_vertex.pkl')))
	unique_labels = list(set(labels));

	neighbourhood=extract_neighbours();
	
	shared_faces={};
	for parts in neighbourhood:
		shared_faces[parts]={};
		for neighbours in neighbourhood[parts]:
			shared_faces[parts][neighbours]=[];
			
	zz =3
	betas1 = np.arange(-zz, zz, 1)
	betas2 = np.arange(-zz, zz, 1)
	betas3 = np.arange(-zz, zz, 1)
	
	verts = smpl.r
	faces = smpl.f
	
	first_frame = True
	for beta1 in betas1:
		smpl.betas[1]=beta1;
		for beta2 in betas2:
			smpl.betas[2]=beta2;
			for beta3 in betas3:
				smpl.betas[3]=beta3;
				if first_frame: 
					#tm = visualize_point_cloud(smpl.r, smpl.f, mv=mv)
					# Set the view angle as desired
					#print("Set the view angle as desired in gui")
					#import ipdb; ipdb.set_trace();
					first_frame = False
				else: 
					
					for parts in neighbourhood:
						for neighbours in neighbourhood[parts]:
							#print parts , ' and ' , neighbours;
							#extract vertices of each part
							parts_indices = [index for index, value in enumerate(labels) if value == parts]
							neighbour_indices =[index for index, value in enumerate(labels) if value == neighbours]
							part_indices_full = (parts_indices)+(neighbour_indices);
							
							#extract faces containing these vertices
							mask = np.in1d(faces, part_indices_full)
							mask = (mask.reshape(faces.shape[0],3))
							mask = (mask.all(axis=1))
							mask_real = (np.argwhere(mask == True))
							face_vertices = (np.squeeze(faces[mask_real,:]))
							
							#remove faces that involve vertices of only 1 part
							uncommon_faces=[];
							for k in range(face_vertices.shape[0]):
								z = face_vertices[k]
								if (np.all(np.in1d(z,parts_indices))) or (np.all(np.in1d(z, neighbour_indices))):
										uncommon_faces.append(k);
							
							#keep faces involving only the common parts			
							face_vertices = np.delete(face_vertices, uncommon_faces, axis=0)
							shared_faces[parts][neighbours]=face_vertices
							#calculate the heuristic on these vertices (Average Area/Average Perimeter for now)
							heuristic = get_score(verts,face_vertices);
							neighbourhood[parts][neighbours].addValue(heuristic);

					#print smpl.betas;

	for parts in neighbourhood:
		for neighbours in neighbourhood[parts]:
			neighbourhood[parts][neighbours].calculateDistribution();
	
	SaveStats(neighbourhood,gender);
	SaveFaces(shared_faces);
	print 'Fertig!'
					
def get_score(verts,face_vertices):
	
	score = 0;
	limit = face_vertices.shape[0];
	
	judge = PerimeterScore();
	#judge = AreaScore();
	
	for faces_id in range(limit):
		faces=face_vertices[faces_id];
		score = score + judge.getScore(verts[faces[0]],verts[faces[1]],verts[faces[2]]);
	
	score = score / limit;
	
	return score;
	
main()
