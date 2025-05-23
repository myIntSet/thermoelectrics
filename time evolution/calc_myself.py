import numpy as np
import matplotlib.pyplot as plt
import importlib
import time_evolutor as te
import plotting as p

import sys
sys.path.append('/../../temp_prog/')
import tur_calculator as tc

def do_all(ti_array, long_time=False):
    #------------------SETUP-------------------
    T_L = 25 
    T_R = 10
    V_B = 30
    eps = 50
    u = 250
    gamma = 1
    delta_gamma = 0.04 #0.04
    delta_epsilon = 0.04 #0.04

    INPUT = {
        'eps': eps,
        'omega': 0, 
        'u': u, 
        'V_B': V_B,
        'gamma': gamma,  
        'T_L': T_L,
        'T_R': T_R,
        'delta_gamma': delta_gamma,
        'delta_epsilon': delta_epsilon,
    }

    initial = [1/4,1/4,1/4,1/4,0,0]         #beginns with both QDs empty


    importlib.reload(te)
    sys, liouvillian, dim, eval_j, left_ev, right_ev, nleads = te.calculate_paper_meta(initial, ti_array, **INPUT, just_lio=True)

    #Theoretically calculating my_rho

    muL = -V_B/2
    muR = V_B/2

    def fermi(mu, E, T):
        return 1/(1+np.exp((E-mu)/T))

    def avg_fermi(eps):
        return (fermi(muL, eps, T_L)+fermi(muR, eps, T_R))/2

    avg_fermi_e = avg_fermi(eps)
    avg_fermi_eU = avg_fermi(eps+u)

    my_rho1 = np.zeros(dim)
    my_rho2 = np.zeros(dim)

    #filling up my_rho1:
    my_rho1[0] = 1-avg_fermi_e
    my_rho1[1] = avg_fermi_e/2
    my_rho1[2] = avg_fermi_e/2
    my_rho1[4] = avg_fermi_e/2

    #filling up my_rho2:
    my_rho2[1] = (1-avg_fermi_eU)/2
    my_rho2[2] = (1-avg_fermi_eU)/2
    my_rho2[3] = avg_fermi_eU
    my_rho2[4] = -(1-avg_fermi_eU)/2

    # -----------------------------PARTICLE CURRENT-------------------------------------
    # qmeq solution for stationary current (at left lead)
    I_ss = sys.current[0]

    # reset current    
    sys.current[:] = np.zeros(nleads)
    sys.energy_current[:] = np.zeros(nleads)

    # set stationary state to my_rho value
    sys.phi0[:] = np.real(my_rho1[:])

    # calculate current (also calculates energy and heat currents)
    sys.appr.generate_current() # calculates current both ways
    J_QH_tot = sys.heat_current
    I_test = sys.current[0]
    I = sys.current_noise[0] 
    I_var = sys.current_noise[1]
    #--------------------------------------------
    # take QmeQ heat current at left lead   
    J_QH = J_QH_tot[0]

    #Power
    P = I*V_B

    importlib.reload(te)
    rho_ss, rho_t = te.time_evolution(left_ev, right_ev, eval_j, my_rho1, liouvillian, ti_array, dim)

    # -----------------------------PARTICLE CURRENT-------------------------------------
    J_QH_tot = np.zeros((nleads,ti_array.shape[0]))
    I = np.zeros((ti_array.shape[0]))
    I_var = np.zeros((ti_array.shape[0]))


    for i in range(ti_array.shape[0]):
        
        # reset current    
        sys.current[:] = np.zeros(nleads)
        sys.energy_current[:] = np.zeros(nleads)
        
        
        # set stationary state to rho_t value
        sys.phi0[:] = np.real(rho_t[:,i])
        
        # calculate current (also calculates energy and heat currents)
        sys.appr.generate_current() # calculates current both ways
        J_QH_tot[:,i] = sys.heat_current
        I[i] = sys.current_noise[0] 
        I_var[i] = sys.current_noise[1]
        
        #--------------------------------------------

    # take QmeQ heat current at left lead   
    J_QH = J_QH_tot[0]

    #Power
    P = I*V_B

    importlib.reload(tc)
    TUR, eff_carnot, eff, sigma = tc.calculate_tur(T_L, T_R, I, I_var, J_QH, P)

    return TUR, I, I_var, sigma