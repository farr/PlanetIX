#!/usr/bin/env python

from pylab import *

import gzip
import os
import pickle
import rebound as re
import utils as u

if __name__ == '__main__':
    loadpath = 'simulation.save'
    if os.path.exists(loadpath):
        loaded = True
        start_t = sim.t
        sim = re.Simulation.from_file(loadpath)
    else:
        loaded = False
        start_t = 0
        sim = u.outer_solar_system()
        sim = u.add_canonical_planar_perturber(sim)
        for e in linspace(0, 1, 21)[:-1]:
            for pomega in linspace(0, 2*pi, 21)[:-1]:
                sim.add(m=0, a=450, e=e, inc=abs(pi/180.0*randn()), pomega=pomega, l=2*pi*rand())
        sim.N_active = 6
    
    for t in linspace(sim.t, sim.t+2*pi*1e9, 1000):
        sim.integrate(t, exact_finish_time=0)

        if not (loaded and sim.t == start_t):
            with gzip.open('orbits.pkl.gz', 'a') as out:
                pickle.dump((sim.t, sim.calculate_orbits()), out)

            tfile = 'simulation.save.temp'
            ofile = 'simulation.save'
            sim.save(tfile)
            os.rename(tfile, ofile)

	print 'Evolved to ', sim.t
