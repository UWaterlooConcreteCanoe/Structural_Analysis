import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import _canoeValues as cv
import math
import time

#-------------------Inputs-------------------------------------------------------------
script = "Longitudinal Analysis_2 Paddler.ipynb"
input_file = "Station Information.csv"
outerHull_file = "Outer Hull.csv" # Will be used for hydrostatic force and waterline calculation
DLF = cv.DLF # Dead Load Factor
LLF = 1.3 # Live Load Factor
pad_weights = cv.pad_weights # Weight of paddlers (kg)
water_den = cv.water_density # Density of water = 1000 kg/m^3
#--------------------------------------------------------------------------------------
# Acquire the waterline from Grasshopper
grasshopper = cv.grasshopper[0] # [mm]

pad1_pos = 1710 # Position of first paddler with respect to left end of canoe (mm)
pad2_pos = 4100 # Position of second paddler with respect to left end of canoe (mm)
# Choose between pad_weights
pad_first = pad_weights[3]
pad_second = pad_weights[3]
# Apply the Live Load Factor (constsant)
pad1 = pad_first * LLF
pad2 = pad_second * LLF
#--------------------------------------------------------------------------------------

script_dir = os.path.abspath('data') # absolute file path in Jupyter
file_path = "/Users/kiranprsd/Projects/Clubs/ConcreteCanoe/Structural_Analysis/data/Station Information.csv"

# Get the canoe's volume and mass from the station info
canoe_info = pd.read_csv(file_path, header=None)
statVol = canoe_info[1][1:]
statMass = canoe_info[2]

# Get the outer hull coordinates from the input file
file_path = "/Users/kiranprsd/Projects/Clubs/ConcreteCanoe/Structural_Analysis/data/Outer Hull.csv"
out_coor = pd.read_csv(file_path, header=None)
x_out = out_coor[0]
y_out = out_coor[1]
z_out = out_coor[2]

# Get the mass and volume at each station from the Station Information csv file (exported from Approximation-Vol Diff)
stat_Mass = []
for i in range(1,len(statMass),1):
    stat_Mass.append(float(statMass[i]))
    
stat_Vol = []
for i in range(1,len(statVol),1):
    stat_Vol.append(float(statVol[i]))

canoe_volume = np.sum(stat_Vol) # m^3
canoe_mass = np.sum(stat_Mass)*DLF # [kg]
total_mass = canoe_mass + pad1 + pad2 # [kg]

station_no = x_out.nunique() # number of stations
station = x_out.unique() # location of each station

def center_of_mass():
    # Calculate Centre of Mass
    stations_mm = [x * float(canoe_info[4][1]) for x in range(0,station_no-1)]

    mass_sum = 0
    for i in range(len(station)-1):
        mass_sum += stat_Mass[i] * stations_mm[i]
        
    mass_sum += pad1 * pad1_pos + pad2 * pad2_pos

    centre_of_mass = mass_sum / (sum(stat_Mass) + pad1 + pad2)

    return centre_of_mass # mm