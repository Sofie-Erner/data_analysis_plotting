import matplotlib.pyplot as plt # import matplotlib
import numpy as np
import sys
plt.style.use('tableau-colorblind10') # make plots colour-blind friendly 

# ---------- Command Line Arguments ----------
if ( len(sys.argv) < 2 ): # less than three command line arguments
    print("Not correct number of command line arguments")
    quit()

file_input = sys.argv[1] # file to read from

# ---------- Variables ----------
m_values = np.array([]) # array for mass values
c_values = np.array([]) # array for coupling values
titles = np.array([]) # array for titles
data = {} # dictionary for data for each mass value

# ---------- Read data file ----------
in_file = open("data.csv","r") # open in read mode
lines = in_file.readlines() # get lines from file

for line in lines: # loop over lines
    line = line.replace("\n","") # remove new-line character

    if "#" not in line: # don't want comment
        split_line = np.array(line.split("\t")) # split line by tab
    
        # first entry is the mass
        m = float(split_line[0]) # line is string

        if m not in m_values: # only add to list once
            m_values = np.append(m_values,m)

        # second entry is the coupling
        c = float(split_line[1]) # line is string

        if c not in c_values: # only add to list once
            c_values = np.append(c_values,c)

        title = str(m)+"_"+str(c) # title will be mass_coupling
        titles = np.append(titles,title) # add to tiles

        # all other entries are data points
        data_i = split_line[2:].astype(float) # splice data from mass value (convert to float)

        if data and len(data_i) != len(data[titles[0]]): # if dictionary is not empty
            #if there are not the same number of data point
            print("Error not same number of data points")
            exit()

        data[title] = data_i # add to dictionary

in_file.close() # close file

# ---------- Analysis ----------
n_m = len(m_values) # number of masses
n_c = len(c_values) # number of couplings
n_all = len(titles) # total number of entries ( = n_m * n_c)
n_d = len(data[titles[0]]) # number of data points

x_values = np.linspace(1,n_d,n_d)

# ----- Sort input parameters
m_list = np.arange(0,n_m) # will store the original position value of the masses
c_list = np.arange(0,n_c)

if not np.all(m_values[:-1] <= m_values[1:]): # if masses not in order
    print("m values not in order")

    # order the m_list values using the sorted mass values
    m_values, m_list = (np.array(x) for x in zip(*sorted(zip(m_values,m_list), key=lambda pair:pair[0]))) 

    titles_temp = titles.copy()
    # fix order of titles
    for i_m in range(0,n_m):
        titles[i_m*n_c:(i_m+1)*n_c] = [x for x in titles_temp[m_list[i_m]*n_c:(m_list[i_m]+1)*n_c] ]

if not np.all(c_values[:-1] <= c_values[1:]):
    print("c values not in order")

    # fix order of titles
    for i_m in range(0,n_m):
        titles[i_m*n_c:(i_m+1)*n_c] = [x for _, x in sorted(zip(c_values,titles[i_m*n_c:(i_m+1)*n_c]), key=lambda pair: pair[0])]

    c_values, c_list = (np.array(x) for x in zip(*sorted(zip(c_values,c_list), key=lambda pair:pair[0])))

data_sums = [ data[title].sum() for title in titles ] # array for the sum of data for each mass value

#print(titles)
#print(data_sums)

#  ----- Sort data
# as a function of mass
z_m = [] # structure for contour plot

# as a function of coupling constant
z_c = [] # structure for contour plot

# Arrange values to fit m and g structures
for i in range(0,n_all):
    if i > n_c and i > n_m:
        break
    else:
        if i < n_m: # constant mass, vary coupling
            z_m.append([ data_sums[c + i*n_c] for c in range(0,n_c) ])

        if i < n_m: # constant coupling, vary mass
            z_c.append([ data_sums[i + m*n_c] for m in range(0,n_m) ])

# make arrays into numpy array
z_c = np.array(z_c)
z_m = np.array(z_m)

# ---------- Plotting ----------
# --- plot 1: Contour Levels
fig1, ax1 = plt.subplots(1,1)
[X, Y] = np.meshgrid(m_values,c_values) # create grid of masses and couplings

z_step = (np.max(z_c)-np.min(z_c))/10.

levels = np.arange(np.min(z_c), np.max(z_c)+z_step, z_step)
im = ax1.contourf(X,Y,z_c, levels=levels) # plot grid and values
#ax1.clabel(im, inline = True, fontsize = 10)

#import matplotlib.cm as cm # matplotlib's color map library
#cpf = ax1.contourf(X,Y,z_c, len(levels), cmap=cm.Reds)

# Set all level lines to black
line_colors = ['black' for l in im.levels]

# Make plot and customize axes
cp = ax1.contour(X, Y, z_c, levels=levels, colors=line_colors)
ax1.clabel(cp, fontsize=10, colors=line_colors)
#plt.xticks([0,0.5,1])
#plt.yticks([0,0.5,1])
ax1.set_xlabel('X-axis')
_ = ax1.set_ylabel('Y-axis')

#plt.colorbar(im, label="Total", format='%.3e')
plt.colorbar(cp, label="Total", format='%.3e')

# --- plot 2: Sum as a function of mass
fig2, ax2 = plt.subplots(1,1)

# --- plot 3: Sum as a function of coupling
fig3, ax3 = plt.subplots(1,1) 

for i in range(0,n_all):
    if i > n_c and i > n_m: # above both
        break
    else:
        if n_m > 1 and i < n_c: # loop over coupling constants
            ax2.scatter(m_values,z_m[i], label="c= "+str("{:.1e}".format(c_values[i])))

        if n_c > 1 and i < n_m: # loop over masses
            ax3.scatter(c_values,z_c[i], label="m= "+str(m_values[i]))
                

# ----- set title, axses, etc.
fic_axes = [ax1,ax2,ax3]
figs = [fig1,fig2,fig3]

plot_titles = ["contour","total_m","total_c"] # names for saving plots
super_titles = ["Contour of Sum of Data","Sum of Data","Sum of Data"]

iter=0
for ax in fic_axes: # loop over plots
    # --- set super title
    figs[iter].suptitle(super_titles[iter])

     # --- set x-axis labels
    if ax in [ax1,ax2]:
        ax.set_xlabel("Mass")
    if ax in [ax3]:
        ax.set_ylabel("Coupling")

     # --- set y-axis labels
    if ax in [ax1]:
        ax.set_ylabel("Coupling")
    if ax in [ax2,ax3]:
        ax.set_ylabel("Sum of Data")

    # --- set legends#
    if ax in [ax2]:
        figs[iter].legend(loc='upper left',bbox_to_anchor=(0.125, 0.88))
    elif ax in [ax3]:
        figs[iter].legend()

    # --- add grid lines
    ax.grid(True) # add grid lines

    # --- save plot
    figs[iter].savefig(plot_titles[iter]+".png" , bbox_inches='tight', dpi=250)

    iter+=1