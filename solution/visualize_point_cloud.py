def visualize_point_cloud(X, faces=None, mv=None, mlab_obj=None):
    """
    Visualize two point clouds
        visualize_point_cloud(X)

    Inputs:
    ------------
    X    
        matrix of point clouds of dimensions Nx3

    faces 
        if different than None is a 3xN matrix indicating which verts are connected
    mv
        MeshViewer

    Outputs
    ------------
    
    Mesh visualization
    """
    use_meshviewer = False
    if use_meshviewer:
        from body.mesh import Mesh
        import types
        mesh1 = Mesh(v= X,f=faces)
        mesh2 = Mesh(v= Y,f=faces)
        mesh2.set_vertex_colors('SeaGreen')
        if isinstance(mv,types.ListType):
            mv[0][0].set_dynamic_meshes([mesh1,mesh2])
            mv[0][1].set_dynamic_meshes([mesh1])
        else: 
            mv.set_dynamic_meshes([mesh1,mesh2])
    else:
		#!/usr/local/bin/ipython --gui=wx
        from mayavi.mlab import triangular_mesh, figure,clf
        import numpy as np
        from os.path import join
        fig = mv
        verts1 = X.T
        if mlab_obj is None: 
            clf(fig)
            mlab_obj = triangular_mesh(verts1[0], verts1[1], verts1[2], faces, color=(.7, .7, .9), figure=fig)
            fig.scene.reset_zoom()
        else:
            mlab_obj.mlab_source.set(x=verts1[0], y=verts1[1], z=verts1[2])
        return mlab_obj
		
  


 
