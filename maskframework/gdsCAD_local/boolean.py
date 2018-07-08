import numpy as np
from gdsCAD_local import *
import math as math
import matplotlib.pyplot as plt

import os
import numpy as np
from gdsCAD_local import *
import gdspy as gdy


		

class Wafer(core.Elements):
	"""This class generates a wafer witch diameter size, the center of the wafer is at the origin of the coordinate system at (0,0)

	:param size: Wafer size in inches
	"""
	def __init__(self,size = 4):
		super(Wafer, self).__init__()

		self.size = 4
		inch = 25400
		self.radius = self.size*inch/2.
		self.line_thickness = 500

		self.usableArea = 0.9*np.sqrt(2)*self.radius
		wafer = Rectangle(self.usableArea,self.usableArea,0)
		self.add(wafer)
		
		wafer = shapes.Circle((0.,0.), self.radius,0)
		self.add(wafer)
		wafer = Rectangle(self.radius*2,self.radius*2,0)
		self.add(wafer)
		self.x_index = 0
		self.y_index = 0 

	def setGrid(self,x_spacing,y_spacing):
		"""sets the gridsize on the wafer's usable area."""

		self.x_spacing = x_spacing
		self.y_spacing = y_spacing
		self.x_max_index = self.usableArea/x_spacing
		self.y_max_index = self.usableArea/y_spacing


	def placeDesign(self,design):
		"""places a design at the next free location on the wafer grid, starting at the top left corner and filling it row wise"""
		
		d = (self.x_spacing*(self.x_index-self.x_max_index/2+1/2.),-self.y_spacing*(self.y_index-self.y_max_index/2+1/2.))

		if self.x_index == int(self.x_max_index)-1:
			self.y_index += 1
			self.x_index = 0
		else:
			self.x_index += 1 

		self.add(utils.translate(design,d))

def Rectangle(w,h,d = 0):
	"""returns a rectangle object with height h, width w and line thickness d"""
	b = (h-d)/2.0
	a = (w-d)/2.0

	box_inner_boundary = [[-a,-b],[-a,b],[a,b],[a,-b],[-a,-b]]

	b = (h)/2.0
	a = (w)/2.0
	# Counterclockwise order
	box_boundary_outer_boundary = [[-a,-b],[a,-b],[a,b],[-a,b],[-a,-b]]
	# Clockwise point order (It is very important, that these two are distinct)
	points =  box_boundary_outer_boundary + box_inner_boundary
	rectangle = core.Boundary(points)

	return rectangle

class AlignementMark(core.Elements):
	"""creates an cross-shaped alignement mark, a is the side length of the alignement mark, t the thichness of the bar relative to the mark size"""

	def __init__(self,a=200,t=20,center=(0,0),shape='cross'):
		super(AlignementMark, self).__init__()


		if shape =='cross':

			boundary = [[t/2.,t/2.],[a/2.,t/2.],[a/2.,-t/2],[t/2.,-t/2.],[t/2.,-a/2.],[-t/2.,-a/2],[-t/2.,-t/2.],
			[-a/2.,-t/2.],[-a/2.,t/2],[-t/2.,t/2.],[-t/2.,a/2.],[t/2.,a/2],[t/2.,t/2.]]
			
			cross = core.Boundary(boundary)

			self.add(cross)

		if shape =='vernier':
			w = a/2.-(t+5)
			h = a/2.-(t+5)
			rect = shapes.Rectangle((-w/2.,-h/2),(w/2.,h/2))

			d = (a/4.,a/4.)
			self.add(utils.translate(rect,d))
			d = (-a/4.,a/4.)
			self.add(utils.translate(rect,d))
			d = (a/4.,-a/4.)
			self.add(utils.translate(rect,d))
			d = (-a/4.,-a/4.)
			self.add(utils.translate(rect,d))

class Pattern(object):
	"""Fills a phase mask object with a pattern"""
	def __init__(self, arg):
		super(Pattern, self).__init__()
		self.arg = arg
		

class PhasemaskSize(core.Elements):
	"""creates a blueprint of the size of a phase mask"""
	def __init__(self):
		super(PhasemaskSize, self).__init__()
		
		self.width = 7000
		self.height = 6000

		Phasemask = Rectangle(self.width,self.height)
		self.add(Phasemask)

	def addDescription(self,text,location = 'top'):
		"""adds a description at the top of the phasemask dummy."""
		self.add(shapes.Label(text, 50, (0, 1800)))

	def addAlignementMarks(self,shape='cross'):
		"""adds the eight alignement marks to the phase mask. """

		pair = core.Elements()
		rect = shapes.Rectangle((-300,-300),(300,300))
		am = AlignementMark(shape=shape)

		d = (150,0)
		pair.add(utils.translate(am, d))
	
		am = AlignementMark(shape=shape)
		d = (-150,0)
		pair.add(utils.translate(am, d))
		d = (-2250,-1600)
		self.add(utils.translate(pair,d))
		d = (2250,1600)
		self.add(utils.translate(pair,d))
		d = (-2250,1600)
		self.add(utils.translate(pair,d))
		d = (2250,-1600)
		self.add(utils.translate(pair,d))

	def addMolocircles(self,default = True):
		"""add the molocircles to the Phase mask size layout"""

		if default:
			for i in xrange(0,10):

				self.add(shapes.Disk((400*i-5*400+200,+750), 400/2))
		

			for i in xrange(0,10):

				self.add(shapes.Disk((400*i-5*400+200,-250), 400/2))


			for i in xrange(0,10):
				
				self.add(shapes.Disk((400*i-5*400+200,-750), 300/2))
	
	def addPattern(self,shape='lines',radius = 0,x_size=0,x_spacing = 0,y_size=0,y_spacing = 0):
		"""creates a referencing pattern in the molographic """
		self.patternArea_x = 4000
		self.patternArea_y = 2000

		if shape == 'lines' or shapes == 'grid':
			
			if (y_spacing != 0):
				i = 0
				while (i*y_spacing) < self.patternArea_y:
					rect = shapes.Rectangle((-self.patternArea_x/2.,-y_size/2.),(self.patternArea_x/2.,y_size/2.))
					d = (0,i*y_spacing-self.patternArea_y/2.)
					self.add(utils.translate(rect,d))
					i += 1

			if x_spacing != 0:
				i = 0
				while i*(x_spacing) < self.patternArea_x:
					rect = shapes.Rectangle((-x_size/2.,-self.patternArea_y/2.),(x_size/2.,self.patternArea_y/2.))
					d = (i*x_spacing-self.patternArea_x/2.,0)
					self.add(utils.translate(rect,d))
					i += 1
		
		if shape == 'dots':

			y_span = self.patternArea_y/y_spacing
			x_span = self.patternArea_x/x_spacing

			for i in range(y_span+1):
				for j in range(x_span+1):
				
					rect = shapes.Disk((0,0),radius)
					d = (j*x_spacing-self.patternArea_x/2.,i*y_spacing-self.patternArea_y/2.)
					self.add(utils.translate(rect,d))
			

		if shape == 'rectangles':
			y_span = self.patternArea_y/y_spacing
			x_span = self.patternArea_x/x_spacing
			for i in range(y_span+1):
				for j in range(x_span+1):
					rect = shapes.Rectangle((-x_size/2.,-y_size/2.),(x_size/2.,y_size/2.))
					d = (j*x_spacing-self.patternArea_x/2.,i*y_spacing-self.patternArea_y/2.)
					self.add(utils.translate(rect,d))

		if shape == 'STED':
			# reference specifically for the field of view of the STED microscope. 
			print "hello"






class layer(core.Cell):
	"""docstring for layer"""

	def __init__(self, name):
		core.Cell.__init__(self,name)

	def xbar(self,Lambda,w,h,field_size,center=(0,0)):
		"""This simple function generates a grid of nanowires, all in the same layer, with period Lambda, height h, and width w. All units are in microns.
		""" 
		xstrip = shapes.Rectangle((0,0), (w, h))
		N = int(field_size/(Lambda))

		for i in range(N):
			print i
			d = (i*Lambda+center[0]-field_size/2.0,center[1] - field_size/2.0)
			self.add(utils.translate(xstrip, d))
		

	def alignment_mark(self,a=5,t=0.1,center=(0,0)):
		"""creates an alignement mark for e-Beam lithography, a is the side length of the alignement mark, t the thichness of the bar relative to the mark size"""

		boundary = [[0,0],[0,a/2.0],[a*t,a/2.0],[a*t,a*t],[a/2.0,a*t],[a/2.0,0]]
		right_part = core.Boundary(boundary)
		# N = int(field_size/(Lambda))

		d = (center[0],center[1])
		
		self.add(utils.translate(right_part, d))
		self.add(utils.translate(utils.rotate(right_part,180), d))
		

	def add_alignement_marks_around_structure(self,field_size,center=(0,0),a=5,t=0.1,):

		# self.alignment_mark(a,t,(-field_size/2.0-2*a+center[0],-field_size/2.0-2*a+center[1]))
		# self.alignment_mark(a,t,(field_size/2.0+2*a+center[0],-field_size/2.0-2*a+center[1]))
		# self.alignment_mark(a,t,(-field_size/2.0-2*a+center[0],field_size/2.0+2*a+center[1]))
		# self.alignment_mark(a,t,(field_size/2.0+2*a+center[0],field_size/2.0+2*a+center[1]))

		self.alignment_mark(a,t,(-field_size/2.0,-field_size/2.0))
		self.alignment_mark(a,t,(field_size/2.0,-field_size/2.0))
		self.alignment_mark(a,t,(-field_size/2.0,field_size/2.0))
		self.alignment_mark(a,t,(field_size/2.0,field_size/2.0))

def OpenInKlayout(file):
	"""opens the design in the Program Klayout """
	arg = quote_argument(os.path.dirname(os.path.abspath(__file__)))
	os.system("open -a klayout --args -s " + arg + '/' + file + '')


def quote_argument(argument):
    return '"%s"' % (
        argument
        .replace('\\', '\\\\')
        .replace('"', '\\"')
        .replace('$', '\\$')
        .replace('`', '\\`')
    )

def substraction(shape1,shape2):
	"""Shape """
	if isinstance(shape2,core.Elements):

		for i in shape2:
		
			substraction1 = utils.boolean(0, [shape1, i],lambda cir, tri: cir and not tri)

			shape1 = substraction1 

	else:
		substraction1 = utils.boolean(0, [shape1, shape2],lambda cir, tri: cir and not tri)

	return substraction1

if __name__ == '__main__':
	

	Wafer_4_inch = Wafer(4)
	Wafer_4_inch.setGrid(7000,6000)


	# pm1 = PhasemaskSize()
	# pm1.addMolocircles()

	# pm1.addAlignementMarks('cross')
	# pm1.addAlignementMarks('vernier')
	# pm1.addDescription('Exp1')
	# pm1.addPattern(shape='dots',radius = 5,x_spacing=50,x_size=5,y_size=10,y_spacing=20)
	# #pm1.addPattern(shape='dots',radius = 5,x_spacing=50,x_size=5,y_size=10,y_spacing=20)


	# for i in np.linspace(1,10,1):
	# 	Wafer_4_inch.placeDesign(pm1)

	disk1 = shapes.Disk((0,0), 1000/2)
	disk2 = shapes.Disk((0,0), 500/2)
	
	a= 200
	t = 20
	boundary = [[t/2.,t/2.],[a/2.,t/2.],[a/2.,-t/2],[t/2.,-t/2.],[t/2.,-a/2.],[-t/2.,-a/2],[-t/2.,-t/2.],
			[-a/2.,-t/2.],[-a/2.,t/2],[-t/2.,t/2.],[-t/2.,a/2.],[t/2.,a/2],[t/2.,t/2.]]
			
	cross = core.Boundary(boundary)

	print type(disk2)
	substraction1 = utils.boolean(0, [disk1, cross],lambda cir, tri: cir and not tri)

	cross2 = utils.translate(cross,(300,0))

	print type(substraction1)
	
	substraction2 = utils.boolean(0, [substraction1, cross2],lambda cir, tri: cir and not tri)
	cross3 = utils.translate(cross,(-300,0))
	
	substraction2 = utils.boolean(0, [substraction2, cross3],lambda cir, tri: cir and not tri)

	# test whether the element wise substraction works: 
	pm1 = core.Elements()
	pm1.add(cross)
	pm1.add(cross2)
	pm1.add(cross3)

	substraction1 = substraction(disk1,pm1)

	pm1 = core.Elements()
	rect1 = shapes.Rectangle((-400,-400),(400,400))
	rect2 = shapes.Rectangle((-200,-400),(200,400))
	# rect3 = shapes.Rectangle((-200,-200),(200,200))
	substraction1 = substraction(rect1,rect2)

	rect2 = shapes.Rectangle((-600,-600),(600,600))

	substraction2 = substraction(rect2,substraction1)


	
	Wafer_4_inch.add(substraction2)
	

	layout = core.Layout('LIBRARY',unit=1e-06, precision=1e-09)
	cell = core.Cell('TOP')
	cell.add(Wafer_4_inch)
	layout.add(cell)
	layout.save('20160108_4inch_Ring.gds')
	OpenInKlayout('20160108_4inch_Ring.gds')
	

	




