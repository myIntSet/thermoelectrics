import sys
sys.path.append('/../QmeQ/qmeq/')
import warnings
import qmeq
import numpy as np

#Serial dot
def run_sweep(VBs, epsilons, omega, u_intra, u_inter, gammaL, gammaR, T_L, T_R):

    if T_L < T_R:
        raise SystemExit("Not my convention! (T_L < T_R)")
    elif T_L > T_R:
        T_COLD = T_R
        T_HOT = T_L
    #elif T_L == T_R:
    #    raise SystemExit("Not a heat engine (T_L = T_R)")
    #lägga till fler checkar här!


    tL = np.sqrt(gammaL/np.pi/2)
    tR = np.sqrt(gammaR/np.pi/2)

    n, nleads = 4, 4 #two leads with spin
    U = {(0,1,1,0):u_intra, (2,3,3,2):u_intra, (0,2,2,0):u_inter, (0,3,3,0):u_inter, (1,2,2,1):u_inter, (1,3,3,1):u_inter } #more coloumb within than between
    tlst = {0:T_L, 1:T_L, 2:T_R, 3:T_R} #Temperatures


    I = np.zeros((len(VBs),len(epsilons)))
    I_var = np.zeros((len(VBs),len(epsilons)))
    J_QH = np.zeros((len(VBs),len(epsilons)))
    P = np.zeros((len(VBs),len(epsilons)))
    P_0 = np.zeros((len(VBs),len(epsilons)))

    for v_idx, vb in enumerate(VBs):
        mu_L = -vb/2       
        mu_R = vb/2        
        for e_idx, eps in enumerate(epsilons):
            system = qmeq.Builder(nsingle=n, hsingle={(0,0):eps, (1,1):eps, (2,2):eps, (3,3):eps, (0,2):omega, (1,3):omega}, coulomb=U, nleads=nleads,
                            mulst={0:mu_L, 1:mu_L, 2:mu_R, 3:mu_R}, tlst=tlst, tleads={(0, 0):tL, (1, 1):tL, (2, 2):tR, (3, 3):tR},
                            dband=1e4, countingleads=[0,1], kerntype='pyLindblad')
            system.solve()
            i = system.current_noise[0]
            i_var = system.current_noise[1]
            j_qh = system.heat_current[0]+system.heat_current[1]
            if i_var < 0 and np.abs(i_var) > 1e-16 and np.abs(i) > 1e-16:
                warnings.warn(f"Warning! Negative noise! {i_var} for V_B: {vb} and epsilon: {eps}\n (I = {i}, J_QH = {j_qh})")
            I[v_idx, e_idx] = i
            I_var[v_idx, e_idx] = i_var
            J_QH[v_idx, e_idx] = j_qh
            P[v_idx, e_idx] = i*vb

            rho = system.phi0
            P_0[v_idx, e_idx] = rho[0]


    #====================Pruning==========<----WRONG!!!!!
    #Puting negative currents, heatcurrents and small negative I_var to zero
    #I[(I < 0) | (J_QH < 0) | ((I_var < 0) & (np.abs(I_var) < 1e-16))] = np.nan 
    #I[(I < 0) | (J_QH < 0)] = np.nan
    #I_var[np.isnan(I)] = np.nan
    #J_QH[np.isnan(I)] = np.nan
    '''
    #====================Pruning==============<-------------PROPER TEMPLATE!!!!
    #Remove values that won't generate a TUR (not a heat engine, or numerical negative noise issue)
    if V_B > 0:
        I[(I < 0) | ((I_var < 0) & (np.abs(I_var) < 1e-16))] = np.nan
    elif V_B < 0:
        I[(I > 0) | ((I_var < 0) & (np.abs(I_var) < 1e-16))] = np.nan
    I_var[np.isnan(I)] = np.nan
    J_QH[np.isnan(I)] = np.nan
    '''

    #Calculations of efficiency, sigma and TUR
    #eff_carnot = 1-(T_COLD/T_HOT)
    #eff = P/J_QH
    #sigma = P*(1/T_COLD)*(eff_carnot-eff)/eff
    #TUR = I_var*sigma/(I**2)

    return I, I_var, J_QH, P, P_0   #, eff, sigma, TUR