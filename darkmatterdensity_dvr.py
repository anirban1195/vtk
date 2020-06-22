#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 08:55:23 2020

@author: anirban
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:37:12 2020

@author: anirban
"""


import h5py
import sys
import vtk
import numpy as np
from vtk.util.misc import vtkGetDataRoot

def Main():
    global ren
    filename = str(sys.argv[1])
    with h5py.File(filename, 'r') as f:
        # List all groups
        idx = list(f.keys())[3]
        
        # Get the data
        data = list(f[idx])
    
    #Take log of data to reduce rande   
    data=np.array(data) +1
    data = np.log10(data)*1
    #Convert the data to vtk image
    dataImporter = vtk.vtkImageImport()
    data_string = data.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    print (np.max(data), np.min(data))
    dataImporter.SetDataScalarTypeToFloat()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, 319, 0, 319, 0, 319)
    dataImporter.SetWholeExtent(0, 319, 0, 319, 0, 319)

    
    # Create transfer mapping scalar value to opacity
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(0, 0.0)
    
    opacityTransferFunction.AddPoint(1, 0.0)
    opacityTransferFunction.AddPoint(1.01, 0.2)
    opacityTransferFunction.AddPoint(1.15, 0.2)
    opacityTransferFunction.AddPoint(1.16 ,0.0)
    
    opacityTransferFunction.AddPoint(1.70, 0.0)
    opacityTransferFunction.AddPoint(1.71, 0.2)
    opacityTransferFunction.AddPoint(1.85, 0.2)
    opacityTransferFunction.AddPoint(1.86 ,0.0)
    
    opacityTransferFunction.AddPoint(2, 0.0)
    opacityTransferFunction.AddPoint(2.01, 0.2)
    opacityTransferFunction.AddPoint(2.15, 0.2)
    opacityTransferFunction.AddPoint(2.16 ,0.0)
    
    opacityTransferFunction.AddPoint(2.71, 0.0)
    opacityTransferFunction.AddPoint(2.71, 0.2)
    opacityTransferFunction.AddPoint(2.85, 0.2)
    opacityTransferFunction.AddPoint(2.86 ,0.0)
    
    opacityTransferFunction.AddPoint(3, 0.0)
    opacityTransferFunction.AddPoint(3.01, 0.2)
    opacityTransferFunction.AddPoint(3.85, 0.2)
    opacityTransferFunction.AddPoint(3.86 ,0.0)
    
    opacityTransferFunction.AddPoint(4, 0.0)
    opacityTransferFunction.AddPoint(4.01, 0.2)
    opacityTransferFunction.AddPoint(4.85, 0.2)
    opacityTransferFunction.AddPoint(4.86 ,0.0)
    
    
    #Create color tranfer function
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(0,0,0,1)
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

    # Create the standard renderer, render window and interactor
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    
    ren.AddVolume(volume)
    ren.SetBackground(0, 0, 0)
    renWin.SetSize(1600, 900)
    
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

if __name__=="__main__":
    Main()