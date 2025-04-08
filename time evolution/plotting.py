import numpy as np
import matplotlib.pyplot as plt

def plot_fermi_function(epsilons, mu, T, ax, title):
    
    def fermi(mu, E, T):
        return 1/(1+np.exp((E-mu)/T))

    # Second plot - Fermi function in Left lead
    fermi = fermi(mu, epsilons, T)
    print('fermi: ',fermi.shape)
    print('epsilons: ', epsilons.shape)
    ax.plot(fermi, epsilons)
    ax.axhline(y=mu, color='r', linestyle='--', label=f'μ = {mu}') 
    ax.set_xlabel('Fermi Function Value')
    ax.set_title(title)

def plot_qd_level(epsilons, eps, ax, title):
    ax.plot(epsilons, epsilons, color='white')
    ax.axhline(eps)
    ax.set_title(title)