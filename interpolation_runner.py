import sys
sys.path.append('/../QmeQ/qmeq/')
import warnings
import qmeq
import numpy as np



def run_interpolation(epsilons, lamdas, omega, u_intra, u_inter, V_B, gammaL, gammaR, T_L, T_R):

    if T_L < T_R:
        raise SystemExit("Not my convention! (T_L < T_R)")
    elif T_L > T_R:
        T_COLD = T_R
        T_HOT = T_L
    elif T_L == T_R:
        raise SystemExit("Not a heat engine (T_L = T_R)")
    #lägga till fler checkar här!

    mu_L = -V_B/2       
    mu_R = V_B/2        
    tL = np.sqrt(gammaL/np.pi/2)
    tR = np.sqrt(gammaR/np.pi/2)

    n, nleads = 4, 4 #two leads with spin
    U = {(0,1,1,0):u_intra, (2,3,3,2):u_intra, (0,2,2,0):u_inter, (0,3,3,0):u_inter, (1,2,2,1):u_inter, (1,3,3,1):u_inter } 
    mulst = {0:mu_L, 1:mu_L, 2:mu_R, 3:mu_R}
    tlst = {0:T_L, 1:T_L, 2:T_R, 3:T_R}

    #Från series till parallel!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #series: omega = 1, tL* = 0:   lamda = 0
    #parallel: omega = 0, tL* = 1:  lamda = 1
    #lmda : 0 -> 1

    I = np.zeros((len(lamdas),len(epsilons)))
    I_var = np.zeros((len(lamdas),len(epsilons)))
    J_QH = np.zeros((len(lamdas),len(epsilons)))

    for l_idx, lmda in enumerate(lamdas):
        for e_idx, eps in enumerate(epsilons):
            system = qmeq.Builder(nsingle=n, hsingle={(0,0):eps, (1,1):eps, (2,2):eps+1, (3,3):eps+1, (0,2):(1-lmda)*omega, (1,3):(1-lmda)*omega}, coulomb=U, nleads=nleads,
                            mulst=mulst, tlst=tlst, tleads={(0, 0):tL, (1, 1):tL, (2, 2):tR, (3, 3):tR, (0,2):lmda*tL, (1,3):lmda*tL, (2,0):lmda*tR, (3,1):lmda*tR},
                            dband=1e4, countingleads=[0,1], kerntype='pyLindblad')
            system.solve()
            if system.current_noise[1] < 0:
                warnings.warn(f"Warning! Negative noise! {system.current_noise[1]} for lambda: {lmda} and epsilon: {eps}")
            I[l_idx, e_idx] = system.current_noise[0]
            I_var[l_idx, e_idx] = system.current_noise[1]
            J_QH[l_idx, e_idx] = system.heat_current[0]+system.heat_current[1]


    #====================Pruning========================
    I[(I < 0) | (J_QH < 0)] = np.nan
    I_var[np.isnan(I)] = np.nan
    J_QH[np.isnan(I)] = np.nan

    #Calculations of P, efficiency, sigma and TUR

    P = I*V_B
    eff_carnot = 1-(T_COLD/T_HOT)
    eff = P/J_QH
    sigma = P*(1/T_COLD)*(eff_carnot-eff)/eff
    TUR = I_var*sigma/(I**2)

    return I, I_var, J_QH, P, eff, sigma, TUR

if __name__ == "__main__":
    epsilons = np.linspace(-500, 500, 10)
    omega = 0.1
    u_intra = 200
    u_inter = 100
    V_B = 90     
    gammaL = 0.1
    gammaR = gammaL
    T_L = 4
    T_R = 1
    run_interpolation(epsilons, omega, u_intra, u_inter, V_B, gammaL, gammaR, T_L, T_R)