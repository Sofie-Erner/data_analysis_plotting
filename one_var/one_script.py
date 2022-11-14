import matplotlib.pyplot as plt # import matplotlib
import numpy as np
import sys
plt.style.use('tableau-colorblind10') # make plots colour-blind friendly 

# ---------- Command Line Arguments ----------
if ( len(sys.argv) < 2 ): # less than three command line arguments
    print("Not correct number of command line arguments")
    quit()

file_input = sys.argv[1] # file to read from
file_suff = file_input.replace("data_","").replace(".csv","") # remove part of input file name

# ---------- Variables ----------
m_values = np.array([]) # array for mass values
data = {} # dictionary for data for each mass value
data_sums = np.array([]) # array for the sum of data for each mass value
same_data_points = 0 # 0: same number of data points, 1: not

# ---------- Read data file ----------
in_file = open(file_input,"r") # open in read mode
lines = in_file.readlines() # get lines from file

for line in lines: # loop over lines
    line = line.replace("\n","") # remove new-line character

    if "#" not in line: # don't want comment
        split_line = np.array(line.split("\t")) # split line by tab
    
        # first entry is the mass
        m = float(split_line[0]) # line is string

        if m in m_values: # in case there are two of the same masses
            print("Error two masses are the same")
            exit()
        else: # add to array
            m_values = np.append(m_values,m)

        # all other entries are data points
        data_m = split_line[1:].astype(float) # splice data from mass value (convert to float)

        if data and len(data_m) != len(data[m_values[0]]): # if dictionary is not empty
            #if there are not the same number of data point
            same_data_points = 1

        data[m] = data_m # add to dictionary
        data_sums = np.append(data_sums, data_m.sum()) # add sum

in_file.close() # close file

# ---------- Analysis ----------
n_m = len(m_values) # number of masses

# ---------- Plotting ----------
# --- plot 1: Sum as a function of mass
fig1, ax1 = plt.subplots(1,1) 

ax1.scatter(m_values,data_sums)
ax1.set_title("Total")

# --- plot 2: data points for each mass
if same_data_points == 0: # same number of data points
    # one plot with all masses
    fig2, ax2 = plt.subplots(1,1)

    n_i = len(data[m_values[0]]) # number of data points
    x_values = np.linspace(1,n_i,n_i) # list for number of data points
    for m in m_values:
        ax2.scatter(x_values,data[m],label=m)
    
elif same_data_points == 1: # not the same number of data points
    # three individual plots
    fig2, ax2 = plt.subplots(1,3) # 3 subplots

    for i in range(0,n_m):
        m = m_values[i] # set mass

        n_i = len(data[m]) # number of data points
        x_values = np.linspace(1,n_i,n_i) # list for number of data points
        
        ax2[i].scatter(x_values,data[m])
        ax2[i].set_title("data for "+str(m))

        ax2[i].set_xlabel("Data Point Number")
        ax2[i].set_xticks(x_values)

        ax2[i].grid(True) # add grid lines

    ax2[0].set_ylabel("Data Values") # only add y-value to first subplot

    fig2.subplots_adjust(wspace=0.3) # move subplots away from each other
    fig2.savefig("individual_"+file_suff+".png" , bbox_inches='tight', dpi=250)


else: # other option??
    print("somehow there is a wrong value")
    exit()

# ----- set title, axses, etc.
if same_data_points == 0:
    fig_axes = [ax1,ax2]
    figs = [fig1,fig2]
else: # not figure 2
    fig_axes = [ax1]
    figs = [fig1]

plot_titles = ["total","individual"] # names for saving plots
super_titles = ["Sum of Data","Indivudial Data"]

iter=0
for ax in fig_axes: # loop over plots
    # --- set super title
    figs[iter].suptitle(super_titles[iter])

     # --- set x-axis labels
    if ax in [ax1]:
        ax.set_xlabel("Mass")
    if same_data_points == 0 and ax in [ax2]:
        ax.set_xlabel("Data Point Number")

     # --- set y-axis labels
    if ax in [ax1]:
        ax.set_ylabel("Sum of Data")
    if same_data_points == 0 and ax in [ax2]:
        ax.set_ylabel("Data Value")

    # --- set legends
    if same_data_points == 0 and ax in [ax2]:
        figs[iter].legend(loc='upper left',bbox_to_anchor=(0.125, 0.88))

    # --- add grid lines
    ax.grid(True) # add grid lines

    # --- save plot
    figs[iter].savefig(plot_titles[iter]+"_"+file_suff+".png" , bbox_inches='tight', dpi=250)

    iter+=1