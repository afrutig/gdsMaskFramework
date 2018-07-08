import numpy as np

import math as math
import matplotlib.pyplot as plt
import sys
sys.path.append("../../")
from gdsCAD_local import *
from gdsCAD_local.boolean_AF import *
import os
import numpy as np


Wafer = core.Elements()

# Example 1
#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

# test whether the element wise substraction works: 


disk1 = shapes.Disk((0,0), 1000/2)
disk2 = shapes.Disk((0,0), 500/2)

a= 200
t = 20
boundary = [[t/2.,t/2.],[a/2.,t/2.],[a/2.,-t/2],[t/2.,-t/2.],[t/2.,-a/2.],[-t/2.,-a/2],[-t/2.,-t/2.],
		[-a/2.,-t/2.],[-a/2.,t/2],[-t/2.,t/2.],[-t/2.,a/2.],[t/2.,a/2],[t/2.,t/2.]]
cross = core.Boundary(boundary)
cross2 = utils.translate(cross,(300,0))
cross3 = utils.translate(cross,(-300,0))

pm1 = core.Elements()
pm1.add(cross)
pm1.add(cross2)
pm1.add(cross3)

substraction1 = substraction(disk1,pm1)

Wafer.add(utils.translate(pm1,(-1000,1000)))
Wafer.add(utils.translate(disk1,(-2000,1000)))
Wafer.add(utils.translate(substraction1,(0,1000)))

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

disk1 = shapes.Disk((0,0), 100/2)
disk2 = shapes.Disk((0,0), 400/2)

substraction2 = substraction(disk1,disk2)

# should be none, therefore cannot be added
Wafer.add(utils.translate(disk1,(-2000,0)))
Wafer.add(utils.translate(disk2,(-1000,0)))
if substraction2 is not None:

	Wafer.add(substraction2)


#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------


pm1 = core.Elements()
disk1 = shapes.Disk((0,0), 100/2)
disk2 = shapes.Disk((0,0), 400/2)
pm1.add(utils.translate(disk1,(-200,0)))
pm1.add(utils.translate(disk1,(200,0)))
substraction2 = substraction(disk2,pm1)
Wafer.add(utils.translate(pm1,(-1000,-1000)))
Wafer.add(utils.translate(disk2,(-2000,-1000)))
Wafer.add(utils.translate(substraction2,(0,-1000)))

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------


pm1 = core.Elements()
disk1 = shapes.Disk((0,0), 100/2)
disk2 = shapes.Disk((0,0), 400/2)
pm1.add(utils.translate(disk1,(-200,0)))
pm1.add(utils.translate(disk1,(200,0)))
substraction3 = substraction(pm1,disk2)
Wafer.add(utils.translate(pm1,(-1000,-2000)))
Wafer.add(utils.translate(disk2,(-2000,-2000)))
Wafer.add(utils.translate(substraction3,(0,-2000)))

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

pm1 = core.Elements()
pm2 = core.Elements()
disk1 = shapes.Disk((0,0), 100/2)
disk2 = shapes.Disk((0,0), 400/2)
pm1.add(utils.translate(disk1,(-200,0)))
pm1.add(utils.translate(disk1,(200,0)))
pm1.add(utils.translate(disk1,(0,200)))
pm1.add(utils.translate(disk1,(0,-200)))
pm2.add(utils.translate(disk2,(200,0)))
pm2.add(utils.translate(disk2,(-200,0)))
substraction3 = substraction(pm1,pm2)
Wafer.add(utils.translate(pm2,(-1000,-3000)))
Wafer.add(utils.translate(pm1,(-2000,-3000)))
Wafer.add(utils.translate(substraction3,(0,-3000)))

#-----------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------

pm1 = core.Elements()
pm2 = core.Elements()
disk1 = shapes.Disk((0,0), 100/2)
disk2 = shapes.Disk((0,0), 400/2)
pm1.add(utils.translate(disk1,(-200,0)))
pm1.add(utils.translate(disk1,(200,0)))
pm1.add(utils.translate(disk1,(0,200)))
pm1.add(utils.translate(disk1,(0,-200)))
pm2.add(utils.translate(disk2,(200,0)))
pm2.add(utils.translate(disk2,(-200,0)))
substraction3 = substraction(pm1,pm2)
Wafer.add(utils.translate(pm2,(-1000,-3000)))
Wafer.add(utils.translate(pm1,(-2000,-3000)))
Wafer.add(utils.translate(substraction3,(0,-3000)))


rect1 = shapes.Rectangle((-400,-400),(400,400))
rect2 = shapes.Rectangle((-200,-400),(200,400))
# rect3 = shapes.Rectangle((-200,-200),(200,200))
substraction1 = substraction(rect1,rect2)

rect2 = shapes.Rectangle((-600,-600),(600,600))

substraction2 = substraction(rect2,substraction1)
Wafer.add(utils.translate(substraction2,(-3000,-4000)))



# Wafer.add(substraction2)


layout = core.Layout('LIBRARY',unit=1e-06, precision=1e-09)
cell = core.Cell('TOP')
cell.add(Wafer)
layout.add(cell)
layout.save('20160108_4inch_Ring.gds')
OpenInKlayout('20160108_4inch_Ring.gds')