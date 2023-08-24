#from blochwave import bloch
#Remember that structure_factor and structure_factor_if_gpu have been switched; the original code is in structure_factor_if_gpu and the if statement is in structure_factor
from blochwave import gpu_diagonalisation as bloch
from blochwave import gpu_diagonalisation_tests_with_cp_and_np as bloch2
import matplotlib
import pylab as plt
import cupy as cp
matplotlib.use('QtAgg')

b0 = bloch.Bloch('diamond',path='',u=[0,0,1],Nmax=3,Smax=0.1,opts='svt')
b1 = bloch2.Bloch('diamond',path='',u=[0,0,1],Nmax=3,Smax=0.1,opts='svt')

print(cp.linalg.norm(b0.gammaj - cp.array(b1.gammaj)))

b1.show_beams_vs_thickness()
plt.show()