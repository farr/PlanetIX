#!/usr/bin/env python

from pylab import *

from argparse import ArgumentParser
import gzip
import os
import pickle
import rebound as re

def init_sim(Ntest=1000, outdir='.'):
    loadpath = os.path.join(outdir, 'simulation.save')
    if os.path.exists(loadpath):
        print 'Loading simulation...'

        sim = re.Simulation.from_file(loadpath)
    else:
        print 'Initialising new simulation...'

        sim = re.Simulation()
        sim.add(['Sun', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'])
        sim.add(m=3e-5, a=700, e=0.6, omega=150.0*pi/180.0, inc=30.0*pi/180.0, l=np.random.uniform(low=0,high=2*pi)) # Perturber
        sim.move_to_com()
        sim.dt = 1.0
        sim.integrator = 'whfast'
        sim.integrator_whfast_safe_mode = 0
        sim.integrator_whfast_corrector = 11

        for i in range(Ntest):
            a = np.random.uniform(low=150, high=550)
            q = np.random.uniform(low=30, high=50)
            e = 1 - q/a
            inc = np.abs(np.random.randn()*15.0*pi/180.0)
            omega = np.random.uniform(low=0,high=2*pi)
            Omega = np.random.uniform(low=0,high=2*pi)
            l = np.random.uniform(low=0, high=2*pi)
            sim.add(a=a, e=e, inc=inc, omega=omega, Omega=Omega, l=l)

        sim.N_active = sim.N - Ntest

    sim.status()
    return sim

def run_sim(sim, dt=2*pi*1e9, Nout=10000, outdir='.'):
    t0 = sim.t

    for t in linspace(t0, t0+dt, Nout):
        sim.integrate(t, exact_finish_time=0)
        print 'Integrated to ', sim.t

        orbs = sim.calculate_orbits()

        with gzip.open(os.path.join(outdir, 'orbits.pkl.gz'), 'a') as out:
            pickle.dump((sim.t, orbs), out)

        tfile = os.path.join(outdir, 'temp.simulation')
        ofile = os.path.join(outdir, 'simulation.save')
        sim.save(tfile)
        os.rename(tfile, ofile)

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--outdir', default='.', help='output directory (default %(default)s)')

    args = parser.parse_args()
    
    sim = init_sim(outdir=args.outdir)

    run_sim(sim, outdir=args.outdir)
