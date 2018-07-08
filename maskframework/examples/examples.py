import numpy as np

import sys

from maskframework.gdsCAD_local import *
import math as math
import matplotlib.pyplot as plt

import os
import numpy as np

import gdspy as gdy

from maskframework import *
import os

if __name__ == '__main__':

	Wafer_4_inch = Wafer(2,shape='rectangle')
	Wafer_4_inch.setGrid(6955,5955)
	Wafer_4_inch.addGridAlignementMarks()

	description_only = False

	

	spacings = [50,75,100]
	radius = [2.5,5,7.5,10,15,20]

	# dots with different diameters and spacing for two inch wafer
	
	for j in spacings:
		counter = 0 
		for i in radius:
			pm1 = PhasemaskSize(description_only)
			# pm1.addAlignementMarks('cross')
			pm1.addPattern(shape='dots',radius = 2*i,x_spacing=j,y_spacing=j)
			Wafer_4_inch.placeDesign(pm1)
			counter += 1
		
		while counter < 7:
			pm1 = PhasemaskSize(description_only)
			Wafer_4_inch.placeDesign(pm1)
			counter += 1

	# squares with different diameters and spacing for two inch wafer


	for j in spacings:
		counter = 0 
		for i in radius:
			counter += 1
			pm1 = PhasemaskSize(description_only)
			# pm1.addAlignementMarks('cross')
			pm1.addPattern(shape='rectangles',x_size = 2*i,y_size=2*i,x_spacing=j,y_spacing=j)
			Wafer_4_inch.placeDesign(pm1)

		while counter < 7:
			pm1 = PhasemaskSize(description_only)
			Wafer_4_inch.placeDesign(pm1)
			counter += 1


	layout = core.Layout('LIBRARY',unit=1e-06, precision=1e-09)
	cell = core.Cell('TOP')
	cell.add(Wafer_4_inch)
	layout.add(cell)
	layout.save(os.path.dirname(__file__) + '/20170515_Reference_Inverse_molos.gds')
	OpenInKlayout(os.path.dirname(__file__) + '/20170515_Reference_Inverse_molos.gds')



		
	# # 
	# pm1.addAlignementMarks('vernier')
	
	# pm1.addPattern(shape='dots',radius = 5,x_spacing=50,x_size=5,y_size=10,y_spacing=20)

	# # Mask for individual mologram addressing

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([i],0,0,size=300)
	# 	pm1.addDescription('L1M' + str(i+1))
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles(0,[i],0,size=300)
	# 	pm1.addDescription('L3M' + str(i+1),)
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([i],[i],[i],size=300)
	# 	pm1.addDescription('M' + str(i+1))
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([i],0,0,size=300)
	# 	pm1.addDescription('L1M' + str(i+1))
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles(0,[i],0,size=300)
	# 	pm1.addDescription('L3M' + str(i+1),)
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([i],[i],[i],size=300)
	# 	pm1.addDescription('M' + str(i+1))
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([i],0,0,size=300)
	# 	pm1.addDescription('L1M' + str(i+1))
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles(0,[i],0,size=300)
	# 	pm1.addDescription('L3M' + str(i+1),)
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in xrange(10):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([i],[i],[i],size=300)
	# 	pm1.addDescription('M' + str(i+1))
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in range(0,6):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('vernier')
	# 	pm1.addDescription('Vernier')
	# 	Wafer_4_inch.placeDesign(pm1)

	# # Mask for the inverse molograms
	# for i in range(0,9):
	# 	Wafer_4_inch.placeDesign(generateInverseMask(description_only))

	# # reference on top of measurement molograms, for last row.
	# for i in range(0,9):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles(0,[0,1,2,3,4,5,6,7,8,9],0,size=300)
	# 	pm1.addDescription('Ref Molo Top')
	# 	Wafer_4_inch.placeDesign(pm1)

	# # Allows to adress the first line of molograms.
	# for i in range(0,9):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([0,1,2,3,4,5,6,7,8,9],0,0,size=300)
	# 	pm1.addDescription('Ref Second Line')
	# 	Wafer_4_inch.placeDesign(pm1)

	# # Allows to adress the last line of molograms.
	# for i in range(0,9):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles(0,0,[0,1,2,3,4,5,6,7,8,9],size=300)
	# 	pm1.addDescription('Ref Second Line')
	# 	Wafer_4_inch.placeDesign(pm1)

	# # reference besides actual measurement molograms
	# for i in range(0,9):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([0,2,4,6,8],[0,2,4,6,8],[0,2,4,6,8],size=300)
	# 	pm1.addDescription('Ref Molo side 0 2 4 6 8')
	# 	Wafer_4_inch.placeDesign(pm1)

	# for i in range(0,9):
	# 	pm1 = PhasemaskSize(description_only,width=6955,height=5955)
	# 	pm1.addAlignementMarks('cross')
	# 	pm1.addMolocircles([1,3,5,7,9],[1,3,5,7,9],[1,3,5,7,9],size=300)
	# 	pm1.addDescription('Ref Molo side 1 3 5 6 8')
	# 	Wafer_4_inch.placeDesign(pm1)

	


