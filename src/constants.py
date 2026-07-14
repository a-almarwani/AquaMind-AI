"""
Physical constants used throughout AquaMind AI.

All values use SI (International System of Units).
"""

# Water properties

WATER_DENSITY = 1000                # kg/m³

SPECIFIC_HEAT_WATER = 4186          # J/(kg·K)

LATENT_HEAT_VAPORIZATION = 2.45e6   # J/kg

# Basin properties

BASIN_THICKNESS = 0.001          # m

BASIN_DENSITY = 7850             # kg/m³

BASIN_SPECIFIC_HEAT = 500        # J/(kg·K)

# Optical properties

BASIN_ABSORPTIVITY = 0.90

# Radiative properties

EFFECTIVE_EMISSIVITY = 0.90

# Universal constants

STEFAN_BOLTZMANN = 5.67e-8          # W/(m²·K⁴)

# Simulation parameters

TIME_STEP = 60                      # s
SIMULATION_DURATION = 8 * 3600      # s