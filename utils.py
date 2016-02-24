from pylab import *

import rebound as re

def outer_solar_system():
    sim = re.Simulation()
    sim.add(['Sun', 'Jupiter', 'Saturn', 'Uranus', 'Neptune'])
    sim.move_to_com()
    sim.dt = 4
    sim.integrator = 'whfast'
    sim.integrator_whfast_safe_mode = 0
    sim.integrator_whfast_corrector = 11
    
    return sim

def add_canonical_planar_perturber(sim):
    sim.add(m=3e-5, a=700, e=0.6, pomega=2*pi*rand(), l=2*pi*rand())
    return sim

def add_planar_testmass_disk(sim, Npart):
    N_active = sim.N

    for i in range(Npart):
        a = 50 + 500*rand()
        q = 30 + 20*rand()
        e = 1 - q/a
        pomega = 2*pi*rand()

        sim.add(m=0, a=a, e=e, pomega=pomega, l=2*pi*rand())

    sim.N_active = N_active

    return sim
