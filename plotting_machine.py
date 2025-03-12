import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset


def plot_all(epsilons, VBs, I, I_var, P, J_QH, sigma, TUR, title):

    def plot_single(fig, axes, i, j, Y, title):
        if title == 'TUR < 2':
            Y = np.ma.masked_where(Y >= 2, Y)
        elif title == 'P > 0':
            Y = np.ma.masked_where(Y <= 0, Y)
        img = axes[i,j].imshow(Y, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower')
        fig.colorbar(img, ax=axes[i,j])
        axes[i,j].set_title(title)
        axes[i,j].set_xlabel('epsilon')
        axes[i,j].set_ylabel('V')

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 8))

    values = [I, I_var, P, J_QH, sigma, TUR]
    titles = ['Current', 'Noise', 'P > 0', 'Heat current', 'sigma', 'TUR < 2']
    plt_idx = 0
    for i in range(0,2):
        for j in range(0,3):
            plot_single(fig, axes, i, j, values[plt_idx], titles[plt_idx])
            plt_idx += 1

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.show()

def plot_one(Y):
    pass

def plot_zoomed_out(epsilons, VBs, Y1, title1, Y2, title2, epsilons_zoom, VBs_zoom, Y1_zoom, Y2_zoom, suptitle):

    # Create Figure
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(16, 5))
    print(VBs[-1])

    # Main imshow plot
    img = axes[0].imshow(Y1, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower')
    fig.colorbar(img, ax=axes[0])
    axes[0].set_title(title1)
    axes[0].set_xlabel(r"$\epsilon$")
    axes[0].set_ylabel('$V_B$')

    # Define zoom area (e.g., focus on a small square region)
    eps_min, eps_max = epsilons_zoom[0], epsilons_zoom[-1]   #0, 2.1  # Epsilon range
    v_min, v_max = VBs_zoom[0], VBs_zoom[-1] #-0.5, 0.5  # V range

    inset_width = 0.3  # 30% of the parent axes
    inset_height = inset_width * (v_max - v_min) / (eps_max - eps_min)  # Maintain aspect ratio
    axins = inset_axes(axes[0], width=f"{inset_width*100}%", height=f"{inset_height*100}%", loc="upper right")
    img_zoom = axins.imshow(Y1_zoom, extent=[eps_min, eps_max, v_min, v_max], aspect='auto', origin='lower')
    axins.set_xticks([])  # Remove ticks for clarity
    axins.set_yticks([])

    # Mark the zoomed region with a rectangle
    axes[0].plot([eps_min, eps_max, eps_max, eps_min, eps_min], [v_min, v_min, v_max, v_max, v_min], 'r-', linewidth=2)
    # Connect main plot and inset with lines
    mark_inset(axes[0], axins, loc1=2, loc2=4, fc="none", ec="red")

    img = axes[1].imshow(Y2, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower')
    fig.colorbar(img, ax=axes[1]) 
    axes[1].set_title(title2)
    axes[1].set_xlabel(r"$\epsilon$")
    axes[1].set_ylabel('$V_B$')

    inset_width = 0.3  # 30% of the parent axes
    inset_height = inset_width * (v_max - v_min) / (eps_max - eps_min)  # Maintain aspect ratio
    axins = inset_axes(axes[1], width=f"{inset_width*100}%", height=f"{inset_height*100}%", loc="upper right")
    img_zoom = axins.imshow(Y2_zoom, extent=[eps_min, eps_max, v_min, v_max], aspect='auto', origin='lower')

    axins.set_xticks([])  # Remove ticks for clarity
    axins.set_yticks([])
    axes[1].plot([eps_min, eps_max, eps_max, eps_min, eps_min], [v_min, v_min, v_max, v_max, v_min], 'r-', linewidth=2)
    mark_inset(axes[1], axins, loc1=2, loc2=4, fc="none", ec="red")

    fig.suptitle(suptitle, fontsize=16, fontweight='bold')
    plt.show()