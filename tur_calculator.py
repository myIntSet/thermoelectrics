import numpy as np

def calculate_tur(T_L, T_R, I, I_var, J_QH, P):

    if T_L < T_R:
        raise SystemExit("Not my convention! (T_L < T_R)")
    elif T_L > T_R:
        T_COLD = T_R
        T_HOT = T_L
    #elif T_L == T_R:
    I_TUR = I.copy()
    P_TUR = P.copy()
    I_var_TUR = I_var.copy()
    J_QH_TUR = J_QH.copy()

    #Remove values that won't generate a TUR (not a heat engine, or numerical negative noise issue)
    P_TUR[(P < 0) | ((I_var < 0) & (np.abs(I_var) < 1e-16)) | ((J_QH < 0) & ((np.abs(J_QH) < 1e-14)))] = np.nan
    I_TUR[np.isnan(P)] = np.nan
    I_var_TUR[np.isnan(P)] = np.nan
    J_QH_TUR[np.isnan(P)] = np.nan


    #Calculations of efficiency, sigma and TUR
    eff_carnot = 1-(T_COLD/T_HOT)
    eff = P_TUR/J_QH_TUR
    #print(np.sort(P))
    #print(np.sort(J_QH))
    sigma = P_TUR*(1/T_COLD)*(eff_carnot-eff)/eff
    TUR = I_var_TUR*sigma/(I_TUR**2)
    return TUR, eff_carnot, eff, sigma