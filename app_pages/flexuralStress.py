import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import _canoeValues as cv
import math

#-------------------Inputs-------------------------------------------------------------
input_files = ["Shear_and_Moment_6 Paddlers.csv", "Shear_and_Moment_4 Paddlers.csv", "Shear_and_Moment_3 Paddlers.csv", "Shear_and_Moment_2 Paddlers.csv", "Shear_and_Moment_Display_Stand.csv"]
moment_files = ["Length_vs_Moment_6 Paddler.csv", "Length_vs_Moment_4 Paddler.csv", "Length_vs_Moment_3 Paddler.csv", "Length_vs_Moment_2 Paddler.csv", "Length_vs_Moment_Display_Stand.csv", ]
inner_file = "Inner Hull.csv"
outer_file = "Outer Hull.csv"
compressive_strength = cv.compressive_strength # MPa
tensile_strength = cv.tensile_strength # MPa
#--------------------------------------------------------------------------------------

script_dir = os.path.abspath('data')

file_path = os.path.join(script_dir, inner_file) # file path for the text file input
in_coor = pd.read_csv(file_path, header=None)

file_path = os.path.join(script_dir, outer_file) # file path for the text file input
out_coor = pd.read_csv(file_path, header=None)

# Get inner and outer hull coordinates (station points)
x_in = in_coor[0]
y_in = in_coor[1]
z_in = in_coor[2]

x_out = out_coor[0]
y_out = out_coor[1]
z_out = out_coor[2]

station_no = x_out.nunique() # number of stations
station_out = x_out.unique() # location of each station
station_in = x_in.unique()

file_path = os.path.join(script_dir, "Station Information.csv")
canoe_info = pd.read_csv(file_path, header=None)
stations_mm = [x * float(canoe_info[4][1]) for x in range(1,station_no-2,1)]

print("Positive Moments for Every Station:\n")

# Store each paddler case's x and shear to recreate their shear force diagrams later
# PAD_CASE_STATIONS = []
# PAD_CASE_LENGTH = []
# PAD_CASE_MOMENT = []

# Store stresses for plotting
# stressTopByCase = []
# stressBottomByCase = []

def initialLoop(moment_files):
    PAD_CASE_STATIONS = []
    PAD_CASE_LENGTH = []
    PAD_CASE_MOMENT = []

    stressTopByCase = []
    stressBottomByCase = []


    resistanceCompTopArrays = []
    resistanceCompBottomArrays = []
    resistanceTensTopArrays = []
    resistanceTensBottomArrays = []

    # Loop through each load case
    for input_file in moment_files:
        print("\033[4m" + input_file + ":\033[0m")

        # Get the moments for each station from the file
        file_path = os.path.join(script_dir, input_file)
        momentByLength = pd.read_csv(file_path, header=None)
        momentArray = []
        for i in range(len(station_in)):
            momentArray.append(momentByLength[2][i * round(len(momentByLength[0])/len(station_in)) + 1])

        # Store each paddler case's x and shear to recreate their BMDs later
        PAD_CASE_STATIONS.append(momentByLength[0][1:])
        PAD_CASE_LENGTH.append(momentByLength[1][1:])
        PAD_CASE_MOMENT.append(momentByLength[2][1:])

        # Initialize arrays to store top and bottom resistance (compressive & tensile) for each station
        resistanceCompTopArray = []
        resistanceCompBottomArray = []
        resistanceTensTopArray = []
        resistanceTensBottomArray = []

        # Initialize arrays to store top and bottom stress for each station
        stressTopArray = []
        stressBottomArray = []

        # Loop through each station
        for k in range(1,station_no-2,1):
            # print(k)

            # X-coordinates for the sides of this station
            X1_in = station_in[k]
            X2_in = station_in[k+1]
            X1_out = station_out[k]
            X2_out = station_out[k+1]

            # Arrays to store the YZ-coordinates of each point in the station (inner and outer hull)
            Y1_in = []; Z1_in = []
            Y2_in = []; Z2_in = []
            Y1_out = []; Z1_out = []
            Y2_out = []; Z2_out = []

            # Loop through each x coordinate and get every point in the cross-section
            for i in range(0,len(x_in),1):

                if x_out[i] == X1_out:
                    Y1_out.append(y_out[i])
                    Z1_out.append(z_out[i])

                elif x_out[i] == X2_out:
                    Y2_out.append(y_out[i])
                    Z2_out.append(z_out[i])
                
                if x_in[i] == X1_in:
                    Y1_in.append(y_in[i])
                    Z1_in.append(z_in[i])

                elif x_in[i] == X2_in:
                    Y2_in.append(y_in[i])
                    Z2_in.append(z_in[i])

            # Depth and Moment (Value) for each station
            depth = (abs(min(Z1_out))+abs(min(Z2_out)))/2
            value = float(momentArray[k])


            # Calculate the canoe's volume (intermediate step for y-bar)
            volume = 0
            product = 0 # y_bar*Volume
            for i in range(0,len(Y1_out)-1,1):
                z_i = ((Z1_out[i]+Z1_out[i+1]+Z1_in[i]+Z1_in[i+1])/4 + (Z2_out[i]+Z2_out[i+1]+Z2_in[i]+Z2_in[i+1])/4) /2
                x = (abs(X1_in-X2_in) + abs(X1_out-X2_out))/2
                y = (abs(Y1_in[i] - Y1_out[i]) + abs(Y1_in[i+1]-Y1_out[i+1]) + abs(Y2_in[i] - Y2_out[i]) + abs(Y2_in[i+1]-Y2_out[i+1]))/4
                z = (abs(Z1_out[i+1]-Z1_out[i]) + abs(Z1_in[i+1]-Z1_in[i]) + abs(Z2_out[i+1]-Z2_out[i]) + abs(Z2_in[i+1]-Z2_in[i]))/4

                volume_i = x * y * z
                volume += volume_i
                product += volume_i * z_i
            
            # Calculate y-bar from the top and bottom
            y_bar_top = abs(product/volume)
            y_bar_bottom = y_bar_top - depth

            # Calculate I
            I = 0
            for i in range(0,len(Y1_out)-1,1):
                z_i = ((Z1_out[i]+Z1_out[i+1]+Z1_in[i]+Z1_in[i+1])/4 + (Z2_out[i]+Z2_out[i+1]+Z2_in[i]+Z2_in[i+1])/4) /2
                y = (abs(Y1_in[i] - Y1_out[i]) + abs(Y1_in[i+1]-Y1_out[i+1]) + abs(Y2_in[i] - Y2_out[i]) + abs(Y2_in[i+1]-Y2_out[i+1]))/4
                z = (abs(Z1_out[i+1]-Z1_out[i]) + abs(Z1_in[i+1]-Z1_in[i]) + abs(Z2_out[i+1]-Z2_out[i]) + abs(Z2_in[i+1]-Z2_in[i]))/4
                I_i = (1/12*y*z**3 + y*z*(abs(z_i) - y_bar_top)**2)/(10**(12)) # [m^4]
                I = I + I_i
        

            # print(y_bar_top)
            # print(y_bar_bottom)
            # print(I)

            # Calculate Stress and Resistance from the top and bottom
            stress_top = value*(y_bar_top/1000)/I
            stress_bottom = value*(y_bar_bottom/1000)/I

            # print(stress_top)
            # print(stress_bottom)
            # print(value)

            resistance_top_comp = compressive_strength * I / (y_bar_top/1000) * 10**6  # Nm
            resistance_bottom_comp = compressive_strength * I / (y_bar_bottom/1000) * 10**6  # Nm
            resistance_top_tens = tensile_strength * I / (y_bar_top/1000) * 10**6  # Nm
            resistance_bottom_tens = tensile_strength * I / (y_bar_bottom/1000) * 10**6  # Nm

            # Store this station's top and bottom resistances in arrays
            resistanceCompTopArray.append(resistance_top_comp)
            resistanceCompBottomArray.append(resistance_bottom_comp)
            resistanceTensTopArray.append(resistance_top_tens)
            resistanceTensBottomArray.append(resistance_bottom_tens)

            # Store this station's top and bottom stresses in arrays
            stressTopArray.append(stress_top/10**6)
            stressBottomArray.append(stress_bottom/10**6)

            ## <?><?><?>
            # Rearrange stress_top / stress_bottom


        # print("Max Compressive Stress Top:", max(stressTopArray), "MPa")
        # print("Max Tensile Stress Top:", min(stressTopArray), "MPa")
        # print("Max Compressive Stress Bottom:", max(stressBottomArray), "MPa")
        # print("Max Tensile Stress Bottom:", min(stressBottomArray), "MPa")

        # # Plot top and bottom stress for each load case
        # plt.plot(stations_mm, stressTopArray)
        # # plt.axhline(y = -1, color = 'r', linestyle = '-') 
        # plt.title('Top Stress')
        # plt.xlabel('x (mm)')
        # plt.yticks(np.arange(round(min(stressTopArray), 1) - 0.1,round(max(stressTopArray), 1) + 0.1,0.1))
        # plt.ylabel('Stress (MPa)')
        # plt.grid()
        # plt.show()

        # plt.plot(stations_mm, stressBottomArray)
        # plt.axhline(y = -cv.tensile_strength, color = 'r', linestyle = '-') 
        # plt.title('Bottom Stress')
        # plt.xlabel('x (mm)')
        # plt.yticks(np.arange(round(-cv.tensile_strength, 1) - 0.1,round(max(stressBottomArray), 1) + 0.1,0.1))
        # plt.ylabel('Stress (MPa)')
        # plt.grid()
        # plt.show()
        
        stressTopByCase.append(stressTopArray)
        stressBottomByCase.append(stressBottomArray)

        resistanceCompTopArrays.append(resistanceCompTopArray)
        resistanceCompBottomArrays.append(resistanceCompBottomArray)
        resistanceTensTopArrays.append(resistanceTensTopArray)
        resistanceTensBottomArrays.append(resistanceTensBottomArray)


        
    
    return (PAD_CASE_STATIONS, PAD_CASE_LENGTH, PAD_CASE_MOMENT, stressTopByCase, stressBottomByCase, stations_mm, stressTopArray, stressBottomArray, resistanceCompTopArray, resistanceCompBottomArray, resistanceTensTopArray, resistanceTensBottomArray, stressTopByCase, stressBottomByCase, resistanceCompTopArrays, resistanceCompBottomArrays, resistanceTensTopArrays, resistanceTensBottomArrays)

def Max_Negative_Moments(input_files):
    # Negative moment - This has to be fixed
    # print("Max Negative Moments:\n")
    # Loop through each script

    results = {}

    for input_file in input_files:
        print("\033[4m" + input_file + ":\033[0m")
        file_path = os.path.join(script_dir, input_file)
        info = pd.read_csv(file_path, header=None)

        value = float(info[1][4])
        width = float(info[3][4])
        depth = float(info[4][4])
        target_station = float(info[2][4])

        # Extract Station Information
        Y1_in = []; Z1_in = []
        Y2_in = []; Z2_in = []
        Y1_out = []; Z1_out = []
        Y2_out = []; Z2_out = []

        for k in range(1,station_no-2,1):
            if k == target_station:
                X1_in = station_in[k]
                X2_in = station_in[k+1]
                X1_out = station_out[k]
                X2_out = station_out[k+1]
                
                for i in range(0,len(x_out),1):
                    if x_out[i] == X1_out:
                        Y1_out.append(y_out[i])
                        Z1_out.append(z_out[i])

                    elif x_out[i] == X2_out:
                        Y2_out.append(y_out[i])
                        Z2_out.append(z_out[i])
                    
                    if x_in[i] == X1_in:
                        Y1_in.append(y_in[i])
                        Z1_in.append(z_in[i])

                    elif x_in[i] == X2_in:
                        Y2_in.append(y_in[i])
                        Z2_in.append(z_in[i])

        # Find y_bar
        volume = 0
        product = 0 # y_bar*Volume

        depth = 0

        for i in range(0,len(Y1_out)-1,1):
            z_i = ((Z1_out[i]+Z1_out[i+1]+Z1_in[i]+Z1_in[i+1])/4 + (Z2_out[i]+Z2_out[i+1]+Z2_in[i]+Z2_in[i+1])/4) /2
            x = (abs(X1_in-X2_in) + abs(X1_out-X2_out))/2
            y = (abs(Y1_in[i] - Y1_out[i]) + abs(Y1_in[i+1]-Y1_out[i+1]) + abs(Y2_in[i] - Y2_out[i]) + abs(Y2_in[i+1]-Y2_out[i+1]))/4
            z = (abs(Z1_out[i+1]-Z1_out[i]) + abs(Z1_in[i+1]-Z1_in[i]) + abs(Z2_out[i+1]-Z2_out[i]) + abs(Z2_in[i+1]-Z2_in[i]))/4

            volume_i = y * z # * x
            volume += volume_i
            product += volume_i * z_i

            depth = max(depth, abs(min(Z1_out)), abs(min(Z2_out)))
            
        y_bar_top = abs(product/volume)
        y_bar_bottom = depth - y_bar_top

        

        # Find I
        I = 0
        for i in range(0,len(Y1_out)-1,1):
            z_i = ((Z1_out[i]+Z1_out[i+1]+Z1_in[i]+Z1_in[i+1])/4 + (Z2_out[i]+Z2_out[i+1]+Z2_in[i]+Z2_in[i+1])/4) /2
            y = (abs(Y1_in[i] - Y1_out[i]) + abs(Y1_in[i+1]-Y1_out[i+1]) + abs(Y2_in[i] - Y2_out[i]) + abs(Y2_in[i+1]-Y2_out[i+1]))/4
            z = (abs(Z1_out[i+1]-Z1_out[i]) + abs(Z1_in[i+1]-Z1_in[i]) + abs(Z2_out[i+1]-Z2_out[i]) + abs(Z2_in[i+1]-Z2_in[i]))/4
            I_i = (1/12*y*z**3 + y*z*(abs(z_i) - y_bar_top)**2)/10**(12) # [m^4]
            I = I + I_i
            
        applied_negative_moment = value

        stress_top = applied_negative_moment*(y_bar_top/1000)/I
        stress_bottom = applied_negative_moment*(y_bar_bottom/1000)/I

        resistance_top = compressive_strength * I / (y_bar_top/1000) * 10**6  # Nm
        resistance_bottom = compressive_strength * I / (y_bar_bottom/1000) * 10**6  # Nm

        tensile_flexural_stress=stress_top/10**6
        compressive_flexural_stress=stress_bottom/10**6

        # print('Tensile Flexural Stress = ', tensile_flexural_stress, ' MPa')
        # print('Compressive Flexural Stress = ', compressive_flexural_stress, ' MPa')
        # print("Applied Negative Moment: " + str(applied_negative_moment) + ' Nm')
        # print("Stress Top: " + str(stress_top) + " MPa")
        # print("Stress Bottom: " + str(stress_bottom) + " MPa")
        # print("Resistance Top: " + str(resistance_top) + " Nm")
        # print("Resistance Bottom: " + str(resistance_bottom) + " Nm")
        print("\n")
        results[input_file] = {
            "applied_negative_moment": value,

            "stress_top": applied_negative_moment*(y_bar_top/1000)/I,
            "stress_bottom": applied_negative_moment*(y_bar_bottom/1000)/I,

            "resistance_top": compressive_strength * I / (y_bar_top/1000) * 10**6,  # Nm
            "resistance_bottom": compressive_strength * I / (y_bar_bottom/1000) * 10**6,  # Nm

            "tensile_flexural_stress": stress_top/10**6,
            "compressive_flexural_stress": stress_bottom/10**6,
        }

    return results
