import sys
sys.path.append('/../../QmeQ/qmeq/')
import qmeq

from scipy.linalg import eig, eigvals
import numpy as np

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

    #check/normalize
    result = np.zeros((dim,dim)) + 0j

    for j in range(dim):
        for k in range(dim):
            result[j,k] = np.dot(np.conjugate(left_ev[:,j]),right_ev[:,k])
            # normalization to 1
            if j == k:
                result[j,k] = result[j,k]/np.dot(np.conjugate(left_ev[:,j]),right_ev[:,k])
                
    print(str(np.round(np.real(result),1)))

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

    #-------------------------------------FULL TIME EVOLUTION:-------------------------------------------------
    # calculate stationary state from left/right eigenvectors
    rho_ss = 1/np.dot((left_ev[:,0]),right_ev[:,0]) * np.dot(np.conjugate(left_ev[:,0]), initial) * right_ev[:,0]


    #dimension
    dim = liouvillian.shape[0]

    rho_t = np.zeros((dim,ti_array.shape[0])) + 0j

    # calculate elements and perform sum
    for i in range(dim-1):
        norm = np.dot(np.conjugate(left_ev[:,i+1]),right_ev[:,i+1])
        rho_t += 1/norm * np.dot(np.conjugate(left_ev[:,i+1]), initial) * np.exp(eval_j[i+1] *  ti_array[None,:]) * right_ev[:,i+1,None] 

    #add stationary state    
    rho_t = rho_t + rho_ss[:,None]
    #--------------------------------------------------------------------------------------------------------------

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