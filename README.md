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

(Zach)

### Flexural Stress

(Zach)

### Longitudinal Analysis_[2,3,4] Paddler

(Shekinah)

### Longitudinal Analysis_[6] Paddler

(Shekinah)

### Longitudinal Analysis_Transportation

(Zach)

### Longitudinal Shear Analysis

Relies On:
| CSV File | Script Output |
| --- | --- |
| Inner Hull | N/A |
| Outer Hull | N/A |
| Station Information | Approximation-Vol Diff |
| Length_vs_Shear_Display_Stand | Approximation-Vol Diff |
| Length_vs_Shear_2 Paddler | Length_vs_Shear_2 Paddler |
| Length_vs_Shear_4 Paddler | Length_vs_Shear_4 Paddler |
| Length_vs_Shear_6 Paddler | Length_vs_Shear_6 Paddler & Longitudinal Analysis_Transportation |
| Shear_and_Moment_Display_Stand | Approximation-Vol Diff |
| Shear_and_Moment_2 Paddler | Length_vs_Shear_2 Paddler |
| Shear_and_Moment_4 Paddler | Length_vs_Shear_4 Paddler |
| Shear_and_Moment_6 Paddler | Length_vs_Shear_6 Paddler & Longitudinal Analysis_Transportation |

Calculates the longitudinal shear stress at each station along the canoe along with an envelope of the max and min allowabale shear stress, for each of the critical cases. It also plots the shear force of each of the critical cases on one graph along with the shear force envelope.

### Punching Shear Analysis

(Shekinah)

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
