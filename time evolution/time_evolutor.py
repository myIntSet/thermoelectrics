import sys
sys.path.append('/../../QmeQ/qmeq/')
import qmeq

from scipy.linalg import eig, eigvals
import numpy as np



def calculate_meta(initial, ti_array, eps, omega, u_intra, u_inter, V_B, gammaL, gammaR, T_L, T_R):

    if T_L < T_R:
        raise SystemExit("Not my convention! (T_L < T_R)")
    elif T_L > T_R:
        T_COLD = T_R
        T_HOT = T_L
    #elif T_L == T_R:
    #    raise SystemExit("Not a heat engine (T_L = T_R)")
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


    sys = qmeq.Builder(nsingle=n, hsingle={(0,0):eps, (1,1):eps, (2,2):eps, (3,3):eps, (0,2):0*omega, (1,3):0*omega}, coulomb=U, nleads=nleads,
                    mulst=mulst, tlst=tlst, tleads={(0, 0):tL, (1, 1):tL, (2, 2):tR, (3, 3):tR, (0,2):0.9*tL, (1,3):0.9*tL, (2,0):0.9*tR, (3,1):0.9*tR},
                    dband=1e4, countingleads=[0,1], kerntype='pyLindblad')
    sys.solve()

    liouvillian, dim, eval_j, left_ev, right_ev = base_calculations(sys)
    print('dim', dim)
    
    rho_ss, rho_t = time_evolution(left_ev, right_ev, eval_j, initial, liouvillian, ti_array, dim)

    # -----------------------------PARTICLE CURRENT-------------------------------------

    # qmeq solution for stationary current (summed over left lead)
    I_ss = sys.current[0]+sys.current[1]
    print('I_ss: ', I_ss)
    print('right lead? ', sys.current[2]+sys.current[3])

    I_qmeq_tot = np.zeros((nleads,ti_array.shape[0]))
    J_QH_tot = np.zeros((nleads,ti_array.shape[0]))
    I = np.zeros((ti_array.shape[0]))
    I_var = np.zeros((ti_array.shape[0]))


    for i in range(ti_array.shape[0]):
        
        # reset current    
        sys.current[:] = np.zeros(nleads)
        
        # set stationary state to rho_t value
        sys.phi0[:] = np.real(rho_t[:,i])
        
        # calculate current (also calculates energy and heat currents)
        sys.appr.generate_current() # calculates current both ways
        I_qmeq_tot[:,i] = sys.current #for verification
        J_QH_tot[:,i] = sys.heat_current
        I[i] = sys.current_noise[0] 
        I_var[i] = sys.current_noise[1]
        
        #--------------------------------------------

    # sum up heat and QmeQ current at left lead   
    J_QH = J_QH_tot[0] + J_QH_tot[1]
    I_qmeq = I_qmeq_tot[0] + I_qmeq_tot[1]

    return sys, rho_ss, rho_t, I_ss, I_qmeq, J_QH, I, I_var
    

def time_evolution(left_ev, right_ev, eval_j, initial, liouvillian, ti_array, dim):
    # calculate stationary state from left/right eigenvectors
    rho_ss = 1/np.dot((left_ev[:,0]),right_ev[:,0]) * np.dot(np.conjugate(left_ev[:,0]), initial) * right_ev[:,0]


    rho_t = np.zeros((dim,ti_array.shape[0])) + 0j

    # calculate elements and perform sum
    for i in range(dim-1):
        norm = np.dot(np.conjugate(left_ev[:,i+1]),right_ev[:,i+1])
        rho_t += 1/norm * np.dot(np.conjugate(left_ev[:,i+1]), initial) * np.exp(eval_j[i+1] *  ti_array[None,:]) * right_ev[:,i+1,None] 

    #add stationary state    
    rho_t = rho_t + rho_ss[:,None]

    return rho_ss, rho_t


def base_calculations(sys):
        #Get Liouvillian
    liouvillian = sys.kern
    dim = liouvillian.shape[0]

    # calculate eigenvalues, left and right eigenvalues
    eval_j, left_ev, right_ev = eig(liouvillian, left = True) 

    # sort eigenvalues/eigenvectors
    idx = eval_j.argsort()[::-1]   
    eval_j = eval_j[idx]
    left_ev = left_ev[:,idx]
    right_ev = right_ev[:,idx] 

    #check normalization
    result = np.zeros((dim,dim)) + 0j

    for j in range(dim):
        for k in range(dim):
            result[j,k] = np.dot(np.conjugate(left_ev[:,j]),right_ev[:,k])
            # normalization to 1
            if j == k:
                result[j,k] = result[j,k]/np.dot(np.conjugate(left_ev[:,j]),right_ev[:,k])
                
    print(str(np.round(np.real(result),1)))

    #print('check l1 is identity:', np.real(np.round(left_ev[:,0],3)))

    return liouvillian, dim, eval_j, left_ev, right_ev


def calculate_single_res(initial, ti_array, eps, mu_L, mu_R, T_L, T_R, gammaL, gammaR):

    n = 1 #single resonant energy level
    nleads = 2
    mulst = {0:mu_L, 1:mu_R}
    tlst = {0:T_L, 1:T_R}
    tL = np.sqrt(gammaL/np.pi/2)
    tR = np.sqrt(gammaR/np.pi/2)
    tleads = {(0, 0):tL, (1, 0):tR}

    sys = qmeq.Builder(nsingle=n, hsingle={(0,0):eps}, nleads=nleads,
                        mulst=mulst, tlst=tlst, tleads=tleads, dband=1e4, countingleads=[0], kerntype='pyPauli')

    # make sure the kernel does not get overwritten
    sys.make_kern_copy = True

    sys.solve()

    liouvillian, dim, eval_j, left_ev, right_ev = base_calculations(sys)

    rho_ss, rho_t = time_evolution(left_ev, right_ev, eval_j, initial, liouvillian, ti_array, dim)

    # PARTICLE CURRENT

    # qmeq solution for stationary current 
    I_ss = sys.current

    I_t_qmeq = np.zeros((nleads,ti_array.shape[0]))
    I_t_CF = np.zeros((ti_array.shape[0]))


    for i in range(ti_array.shape[0]):
        
        # reset current    
        sys.current[:] = np.zeros(nleads)
        
        # set stationary state to rho_t value
        sys.phi0[:] = np.real(rho_t[:,i])
        
        # calculate current (also calculates energy and heat currents)
        sys.appr.generate_current() # calculates current both ways
        I_t_qmeq[:,i] = sys.current
        I_t_CF[i] = sys.current_noise[0] 
        
        #--------------------------------------------

    # current at left and right lead    
    IL_t_qmeq = I_t_qmeq[0]
    IR_t_qmeq = I_t_qmeq[1]

    return sys, rho_ss, rho_t, I_ss, IL_t_qmeq, IR_t_qmeq, I_t_CF