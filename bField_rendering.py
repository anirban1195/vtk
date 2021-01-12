#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 18:16:22 2021

@author: anirban
"""

import h5py 
import sys
import vtk 
import numpy as np 
from vtk.util.misc import vtkGetDataRoot 
filename = 'magField_vectors.vtk'
reader = vtk.vtkStructuredGridReader()
reader.SetFileName(filename)
        
rakes = [ 
             vtk.vtkLineSource(), 
             vtk.vtkLineSource(), 
             vtk.vtkLineSource() 

             ] 

rakes[0].SetPoint1(160, 100, 160) 
rakes[0].SetPoint2(160, 200, 160) 
rakes[0].SetResolution(50)   

rakes[1].SetPoint1(100, 160, 160) 
rakes[1].SetPoint2(200, 160, 160) 
rakes[1].SetResolution(50)      

rakes[2].SetPoint1(160, 160, 100) 
rakes[2].SetPoint2(160, 160, 200) 
rakes[2].SetResolution(50) 

streamLineArr=[] 

for i in range(0, len(rakes)): 
	streamLine = vtk.vtkStreamTracer() 
	streamLine.SetInputConnection(reader.GetOutputPort()) 
	streamLine.SetSourceConnection(rakes[i].GetOutputPort()) 
	streamLine.SetMaximumPropagation(3000) 
	streamLine.SetIntegrationDirectionToForward() 
	streamLine.SetIntegratorTypeToRungeKutta4() 
	streamLineArr.append(streamLine) 
    
# Create the standard renderer, render window and interactor 
ren = vtk.vtkRenderer() 
renWin = vtk.vtkRenderWindow() 
renWin.AddRenderer(ren) 
iren = vtk.vtkRenderWindowInteractor() 
iren.SetRenderWindow(renWin) 
n=len(rakes) 
stream_actorArr=[] 

for j in range(n): 
	streamLineMapper = vtk.vtkPolyDataMapper() 
	#streamLineMapper.SetLookupTable(lut) 
	streamLineMapper.SetInputConnection(streamLineArr[j].GetOutputPort()) 
	streamLineMapper.SetScalarModeToUsePointFieldData() 
	streamLineMapper.ScalarVisibilityOn() 
	#streamLineMapper.SelectColorArray(0) #Use this line if you want your streamlines to be colored  
	streamLineActor = vtk.vtkActor() 
	streamLineActor.SetMapper(streamLineMapper) 
	streamLineActor.VisibilityOn() 
	stream_actorArr.append(streamLineActor) 
	ren.AddActor(streamLineActor) 


filename = 'snap_s138.hdf'

with h5py.File(filename, 'r') as f: 

	# Select Total Matter Density
	idx = list(f.keys())[4] 
	# Get the data 
	data = list(f[idx]) 

         

data=np.array(data) +1 
data = np.log10(data)*1 
dataImporter = vtk.vtkImageImport() 
data_string = data.tostring() 
dataImporter.CopyImportVoidPointer(data_string, len(data_string)) 
print (len(data_string)) 

dataImporter.SetDataScalarTypeToFloat() 
dataImporter.SetNumberOfScalarComponents(1) 
dataImporter.SetDataExtent(0, 319, 0, 319, 0, 319) 
dataImporter.SetWholeExtent(0, 319, 0, 319, 0, 319) 

# Create transfer mapping scalar value to opacity 

opacityTransferFunction = vtk.vtkPiecewiseFunction() 
opacityTransferFunction.AddPoint(0, 0.0) 

opacityTransferFunction.AddPoint(0.15, 0.0) 
opacityTransferFunction.AddPoint(0.16, 0.1) 
opacityTransferFunction.AddPoint(0.25, 0.1) 
opacityTransferFunction.AddPoint(0.36 ,0.0) 


opacityTransferFunction.AddPoint(1, 0.0) 
opacityTransferFunction.AddPoint(1.01, 0.2) 
opacityTransferFunction.AddPoint(1.15, 0.2) 
opacityTransferFunction.AddPoint(1.16 ,0.0) 


opacityTransferFunction.AddPoint(1, 0.0) 
opacityTransferFunction.AddPoint(1.71, 0.2) 
opacityTransferFunction.AddPoint(1.85, 0.2) 
opacityTransferFunction.AddPoint(1.86 ,0.0) 

opacityTransferFunction.AddPoint(2, 0.0) 
opacityTransferFunction.AddPoint(2.01, 0.2) 
opacityTransferFunction.AddPoint(2.15, 0.2) 
opacityTransferFunction.AddPoint(2.16 ,0.0) 


opacityTransferFunction.AddPoint(2, 0.0) 
opacityTransferFunction.AddPoint(2.71, 0.2) 
opacityTransferFunction.AddPoint(2.85, 0.2) 
opacityTransferFunction.AddPoint(2.86 ,0.0) 


opacityTransferFunction.AddPoint(3, 0.0) 
opacityTransferFunction.AddPoint(3.01, 0.2) 
opacityTransferFunction.AddPoint(3.15, 0.2) 
opacityTransferFunction.AddPoint(3.16 ,0.0) 


opacityTransferFunction.AddPoint(4, 0.0) 
opacityTransferFunction.AddPoint(4.01, 0.2) 
opacityTransferFunction.AddPoint(4.15, 0.2) 
opacityTransferFunction.AddPoint(4.16 ,0.0) 


#opacityTransferFunction.AddPoint(1.26 ,0.0) 



colorTransferFunction = vtk.vtkColorTransferFunction() 
colorTransferFunction.AddRGBPoint(0,0.2,0.5,0.8) 
colorTransferFunction.AddRGBPoint(2,1,1,0) 
colorTransferFunction.AddRGBPoint(4,1,0,0) 

# The property describes how the data will look 
volumeProperty = vtk.vtkVolumeProperty() 
volumeProperty.SetColor(colorTransferFunction) 
volumeProperty.SetScalarOpacity(opacityTransferFunction) 
volumeProperty.SetScalarOpacityUnitDistance(10) 
volumeProperty.ShadeOn() 
volumeProperty.SetInterpolationTypeToLinear() 

# The mapper / ray cast function know how to render the data 
volumeMapper = vtk.vtkSmartVolumeMapper() 
volumeMapper.SetBlendModeToComposite() 
volumeMapper.SetInputConnection(dataImporter.GetOutputPort()) 


# The volume holds the mapper and the property and 
# can be used to position/orient the volume 
volume = vtk.vtkVolume() 
volume.SetMapper(volumeMapper) 
volume.SetProperty(volumeProperty) 

ren.AddVolume(volume)
ren.SetBackground(0, 0, 0)
# create the scalar_bar
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetOrientationToHorizontal()
scalar_bar.SetLookupTable(colorTransferFunction)
scalar_bar.SetMaximumWidthInPixels(100)
 # create the scalar_bar_widget
scalar_bar_widget = vtk.vtkScalarBarWidget()
scalar_bar_widget.SetInteractor(iren)
scalar_bar_widget.SetScalarBarActor(scalar_bar)
scalar_bar_widget.On()


iren.Initialize() 
renWin.Render() 
iren.Start() 