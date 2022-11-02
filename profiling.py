# %time
# %timeit
# %prun
# %lprun
# %memit
# %mprun

#   NOTES gia tin askisi #:
#   
#
#
#
#



# magic command % --> only one line
#               %% for all the shell

import time
import statistics
from line_profiler import LineProfiler

def sum_oflists(N):
        total = 0
        for i in range(5):
            L = [j ^ (j >> i) for j in range(N)]
            total += sum(L)
        return total


import cProfile
import time




n = 100
lp = LineProfiler()
lp_wrapper = lp(sum_oflists)
lp_wrapper(n)
lp.print_stats()


cProfile.run("profiling.sum_of_lists(10000)")
