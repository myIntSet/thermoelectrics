import numpy as np
import matplotlib.pyplot as plt



T = 1
e = 1
#(kb = 1)
gamma_L = 0.3
gamma_R = gamma_L

'''
def fermi(mu, E):
    if E > mu:
        return 0
    elif E < mu: 
        return 1
    elif E == mu:
        return 0.5
'''

def fermi(mu, E):
    return 1/(1+np.exp((E-mu)/T))

def calculate_current(epsilon, V_B):
    mu_L = -V_B/2
    mu_R = V_B/2

    W_1_0 = gamma_L*fermi(mu_L, epsilon)+gamma_R*fermi(mu_R, epsilon)
    W_0_1 = gamma_L*(1-fermi(mu_L, epsilon))+ gamma_R*(1-fermi(mu_R, epsilon))
    Wsum = W_0_1 + W_1_0
    P_0 = W_0_1/Wsum
    P_1 = W_1_0/Wsum

    I = -e*(gamma_R*fermi(mu_R, epsilon)*P_0 - gamma_R*(1-fermi(mu_R, epsilon))*P_1)
    return I
    #return P_0, P_1
    

def main():
    # Define the range and number of points for the two parameters

    epsilon_vals = np.linspace(-100, 100, 100)  # Adjust the range and number of points as needed
    V_B_vals = np.linspace(-100, 100, 100)

    # Create a mesh grid
    epsilon, V_B = np.meshgrid(epsilon_vals, V_B_vals)

    I = calculate_current(epsilon, V_B)

    #P_0, P_1 = calculate_current(epsilon, V_B)

    plt.figure(figsize=(8, 6))
    # Create a contour plot (or a pcolormesh plot for a smooth color gradient)
    contour = plt.contourf(epsilon, V_B, I, 20, cmap='vanimo')  # Adjust number of contour levels as needed
    #contour = plt.contourf(epsilon, V_B, I, 20, cmap='viridis')
    # Add color bar
    plt.colorbar(contour)

    # Label the axes
    plt.xlabel('epsilon')
    plt.ylabel('V_B')

    # Title of the plot
    plt.title('Current for different values of V_B and epsilon')

    # Show the plot
    plt.show()
    

def main2():
    epsilons = np.linspace(-100, 100, 100)
    ns = fermi(-25, epsilons)
    plt.plot(epsilons, ns)
    plt.show()

if __name__ == "__main__":
    #V_B = 3
    #epsilon = 1
    #P_0, P_1 = calculate_current(V_B, epsilon)
    #print(P_0+P_1)
    main()
    #main2()