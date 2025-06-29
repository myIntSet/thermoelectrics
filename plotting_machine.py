import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset


def plot_single_report(plt, epsilons, VBs, Y, title, cmap, vmin=None, vmax=None, plotting_TURs=False):
    text_font = 35
    plt.rcParams.update({'font.size': 20})  # Applies globally
    plt.figure(figsize=(8, 5))  # Optional: set figure size
    if title == r'$\Phi$' or plotting_TURs:
        Y = np.ma.masked_where(Y >= 2, Y)
    elif title == 'P':
        Y = np.ma.masked_where(Y <= 0, Y)
    img = plt.imshow(Y, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower', cmap=cmap, vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(img)
    if title == r'$J_{QH}$':
        #lamda0:
        #cbar.set_ticks([0.0015, 0.0010, 0.0005, 0.0000, -0.0005, -0.0010, -0.0015])
        #cbar.set_ticklabels(['> 0.0015', '0.0010', '0.0005', '0.0000', '-0.0005', '-0.0010', '< -0.0015'])
        #lamda1:
        cbar.set_ticks([0.005, 0.004, 0.002, 0.00, -0.002, -0.004, -0.005])
        cbar.set_ticklabels(['> 0.005', '0.004', '0.002', '0.00', '-0.002', '-0.004', '< -0.005'])
    actual_vmin, actual_vmax = img.get_clim()
    print('actual_vmin,', actual_vmin, actual_vmax)
    plt.title(title, fontsize=text_font)
    plt.xlabel(r'$\varepsilon$', fontsize=text_font)
    plt.ylabel('V', fontsize=text_font, labelpad=0)
    plt.show()

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

def plot_big_coulomb_report_cropped(epsilons, VBs, Y, title, epsilons_zoom, VBs_zoom, Y_zoom):

    # Create Figure

    #plt.figure(figsize=(8, 5))  # Optional: set figure size
    text_font = 16
    #plt.rcParams.update({'font.size': 16})  # Applies globally
    fig, ax = plt.subplots(figsize=(12, 4))

    # Main imshow plot
    img = ax.imshow(Y, extent=[epsilons[0], epsilons[-1], VBs[49], VBs[149]], aspect='auto', origin='lower', cmap='bwr')
    #ax.scatter(epsilons[10], VBs[50])
    fig.colorbar(img, ax=ax)
    ax.set_title(title, fontsize=text_font)
    ax.set_xlabel(r"$\epsilon$", fontsize=text_font)
    ax.set_ylabel('$V_B$', fontsize=text_font)

    # Define zoom area (e.g., focus on a small square region)
    eps_min, eps_max = epsilons_zoom[0], epsilons_zoom[-1]   #0, 2.1  # Epsilon range
    v_min, v_max = VBs_zoom[0], VBs_zoom[-1] #-0.5, 0.5  # V range

    inset_width = 0.21  # 30% of the parent axes
    inset_height = 1.4*inset_width * (v_max - v_min) / (eps_max - eps_min)  # Maintain aspect ratio
    axins = inset_axes(ax, width=f"{inset_width*100}%", height=f"{inset_height*100}%", loc="upper right")
    img_zoom = axins.imshow(Y_zoom, extent=[eps_min, eps_max, v_min, v_max], aspect='auto', origin='lower', cmap='bwr')
    axins.set_xticks([])  # Remove ticks for clarity
    axins.set_yticks([])

    # Mark the zoomed region with a rectangle
    ax.plot([eps_min, eps_max, eps_max, eps_min, eps_min], [v_min, v_min, v_max, v_max, v_min], 'r-', linewidth=2)
    # Connect main plot and inset with lines
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="red")
    plt.show()

def plot_big_coulomb_report(epsilons, VBs, Y, title, epsilons_zoom, VBs_zoom, Y_zoom):

    # Create Figure

    #plt.figure(figsize=(8, 5))  # Optional: set figure size
    #text_font = 18
    #plt.rcParams.update({'font.size': 16})  # Applies globally
    fig, ax = plt.subplots(figsize=(8, 5))

    # Main imshow plot
    img = ax.imshow(Y, extent=[epsilons[0], epsilons[-1], VBs[0], VBs[-1]], aspect='auto', origin='lower', cmap='bwr')
    fig.colorbar(img, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(r"$\epsilon$")
    ax.set_ylabel('$V_B$')

    # Define zoom area (e.g., focus on a small square region)
    eps_min, eps_max = epsilons_zoom[0], epsilons_zoom[-1]   #0, 2.1  # Epsilon range
    v_min, v_max = VBs_zoom[0], VBs_zoom[-1] #-0.5, 0.5  # V range

    inset_width = 0.3  # 30% of the parent axes
    inset_height = inset_width * (v_max - v_min) / (eps_max - eps_min)  # Maintain aspect ratio
    axins = inset_axes(ax, width=f"{inset_width*100}%", height=f"{inset_height*100}%", loc="upper right")
    img_zoom = axins.imshow(Y_zoom, extent=[eps_min, eps_max, v_min, v_max], aspect='auto', origin='lower', cmap='bwr')
    axins.set_xticks([])  # Remove ticks for clarity
    axins.set_yticks([])

    # Mark the zoomed region with a rectangle
    ax.plot([eps_min, eps_max, eps_max, eps_min, eps_min], [v_min, v_min, v_max, v_max, v_min], 'r-', linewidth=2)
    # Connect main plot and inset with lines
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="red")
    plt.show()

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

#I and I_var etc should be 1D-arrays
def plot_inter(lamdas, I, I_var, P, J_QH, sigma, TUR, title):

    def plot_single(fig, axes, i, j, Y, title):
        axes[i,j].plot(lamdas, Y)
        axes[i,j].set_title(title)
        axes[i,j].set_xlabel('lambda')
        axes[i,j].set_ylabel(title)

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 8))

    values = [I, I_var, P, J_QH, sigma, TUR]
    titles = ['Current', 'Noise', 'P', 'Heat current', 'sigma', 'TUR']
    plt_idx = 0
    for i in range(0,2):
        for j in range(0,3):
            plot_single(fig, axes, i, j, values[plt_idx], titles[plt_idx])
            plt_idx += 1

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.show()

#"ys should be list/tuple with two entrys and y_names containes the corresponding names"
def plot_two(x, x_name, ys, y_names, y_titles, title):

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 8))

    for i in range(0,2):
        axes[i].plot(x, ys[i], label=f"{y_names[i]}")
        axes[i].set_xlabel(x_name)
        axes[i].set_ylabel(y_names[i])
        axes[i].set_title(y_titles[i])
        axes[i].set_ylim(1.96, 2.05) #<------------------Hard coded line, remove when wanting other behaviour!

    
    fig.suptitle(title, fontsize=16, fontweight='bold')
    plt.show()

def plot_minimal_TUR_points(x, y):
    indices = np.arange(len(x))  # Indices for colormap

    # Create a figure
    fig, ax = plt.subplots()

    # Scatter plot with color gradient
    sc = ax.scatter(x, y, c=indices, cmap='viridis', edgecolor='black', s=50, zorder=3)

    # Connect points with a line
    ax.plot(x, y, color='gray', linestyle='dashed', alpha=0.7, zorder=2)

    # Add colorbar to show order
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label(r"<-- lower $\lambda$                        higher $\lambda$ -->")
    cbar.set_ticks([])  # Remove numbers

    # Labels
    ax.set_xlabel(r"$\epsilon$")
    ax.set_ylabel("$V_B$")
    ax.set_title(r"How the minimal TUR points change with $\lambda$")

    plt.show()