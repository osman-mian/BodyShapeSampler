from os.path import join
import cPickle as pkl
import numpy as np
from smpl_utils import load_smpl
from time import sleep

def SaveStats(indices):
	with open('./custom/pkls/vertices_per_part.pkl','wb') as file_:
		pkl.dump(indices,file_);
		
def SaveFaces(faces_dict):
	with open('./custom/pkls/common_faces.pkl','wb') as file_:
		pkl.dump(faces_dict,file_);	

def extract_neighbours():
	
	neighbourhood = {}
	
	neighbourhood['head'] = dict.fromkeys(['upperBody']);
	neighbourhood['leftHand'] = dict.fromkeys(['leftArm']);
	neighbourhood['leftArm'] = dict.fromkeys(['leftHand','upperBody']);
	neighbourhood['upperBody'] = dict.fromkeys(['leftArm']);
	
	neighbourhood['rightHand'] = dict.fromkeys(['rightArm']);
	neighbourhood['rightArm'] = dict.fromkeys(['rightHand','upperBody']);
	neighbourhood['leftFoot'] = dict.fromkeys(['leftThigh']);
	neighbourhood['leftThigh'] = dict.fromkeys(['leftFoot','lowerBody']);
	neighbourhood['rightFoot'] = dict.fromkeys(['rightThigh']);
	neighbourhood['rightThigh'] = dict.fromkeys(['rightFoot','lowerBody']);
	neighbourhood['lowerBody'] = dict.fromkeys(['upperBody','leftThigh','rightThigh']);
	neighbourhood['upperBody'] = dict.fromkeys(['lowerBody','head','leftArm','rightArm']);
	
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
	faces = smpl.f
	
	labels = pkl.load(open(join(data_path, 'condensed_partnames_per_vertex.pkl')))
	neighbourhood=extract_neighbours();
	
	indices = {};
	for parts in neighbourhood:
		
		parts_indices = np.array([index for index, value in enumerate(labels) if value == parts])
		if parts not in indices:
			indices[parts]=parts_indices;
			
		for neighbours in neighbourhood[parts]:
			print parts, ' and ' , neighbours
			neighbour_indices =np.array([index for index, value in enumerate(labels) if value == neighbours])
			if neighbours not in indices:
				indices[neighbours]=neighbour_indices;
			
			part_indices_full = np.vstack((parts_indices.reshape(-1,1),neighbour_indices.reshape(-1,1)));
			
			#extract faces containing these vertices
			mask = np.in1d(faces, part_indices_full)
			mask = (mask.reshape(faces.shape[0],3))
			mask = (mask.all(axis=1))
			mask_real = (np.argwhere(mask == True))
			face_vertices = (np.squeeze(faces[mask_real,:]))
			
			uncommon_faces=[];
			for k in range(face_vertices.shape[0]):
				z = face_vertices[k]
				if (np.all(np.in1d(z,parts_indices))) or (np.all(np.in1d(z, neighbour_indices))):
						uncommon_faces.append(k);
			
			#keep faces involving only the common parts			
			face_vertices = np.delete(face_vertices, uncommon_faces, axis=0)
			list_shared = np.unique(face_vertices);
			
			#append bordering vertices to parts_vertices
			indices[parts]=np.unique(np.vstack((indices[parts].reshape(-1,1),list_shared.reshape(-1,1))));
			indices[neighbours]=np.unique(np.vstack((indices[neighbours].reshape(-1,1),list_shared.reshape(-1,1))));
			
	for parts in neighbourhood:
		indices[parts]=np.unique(indices[parts]);
	
	SaveStats(indices);
	
main()
