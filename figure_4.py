#!/usr/bin/env python

from pylab import *

from argparse import ArgumentParser
import gzip
import os
import pickle
import rebound as re
import utils as u

if __name__ == '__main__':
    parser = ArgumentParser()

    parser.add_argument('--outdir', default='.', metavar='DIR', help='output dir (default: %(default)s)')

    args = parser.parse_args()

    loadpath = os.path.join(args.outdir, 'simulation.save')
    if os.path.exists(loadpath):
        sim = re.Simulation.from_file(loadpath)
    else:       
        sim = u.outer_solar_system()
        sim = u.add_canonical_planar_perturber(sim)
        for e in linspace(0, 1, 21)[:-1]:
            for pomega in linspace(0, 2*pi, 21)[:-1]:
                sim.add(m=0, a=450, e=e, inc=abs(pi/180.0*randn()), pomega=pomega, l=2*pi*rand())
        sim.N_active = 6
    
    for t in linspace(0, 2*pi*1e9, 1000):
        sim.integrate(t, exact_finish_time=0)

        with gzip.open(os.path.join(args.outdir, 'orbits.pkl.gz'), 'a') as out:
            pickle.dump((sim.t, sim.calculate_orbits()), out)

        tfile = os.path.join(args.outdir, 'simulation.save.temp')
        ofile = os.path.join(args.outdir, 'simulation.save')
        sim.save(tfile)
        os.rename(tfile, ofile)
