#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 12:33:48 2020

@author: anirban
"""
import h5py 
import numpy as np 
from numpy import mgrid, empty 
from tvtk.api import tvtk,write_data 
import sys 
with h5py.File('snap_s138.hdf', 'r') as f: 
    # List all groups
    print("Keys: %s" % f.keys())
    Bx = list(f.keys())[0]
    By = list(f.keys())[1]
    Bz = list(f.keys())[2]

    # Get the data
    datax = np.array(f[Bx])
    datay = np.array(f[By])
    dataz = np.array(f[Bz])

    
# Generate some points. 
x, y, z = mgrid[0:320,0:320, 0:320] 
# The actual points. 

pts = empty(z.shape + (3,), dtype=np.int16) 
pts[..., 0] = x 
pts[..., 1] = y 
pts[..., 2] = z 

# Some vectors 
vectors = empty(z.shape + (3,), dtype=np.float32) 
vectors[..., 0] = datax 
vectors[..., 1] = datay 
vectors[..., 2] = dataz 
#Transposing because the order is z,y and x 
pts = pts.transpose(2, 1, 0, 3).copy() 
pts.shape = int(pts.size / 3), 3 #Flattening   

vectors = vectors.transpose(2, 1, 0, 3).copy() 
vectors.shape = int(vectors.size / 3), 3 #Flattening 

sg = tvtk.StructuredGrid(dimensions=x.shape, points=pts) 
sg.point_data.vectors = vectors 
sg.point_data.vectors.name = 'vector_field' 
write_data(sg, 'magField_vectors.vtk') 