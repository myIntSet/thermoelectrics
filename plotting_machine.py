import numpy as np
import matplotlib.pyplot as plt


def plot_all(epsilons, VBs, I, I_var, P, J_QH, sigma, TUR):

    def plot_single(fig, axes, i, j, Y, title):
        if title == 'TUR':
            Y = np.ma.masked_where(Y >= 2, Y)
        elif title == 'P':
            Y = np.ma.masked_where(Y <= 0, Y)
        img = axes[i,j].imshow(Y, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower')
        fig.colorbar(img, ax=axes[i,j])
        axes[i,j].set_title(title)
        axes[i,j].set_xlabel('epsilon')
        axes[i,j].set_ylabel('V')

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 8))

    values = [I, I_var, P, J_QH, sigma, TUR]
    titles = ['Current', 'Noise', 'P', 'Heat current', 'sigma', 'TUR']
    plt_idx = 0
    for i in range(0,2):
        for j in range(0,3):
            plot_single(fig, axes, i, j, values[plt_idx], titles[plt_idx])
            plt_idx += 1

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.suptitle("Zoomed in region", fontsize=16, fontweight='bold')
    plt.show()

    '''
    # Plot on different subplots using the axes array
    img = axes[0,0].imshow(I, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower')
    fig.colorbar(img, ax=axes[0,0]) 
    axes[0,0].set_title("Current")
    axes[0,0].set_xlabel('epsilon')
    axes[0,0].set_ylabel('V')
    #img.set_clim(-0.1, 0.1)  # Set color limits

    img = axes[0,1].imshow(I_var, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower')
    fig.colorbar(img, ax=axes[0,1]) 
    axes[0,1].set_title("Noise")
    axes[0,1].set_xlabel('epsilon')
    axes[0,1].set_ylabel('V')

    fig.suptitle("CZoomed in region", fontsize=16, fontweight='bold')
    # Adjust layout to prevent overlap
    #plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leaves space for suptitle
    '''

def plot_one(Y):
    pass