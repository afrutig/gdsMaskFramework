import numpy as np
import math as math
import matplotlib.pyplot as plt
from gdsCAD_local.boolean_AF import *
import os
import numpy as np
#from gdsCAD_local import core,shapes,utils
import gdspy as gdy

from gdsCAD_local import *
from fsc.export import export



@export
class Wafer(core.Elements):
	"""This class generates a wafer with diameter size, the center of the wafer is at the origin of the coordinate system at (0,0)

	:param size: Wafer size in inches
	"""
	def __init__(self,size = 4,draw=True,shape='disk'):
		super(Wafer, self).__init__()

		self.size = size
		inch = 25400
		self.radius = self.size*inch/2.
		self.line_thickness = 500

		if shape == 'disk':

			self.usableArea = 0.9*np.sqrt(2)*self.radius

			if draw:
				wafer = Rectangle(self.usableArea,self.usableArea,0)
				self.add(wafer)
				
				wafer = shapes.Circle((0.,0.), self.radius,0)
				self.add(wafer)
				wafer = Rectangle(self.radius*2,self.radius*2,0)
				self.add(wafer)
		
		if shape == 'rectangle':
			self.usableArea = 0.9*2*self.radius

			if draw:
				wafer = Rectangle(self.usableArea,self.usableArea,0)
				self.add(wafer)


		self.x_index = 0
		self.y_index = 0


	def setGrid(self,x_spacing,y_spacing,x_offset = 0,y_offset = 0):
		
		"""sets the gridsize on the wafer's usable area.

		:param: x_spacing, the length of a design block in x direction without the offset included
		:param: y_spacing, the height of a design block in y direction without the y_offset included
		:param: x_offset, spacing that is added on both sides of the design in x direction
		:param: y_offset, spacing that is added on both sides of the design in y direction

		All sizes are in microns.

		"""

		self.x_spacing = x_spacing
		self.y_spacing = y_spacing
		self.x_offset = x_offset
		self.y_offset = y_offset
		self.x_max_index = self.usableArea/(x_spacing+x_offset)
		self.y_max_index = self.usableArea/(y_spacing+y_offset)

	def addGridAlignementMarks(self):

		"""Places alignement marks for the dicing on the Grid edges."""

		self.y_index = 0
		self.x_index = 0


		am = AlignementMark(1000,200)
		for i in range(int(self.x_max_index*(self.y_max_index) - 6)):

			x_index = self.x_index
			y_index = self.y_index

			# places the alignement mark in the top left corner.
			self.placeDesign(am,(-self.x_spacing/2.,self.y_spacing/2.),N=1)

			if self.x_offset != 0:
				self.x_index = x_index
				self.y_index = y_index

				# places the alignement mark in the top right corner.
				self.placeDesign(am,(-self.x_spacing/2.+self.x_spacing,self.y_spacing/2.),N=1)

			if self.y_offset != 0:
				self.x_index = x_index
				self.y_index = y_index

				# places the alignement mark in the bottom left corner.
				self.placeDesign(am,(-self.x_spacing/2.,self.y_spacing/2.-self.y_spacing),N=1)

			if self.x_offset != 0 and self.y_offset != 0:
				self.x_index = x_index
				self.y_index = y_index

				# places the alignement mark in the bottom right corner.
				self.placeDesign(am,(-self.x_spacing/2.+self.x_spacing,self.y_spacing/2.-self.y_spacing),N=1)



		self.y_index = 0
		self.x_index = 0



	def placeDesign(self,design,offset=(0,0),N=1):

		"""places a design at the next free location on the wafer grid, starting at the top left corner and fills it row wise"""
		
		d = ((self.x_spacing+self.x_offset)*(self.x_index-self.x_max_index/2+1/2.)+offset[0],-(self.y_spacing+self.y_offset)*(self.y_index-self.y_max_index/2+1/2.) + offset[1])

		if self.x_index == int(self.x_max_index)- N:
			self.y_index += 1
			self.x_index = 0
		else:
			self.x_index += 1

		self.add(utils.translate(design,d))

@export
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

@export
class AlignementMark(core.Elements):
	"""creates an cross-shaped alignement mark, a is the side length of the alignement mark, t the thichness of the bar relative to the mark size"""

	def __init__(self,a=200,t=20,center=(0,0),shape='cross',inverse = True):
		super(AlignementMark, self).__init__()


		if shape == 'cross':

			boundary = [[t/2.,t/2.],[a/2.,t/2.],[a/2.,-t/2],[t/2.,-t/2.],[t/2.,-a/2.],[-t/2.,-a/2],[-t/2.,-t/2.],
			[-a/2.,-t/2.],[-a/2.,t/2],[-t/2.,t/2.],[-t/2.,a/2.],[t/2.,a/2],[t/2.,t/2.]]
			
			cross = core.Boundary(boundary)

			self.add(cross)


		if shape == 'vernier':
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

@export
class PhasemaskSize(core.Elements):
	"""creates a blueprint of the size of a phase mask"""
	def __init__(self,description_only = False,draw=True,width=7000,height=6000):
		super(PhasemaskSize, self).__init__()
		
		self.width = width
		self.height = height
		if draw:	
			Phasemask = Rectangle(self.width,self.height)
			self.add(Phasemask)
		self.description_only = description_only

	def addDescription(self,text,location = 'top'):
		"""adds a description at the top of the phasemask dummy."""
		if self.description_only:
			self.add(shapes.Label(text, 350, (-3000, 0)))

		else:

			self.add(shapes.Label(text, 100, (-500, 1800)))

	def addAlignementMarks(self,shape='cross',inverse = True):
		"""adds the eight alignement marks to the phase mask. if inverse is True the alignement mark is for 
		positive resist."""

		if not self.description_only:
			pair = core.Elements()
			rect = shapes.Rectangle((-400,-200),(400,200))
			am = AlignementMark(shape=shape)

			d = (150,0)
			pair.add(utils.translate(am, d))
		
			am = AlignementMark(shape=shape)
			d = (-150,0)
			pair.add(utils.translate(am, d))

			if inverse == True:

				sub = substraction(rect,pair)
			else:
				sub = pair

			d = (-2250,-1600)
			self.add(utils.translate(sub,d))
			d = (2250,1600)
			self.add(utils.translate(sub,d))
			d = (-2250,1600)
			self.add(utils.translate(sub,d))
			d = (2250,-1600)
			self.add(utils.translate(sub,d))

	def addMolocircles(self,L1=[0,1,2,3,4,5,6,7,8,9],L3=[0,1,2,3,4,5,6,7,8,9],L4=[0,1,2,3,4,5,6,7,8,9],size=400):
		"""add the molocircles to the Phase mask size layout"""

		if not self.description_only:
			if not isinstance(L1,int):
				for i in L1:

					self.add(shapes.Disk((400*i-5*400+200,+750), size/2))
		
			if not isinstance(L3,int):
				for i in L3:

					self.add(shapes.Disk((400*i-5*400+200,-250), size/2))

			if not isinstance(L4,int):
				for i in L4:
					
					self.add(shapes.Disk((400*i-5*400+200,-750), size/2))
		
	def addPattern(self,shape='lines',radius = 0,x_size=0,x_spacing = 0,y_size=0,y_spacing = 0):
		"""creates a referencing pattern in the molographic """
		self.patternArea_x = 4000
		self.patternArea_y = 2000

		if shape == 'lines':

			self.addDescription('LINES X' + str(x_size) + 'Y' + str(y_size) + 'XSP' + str(x_spacing) + 'YSP' + str(y_spacing))

			if not self.description_only:

				if (y_spacing != 0):
					y_span = self.patternArea_y/y_spacing
					for i in range(y_span+1):
						rect = shapes.Rectangle((-self.patternArea_x/2.,-y_size/2.),(self.patternArea_x/2.,y_size/2.))
						d = (0,i*y_spacing-self.patternArea_y/2.)
						self.add(utils.translate(rect,d))

				if (x_spacing != 0):
					x_span = self.patternArea_x/x_spacing
					for i in range(x_span+1):
						rect = shapes.Rectangle((-x_size/2.,-self.patternArea_y/2.),(x_size/2.,self.patternArea_y/2.))
						d = (i*x_spacing-self.patternArea_x/2.,0)
						self.add(utils.translate(rect,d))

		if shape == 'grid':
			
			self.addDescription('GRID X' + str(x_size) + 'Y' + str(y_size) + 'XSP' + str(x_spacing) + 'YSP' + str(y_spacing))

			if not self.description_only:
				y_span = self.patternArea_y/y_spacing
				x_span = self.patternArea_x/x_spacing

				for i in range(y_span+1):
					for j in range(x_span+1):
						rect = shapes.Rectangle((-self.patternArea_x/2.,-y_size/2.),(self.patternArea_x/2.,y_size/2.))
						d = (0,i*y_spacing-self.patternArea_y/2.)
						self.add(utils.translate(rect,d))
						rect = shapes.Rectangle((-x_size/2.,-self.patternArea_y/2.),(x_size/2.,self.patternArea_y/2.))
						d = (j*x_spacing-self.patternArea_x/2.,0)
						self.add(utils.translate(rect,d))


		if shape == 'dots':

			self.addDescription('DOTS R' + str(radius) + 'XSP' + str(x_spacing) + 'YSP' + str(y_spacing))

			if not self.description_only:

				

				y_span = self.patternArea_y/y_spacing
				x_span = self.patternArea_x/x_spacing

				for i in range(y_span+1):
					for j in range(x_span+1):
					
						rect = shapes.Disk((0,0),radius)
						d = (j*x_spacing-self.patternArea_x/2.,i*y_spacing-self.patternArea_y/2.)
						self.add(utils.translate(rect,d))
			

		if shape == 'rectangles':

			self.addDescription('SQUA X' + str(x_size) + 'Y' + str(y_size) + 'XSP' + str(x_spacing) + 'YSP' + str(y_spacing))


			if not self.description_only:

				
				y_span = self.patternArea_y/y_spacing
				x_span = self.patternArea_x/x_spacing
				for i in range(y_span+1):
					for j in range(x_span+1):
						rect = shapes.Rectangle((-x_size/2.,-y_size/2.),(x_size/2.,y_size/2.))
						d = (j*x_spacing-self.patternArea_x/2.,i*y_spacing-self.patternArea_y/2.)
						self.add(utils.translate(rect,d))


@export
class ZeptoChip(core.Elements):
	"""This is a container in the shape of a Zeptochip with """
	def __init__(self):
		super(ZeptoChip, self).__init__()
		self.width = 14000
		self.height = 57000
		self.index = 0
		Zeptochip = Rectangle(self.width,self.height,50)
		self.add(Zeptochip)

	def placeDesign(self,design):
		"""places the design at the next free location on the Zeptochip, fills from top to bottom"""

		d = (0,-self.index*9000+self.height/2-6000)

		
		self.index += 1 

		

		self.add(utils.translate(design,d))

	def addDescription(self,text,location = 'top'):
		"""adds a description at the top of the phasemask dummy."""

		self.add(shapes.Label(text, 100, (0, 0)))

		


@export
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

@export
def OpenInKlayout(file):
	"""opens the design in the Program Klayout - Mac OS X El Capitan only"""
	arg = quote_argument(os.getcwd())
	os.system("open -a klayout --args -s " + arg + '/' + file + '')


def quote_argument(argument):
    return '"%s"' % (
        argument
        .replace('\\', '\\\\')
        .replace('"', '\\"')
        .replace('$', '\\$')
        .replace('`', '\\`')
    )


if __name__ == '__main__':
	

	Wafer_4_inch = Wafer(4)
	Wafer_4_inch.setGrid(6800,5800,1000,1000)
	Wafer_4_inch.addGridAlignementMarks()


	pm1 = PhasemaskSize()
	pm1.addMolocircles()

	pm1.addAlignementMarks('cross')
	pm1.addAlignementMarks('vernier')
	pm1.addDescription('Exp1')
	pm1.addPattern(shape='dots',radius = 5,x_spacing=50,x_size=5,y_size=10,y_spacing=20)
	#pm1.addPattern(shape='dots',radius = 5,x_spacing=50,x_size=5,y_size=10,y_spacing=20)


	for i in np.linspace(1,10,10):
		Wafer_4_inch.placeDesign(pm1)

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
	# pm1 = core.Elements()
	# pm1.add(cross)
	# pm1.add(cross2)
	# pm1.add(cross3)

	# substraction1 = substraction(disk1,pm1)

	# pm1 = core.Elements()
	# rect1 = shapes.Rectangle((-400,-400),(400,400))
	# rect2 = shapes.Rectangle((-200,-400),(200,400))
	# # rect3 = shapes.Rectangle((-200,-200),(200,200))
	# substraction1 = substraction(rect1,rect2)

	# rect2 = shapes.Rectangle((-600,-600),(600,600))

	# substraction2 = substraction(rect2,substraction1)


	
	# Wafer_4_inch.add(substraction2)
	

	layout = core.Layout('LIBRARY',unit=1e-06, precision=1e-09)
	cell = core.Cell('TOP')
	cell.add(Wafer_4_inch)
	layout.add(cell)
	layout.save('20160108_4inch_Ring.gds')
	OpenInKlayout('20160108_4inch_Ring.gds')
	

	




