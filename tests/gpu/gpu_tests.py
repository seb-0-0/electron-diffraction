#from blochwave import bloch
from blochwave import gpu_diagonalisation as bloch

import matplotlib
matplotlib.use('QtAgg')

b0 = bloch.Bloch('diamond',path='',u=[0,0,1],Nmax=3,Smax=0.1,opts='svt')

b0.show_beams_vs_thickness()