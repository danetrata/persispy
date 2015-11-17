GPU = 1 # use the GPU
DIR = '/home/jan/Problems/GPUdata/MultiPath' # location of systems
from phcpy.phcpy2c \
import py2c_read_standard_target_system_from_file as read_target
from phcpy.phcpy2c \
import py2c_read_standard_start_system_from_file as read_start
cyc10tarfile = DIR + '/cyclic10.target'
cyc10stafile = DIR + '/cyclic10.start'
fail = read_target(len(cyc10tarfile), cyc10tarfile)
from phcpy.interface import load_standard_system as loadsys
from phcpy.interface import load_standard_solutions as loadsols
cyc10 = loadsys()
print 'the cyclic 10-roots problem :'
for pol in cyc10:
    print pol
fail = read_start(len(cyc10stafile), cyc10stafile)
cyc10q = loadsys()
print 'a start system for the cyclic 10-roots problem :'
for pol in cyc10q:
    print pol
cyc10qsols = loadsols()
print 'number of start solutions :', len(cyc10qsols)
print 'the first solution :'
print cyc10qsols[0]
print 'calling the path tracker...'
if(GPU == 0):
    from phcpy.trackers import ade_double_track
    cyc10sols = ade_double_track(cyc10,cyc10q,cyc10qsols,verbose=0)
else:
    from phcpy.trackers import gpu_double_track
    cyc10sols = gpu_double_track(cyc10,cyc10q,cyc10qsols,verbose=0)
print 'number of solutions :', len(cyc10sols)
for sol in cyc10sols:
    print sol

