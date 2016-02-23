#!/usr/bin/env python

from pylab import *

import gzip
import os
import pickle
import rebound as re

def init_sim(Ntest=1000):
    if os.path.exists('simulation.save'):
        print 'Loading simulation...'

        sim = re.Simulation.from_file('simulation.save')
    else:
        print 'Initialising new simulation...'

        sim = re.Simulation()
        sim.add(['Sun', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'])
        sim.add(m=3e-5, a=700, e=0.6, pomega=pi, l=np.random.uniform(low=0,high=2*pi)) # Perturber
        sim.move_to_com()
        sim.dt = 1.0
        sim.integrator = 'whfast'
        sim.integrator_whfast_safe_mode = 0
        sim.integrator_whfast_corrector = 11

        for i in range(Ntest):
            a = np.random.uniform(low=50, high=550)
            q = np.random.uniform(low=30, high=50)
            e = 1 - q/a
            pomega = np.random.uniform(low=0, high=2*pi)
            l = np.random.uniform(low=0, high=2*pi)
            sim.add(a=a, e=e, pomega=pomega, inc=0, l=l)

        sim.N_active = sim.N - Ntest

    sim.status()
    return sim

def run_sim(sim, dt=2*pi*1e9, Nout=10000):
    t0 = sim.t

    for t in linspace(t0, t0+dt, Nout):
        sim.integrate(t, exact_finish_time=0)
        print 'Integrated to ', sim.t

        orbs = sim.calculate_orbits()

        with gzip.open('orbits.pkl.gz', 'a') as out:
            pickle.dump((sim.t, orbs), out)

        sim.save('temp.simulation')
        os.rename('temp.simulation', 'simulation.save')

if __name__ == '__main__':
    sim = init_sim()

    run_sim(sim)
