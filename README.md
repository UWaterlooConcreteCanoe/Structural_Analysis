# University of Waterloo Concrete Canoe Analysis Suite

These scripts are designed to take in the properties of the mix (as variables in _canoeValues.py) and hull design (as 3d points in csv files in data/HullDesignExports) and paddler positions and weights entered in each of the Longitudinal Analysis scripts, and calculate the canoe's expected structural integrity and performance characteristics.

# Script Run Order

1. Approximation-Vol Diff.ipynb
2. Longitudinal Analysis_[2-6] Paddler.ipynb
3. All Other Scripts

# Script Overview

### _canoeValues

Relies On: None

Contains all constants used in the code, for variables, concrete properties, etc. Imported into basically every file.

Ensure this is updated before running any scripts!

### Approximation-Vol Diff
| CSV File | Script Output |
| --- | --- |
| Inner Hull | N/A |
| Outer Hull | N/A |

The first part of this script is solving for the volume and mass of the canoe station by station. This is accomplished by subtracting the volume bound by the inner hull from the volume bound by the outer hull. Currently, this script also performs the longitudinal and shear analysis for the display case.

### Flexural Stress
| CSV File | Script Output |
| --- | --- |
| Inner Hull | N/A |
| Outer Hull | N/A |
| Station Information | Approximation-Vol Diff |
| Length_vs_Moment_Display_Stand | Approximation-Vol Diff |
| Length_vs_Moment_2 Paddler | Longitudinal Analysis_2 Paddler |
| Length_vs_Moment_4 Paddler | Longitudinal Analysis_4 Paddler |
| Length_vs_Moment_6 Paddler | Longitudinal Analysis_6 Paddler & Longitudinal Analysis_Transportation |
| Shear_and_Moment_Display_Stand | Approximation-Vol Diff |
| Shear_and_Moment_2 Paddler | Longitudinal Analysis_2 Paddler |
| Shear_and_Moment_4 Paddler | Longitudinal Analysis_4 Paddler |
| Shear_and_Moment_6 Paddler | Longitudinal Analysis_6 Paddler & Longitudinal Analysis_Transportation |

For all load cases, solves for the stress experienced along the top and bottom of the canoe due to bending moment. The max tensile and compressive stresses can be compared with the concrete strength to determine if the canoe fails due to longitudinal bending. Plots the bending moment experienced in each case against the allowable bending moment to produce the resistance envelope plot.

### Longitudinal Analysis_[2,3,4] Paddler

Calculates maximum shear force and bending moments that the canoe experiences in the case of the races. Creates shear force and bending moment diagrams. Also calculates the waterline, water weight, and canoe total weight.

### Longitudinal Analysis_[6] Paddler

Calculates maximum shear force and bending moments that the canoe experiences during the swamp test. Creates shear force and bending moment diagrams. Also calculates the waterline, water weight, and canoe total weight.

### Longitudinal Analysis_Transportation

**THIS SHOULD NOT BE RUN TO AVOID OVERWRITING CSVs**
**Zach thinks he commented the sections that would overwrite but just to be safe**

In theory this would obtain a maximum allowable acceleration based on the bending moment resistance obtained in FlexuralStress. In reality, that functionality is mostly hard-coded and it is almost entirely a copy of Longitudinal Analysis_6 Paddler. 



### Longitudinal Shear Analysis

Relies On:
| CSV File | Script Output |
| --- | --- |
| Inner Hull | N/A |
| Outer Hull | N/A |
| Station Information | Approximation-Vol Diff |
| Length_vs_Shear_Display_Stand | Approximation-Vol Diff |
| Length_vs_Shear_2 Paddler | Longitudinal Analysis_2 Paddler |
| Length_vs_Shear_4 Paddler | Longitudinal Analysis_4 Paddler |
| Length_vs_Shear_6 Paddler | Longitudinal Analysis_6 Paddler & Longitudinal Analysis_Transportation |
| Shear_and_Moment_Display_Stand | Approximation-Vol Diff |
| Shear_and_Moment_2 Paddler | Longitudinal Analysis_2 Paddler |
| Shear_and_Moment_4 Paddler | Longitudinal Analysis_4 Paddler |
| Shear_and_Moment_6 Paddler | Longitudinal Analysis_6 Paddler & Longitudinal Analysis_Transportation |

Calculates the longitudinal shear stress at each station along the canoe along with an envelope of the max and min allowabale shear stress, for each of the critical cases. It also plots the shear force of each of the critical cases on one graph along with the shear force envelope.

### Punching Shear Analysis

Calculates the punching shear stress at the canoe’s critical location, punching shear stress canoe resisted and compares the minimum punching shear resisted to the stress at critical location. Also calculates the minimum compressive strength required to resist punching shear.

### roadSurfaceModel

(Zach)

### Torsional Analysis

Relies On:
| CSV File | Script Output |
| --- | --- |
| Outer Hull | N/A |
| Station Information | Approximation-Vol Diff |
| Shear_and_Moment_6 Paddler | Length_vs_Shear_6 Paddler & Longitudinal Analysis_Transportation |

Calculate torsional stress at each station along the length of the canoe.

### Torsional_Loading

Relies On:
| CSV File | Script Output |
| --- | --- |
| Outer Hull | N/A |
| Station Information | Approximation-Vol Diff |
| Station_Loads_2 Paddlers | Length_vs_Shear_2 Paddler |
| Station_Loads_4 Paddlers | Length_vs_Shear_4 Paddler |
| Station_Loads_6 Paddlers | Length_vs_Shear_6 Paddler |

Print the torsional loading at each station. Has a WIP section to calculate torsion along the canoe with forces focused on different sides for different paddlers.

### Transverse Analysis_6 Paddlers

Relies On:
| CSV File | Script Output |
| --- | --- |
| Outer Hull | N/A |
| Station Information | Approximation-Vol Diff |
| Station_Loads_6 Paddlers | Length_vs_Shear_6 Paddler & Longitudinal Analysis_Transportation |

Enter the paddler number case, calculates the max transverse load and at which station it occurs.

Outputs: Station_Loads_6 Paddlers.csv

### Transverse Shear from Center

WIP

### Transverse_Bending

Relies On:
| CSV File | Script Output |
| --- | --- |
| Outer Hull | N/A |
| Station Information | Approximation-Vol Diff |

Calculates the moments along the length of the canoe (?)
