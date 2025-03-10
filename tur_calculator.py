import numpy as np

def calculate_tur(T_L, T_R, I, I_var, J_QH, P):

    if T_L < T_R:
        raise SystemExit("Not my convention! (T_L < T_R)")
    elif T_L > T_R:
        T_COLD = T_R
        T_HOT = T_L
    #elif T_L == T_R:

    #Calculations of efficiency, sigma and TUR
    eff_carnot = 1-(T_COLD/T_HOT)
    eff = P/J_QH
    P[(P < 0)] = np.nan
    sigma = P*(1/T_COLD)*(eff_carnot-eff)/eff
    TUR = I_var*sigma/(I**2)
    return TUR, eff_carnot, eff, sigma