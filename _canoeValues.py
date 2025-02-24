# Grasshopper waterline must be modified per script
# ------------ Universal Constants ------------ #
water_density = 1000 # Density of water = 1000 kg/m^3
g = 9.81 # Gravity [m/s^2]
# Weights in lbs 130,       150,        175,        200         140 :( [Kielen made me do this]
pad_weights =   [58.967,    68.0389,    79.3787,    90.7185,    63.5029] # Paddler weight classes (kg)
DLF = 1.25
# LLF goes here someday maybe
safety_factor = 1.2
lamda = 0.75
beta = 0.21

alpha_s = 4 # As per CSA A23.3-14 CL 13.3.4.1 (13-7)

kneecap_length = 50 # Kneecap area length [mm]
kneecap_width = 50 # Kneecap area width [mm]

# ------------ Canoe-specific Constants ------------ #
concrete_density = 950 # kg/m^3 (dry density)
compressive_strength = 13 # MPa (f_c)
tensile_strength = 1.6 # MPa
concrete_thickness = 8 # mm

hasLayer1 = 1 # If the canoe has 1 layer of mesh
d_mesh_1 = 8 # distance between the first layer of reinforcement to the surface [mm]
hasLayer2 = 0 # If the canoe has 2 layers of mesh
d_mesh_2 = 0 # distance between the second layer of reinforcement to the surface [mm]

# Waterlines for 2, 3, 4, 6 paddler cases [mm]
grasshopper = [150, 140, 140, 0]

# ------------ Reinforcement Property ------------ #
phi_s = 0.85
fy = 1725 # [MPa] # outdated
phi_c = 0.65
E_s = 72400 # [MPa] # outdated
layer_unit_1 = 297.66 # one lap for layer 1 [mm^2/m]
layer_unit_2 = 297.66 # one lap for layer 2