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
    sim.add(m=3e-5, a=700, e=0.6, inc=abs(randn()*pi/180.0), Omega=2*pi*rand(), omega=2*pi*rand(), l=2*pi*rand())
    return sim
