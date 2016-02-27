#!/usr/bin/env python

from pylab import *

import gzip
import os
import pickle
import rebound as re
import utils as u

if __name__ == '__main__':
    loadfile = 'simulation.save'
    if os.path.exists(loadfile):
        sim = re.Simulation.from_file(loadfile)
        loaded = True
        start_t = sim.t
    else:
        loaded = False
        start_t = 0
        sim = u.outer_solar_system()
        sim = u.add_canonical_planar_perturber(sim)
        sim = u.add_planar_testmass_disk(sim, 400)

    for t in linspace(sim.t, sim.t+2*pi*1e9, 1000):
        sim.integrate(t, exact_finish_time=0)

        if not (loaded and start_t == sim.t):
            with gzip.open('orbits.pkl.gz', 'a') as out:
                pickle.dump((sim.t, sim.calculate_orbits()), out)

            tfile = 'simulation.save.temp'
            sfile = 'simulation.save'
            sim.save(tfile)
            os.rename(tfile, sfile)

        print 'Evolved to ', sim.t
        
