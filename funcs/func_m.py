import numpy as np
import matplotlib.pyplot as plt
import sys
import os
from matplotlib import cbook
plt.style.use('tableau-colorblind10')

# ---------- Functions ----------
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# ---------- Variables ----------
titles = np.array([])  # empty array for titles of processes
m_values = np.array([])  # empty array for masses
c_values = np.array([])  # empty array for couplings

hist_name = "" # histogram values come from

funcs = {} # empty dictionary for functions

# ---------- Command Line Arguments ----------
if ( len(sys.argv) < 1 ): # less than three command line arguments
    print("Not correct number of command line arguments")
    quit()

dir = sys.argv[1] # path

# ---------- output files
r_file = "res"
res_file = open(r_file, "w")

# ---------- Read through files ----------
file_i = 0
for file in os.listdir(dir):
    if ".dat" in file and "res" not in file:
        in_file = open(file, "r")
        lines = in_file.readlines()

        t_file = file.replace("_tot","").replace(".dat","")
        titles = np.append(titles,t_file)

        for line in lines:
            line = line.replace('\n', '')

            if ".dat" in line: # histogram
                if hist_name == "":
                    hist_name = line
                else:
                    if hist_name != line:
                        print("Error data not from same histogram")
                        exit()
                    else:
                        continue
            elif "Mass" in line: # mass value
                a_line = line.split(": ")
                m = float(a_line[1])

                if file_i == 0:
                    if m not in m_values:
                        m_values = np.append(m_values,m)
                else:
                    if m not in m_values:
                        print("Error not the same masses")
                        exit()
            elif "g_values" in line: # coupliong values
                a_line = line.replace(":","").split(" ")

                if file_i == 0:
                    g_values = np.array([ float(g) for g in a_line if isfloat(g) ])
                else:
                    g_temp = np.array([ float(g) for g in a_line if isfloat(g) ])
                    if g_temp.all() != g_values.all():
                        print("Error not the same couplings")
                        exit()

            elif "*g**" in line: # function of coupling
                a_line = line.split("*g**")

                if t_file in funcs:
                    funcs[t_file] = np.append(funcs[t_file],a_line)
                else:
                    funcs[t_file] = np.array([a_line])

        funcs[t_file] = np.reshape(funcs[t_file],(int(len(funcs[t_file])/2),2))

        in_file.close()
    else:
        continue

    file_i += 1

n_m = len(m_values)
n_g = len(g_values)

y_max = 0
y_values = {}
for title in titles:
    y_values[title] = np.array([ float(funcs[title][i][0])*g_values**(float(funcs[title][i][1])) for i in range(0,n_m) ])

    temp = [ max(y_values[title][i]) for i in range(0,n_m) ]
    if max(temp) > y_max:
        y_max = max(temp)

# ---------- Plotting ----------
print("------ Plotting ------")
# ---------- Variables
plot_file = "tot.png"

# --- plot 1: Function
n_i = 3
fig1, ax1 = plt.subplots(3,3)
for i in range(0,n_m):
    res_file.write("Mass: " + str(m_values[i]) + "\n")

    idx = int((m_values[i]-1)/3)
    idy = int((m_values[i]-1)%3)

    if ".0" in str(m_values[i]):
        iter = 0
        data = np.array([])

        zax = ax1[idx,idy].inset_axes([0.5, 0.5, 0.5, 0.5])
        for title in titles:
            if title != "both":
                res_file.write(title+" ")
                data = np.append(data,y_values[title][i])
                ax1[idx,idy].plot(g_values,y_values[title][i],label=title)
                ax1[idx,idy].set_title(str(m_values[i])+" GeV",fontsize=7)

                # zoomed in
                zax.plot(g_values[0:n_i],y_values[title][i][0:n_i],label=title)
                zax.grid(True)

                #zax.set_xlim([g_values[0],g_values[n_i]])
                zax.set_xticklabels([])
                zax.xaxis.set_tick_params(width=0.5)

                zax.set_ylim([min(y_values[title][i][0:n_i]),max(y_values[title][i][0:n_i])])
                zax.set_yticklabels([])
                zax.yaxis.set_tick_params(width=0.5)

                ax1[idx,idy].indicate_inset_zoom(zax, edgecolor="black")

            iter += 1
        res_file.write("\n")
        
        data = np.reshape(data,(2,int(len(data)/2)))

        intersections = np.argwhere(np.diff(np.sign(data[0] - data[1]))).flatten()

        if len(intersections) != 0:
            print("test")
        else:
            if (data[0] - data[1])[0] > 0: # first bigger than second
                res_file.write("0 \n")
            elif (data[0] - data[1])[0] < 0: # second bigger than first
                res_file.write("1 \n")

for i in range(0,3):
    for j in range(0,3):
        lab = ax1[i][j].get_yticks()
        ax1[i][j].set_yticklabels([np.format_float_scientific(lab_el, unique=False, precision=1) for lab_el in lab],fontsize=7)
        ax1[i,j].grid(True)
        #ax1[i][j].set_yticklabels(lab,fontsize=7)

    # x axis
    ax1[2,i].set_xlabel("$f_a$",fontsize=7)
    ax1[0][i].set_xticklabels([])
    ax1[1][i].set_xticklabels([])
    lab = ax1[2][i].get_xticks()
    ax1[2][i].set_xticklabels([np.format_float_scientific(lab_el, unique=False, precision=1) for lab_el in lab],fontsize=7)
    #ax1[2][i].set_xticklabels(ax1[2][i].get_xticks(),fontsize=7)

    # y axis
    ax1[i,0].set_ylabel("# Events",fontsize=7)

fig1.suptitle("Total Number of Events", x=0.1, y=0.97)
ax1[0,2].legend(loc='upper right',bbox_to_anchor=(1.0, 1.5), ncol=2)
fig1.subplots_adjust(left=0,wspace=0.4,hspace=0.25)
fig1.savefig(plot_file, bbox_inches='tight', dpi=250)

res_file.close()