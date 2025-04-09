import numpy as np
import matplotlib.pyplot as plt

def plot_fermi_function(epsilons, mu, T, ax, title):
    
    def fermi(mu, E, T):
        return 1/(1+np.exp((E-mu)/T))

    # Second plot - Fermi function in Left lead
    fermi = fermi(mu, epsilons, T)
    ax.plot(fermi, epsilons)
    ax.axhline(y=mu, color='r', linestyle='--', label=f'μ = {mu}') 
    ax.set_xlabel('Fermi Function Value')
    ax.set_title(title)

def plot_qd_level(epsilons, eps, ax, title):
    ax.plot(epsilons, epsilons, color='white')
    ax.axhline(eps)
    ax.set_title(title)

def plot_rho(ti_array, rho_t, sys, eps, V_B, T_L, T_R):
    epsilons = np.linspace(-25,25,100)
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(18, 6), gridspec_kw={'width_ratios': [10, 3, 2, 3]}) 

    rho_0, rho_1, rho_2, rho_3, rho_4, rho_0_ss, rho_1_ss, rho_2_ss, rho_3_ss, rho_4_ss = get_rho(rho_t, sys)

    ax1.plot(ti_array, np.real(rho_0), label = r'$\rho_{0}$')
    ax1.plot(ti_array[-1],rho_0_ss, '>',color = 'C0')

    ax1.plot(ti_array, np.real(rho_1), label = r'$\rho_{1}$')
    ax1.plot(ti_array[-1],rho_1_ss, '>',color = 'C1')

    ax1.plot(ti_array, np.real(rho_2), label = r'$\rho_{2}$')
    ax1.plot(ti_array[-1],rho_2_ss, '>',color = 'C2')

    ax1.plot(ti_array, np.real(rho_3), label = r'$\rho_{3}$')
    ax1.plot(ti_array[-1],rho_3_ss, '>',color = 'C3')

    ax1.plot(ti_array, np.real(rho_4), label = r'$\rho_{4}$')
    ax1.plot(ti_array[-1],rho_4_ss, '>',color = 'C4')

    ax1.legend()

    ax1.set_xlabel(r'time $t$')
    ax1.set_ylabel(r'$\rho(t)$')

    mu_L = -V_B/2       
    mu_R = V_B/2 

    plot_fermi_function(epsilons, mu_L, T_L, ax2, "Fermifunction of the left lead")
    plot_qd_level(epsilons, eps, ax3, "QD level")
    plot_fermi_function(epsilons, mu_R, T_R, ax4, "Fermifunction of the right lead")

    plt.show()

def get_rho(rho_t, sys):
    rho_0 = rho_t[0]
    rho_1 = rho_t[1]+rho_t[2]+rho_t[3]+rho_t[4]
    rho_2 = rho_t[5]+rho_t[6]+rho_t[7]+rho_t[8]+rho_t[9]+rho_t[10]
    rho_3 = rho_t[11]+rho_t[12]+rho_t[13]+rho_t[14]
    rho_4 = rho_t[15]

    rho_0_ss = sys.phi0[0]
    rho_1_ss = sys.phi0[1]+sys.phi0[2]+sys.phi0[3]+sys.phi0[4]
    rho_2_ss = sys.phi0[5]+sys.phi0[6]+sys.phi0[7]+sys.phi0[8]+sys.phi0[9]+sys.phi0[10]
    rho_3_ss = sys.phi0[11]+sys.phi0[12]+sys.phi0[13]+sys.phi0[14]
    rho_4_ss = sys.phi0[15]

    return rho_0, rho_1, rho_2, rho_3, rho_4, rho_0_ss, rho_1_ss, rho_2_ss, rho_3_ss, rho_4_ss