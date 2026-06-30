"""
Engineering model for AquaMind AI.

This module contains research-informed calculations for
solar still performance.
"""

from constants import (
    WATER_DENSITY,
    SPECIFIC_HEAT_WATER,
    BASIN_ABSORPTIVITY,
)


def calculate_solar_energy(irradiance, basin_area):
    """
    Calculate incoming solar power.

    Parameters
    ----------
    irradiance : float
        Solar irradiance (W/m²)

    basin_area : float
        Basin area (m²)

    Returns
    -------
    float
        Incoming solar power (W)
    """

    if irradiance < 0:
        raise ValueError("Solar irradiance cannot be negative.")

    if basin_area <= 0:
        raise ValueError("Basin area must be greater than zero.")

    solar_power = irradiance * basin_area

    return solar_power

def calculate_absorbed_solar_energy(solar_power):
    """
    Calculate the solar power absorbed by the basin.

    Parameters
    ----------
    solar_power : float
        Incoming solar power (W)

    Returns
    -------
    float
        Absorbed solar power (W)
    """

    if solar_power < 0:
        raise ValueError("Solar power cannot be negative.")

    absorbed_power = solar_power * BASIN_ABSORPTIVITY

    return absorbed_power

def calculate_water_volume(basin_area, water_depth_cm):
    """
    Calculate the volume of water inside the basin.

    Parameters
    ----------
    basin_area : float
        Basin area (m²)

    water_depth_cm : float
        Water depth (cm)

    Returns
    -------
    float
        Water volume (m³)
    """

    if basin_area <= 0:
        raise ValueError("Basin area must be greater than zero.")

    if water_depth_cm <= 0:
        raise ValueError("Water depth must be greater than zero.")

    # Convert centimeters to meters
    water_depth_m = water_depth_cm / 100

    volume = basin_area * water_depth_m

    return volume

def calculate_water_mass(volume):
    """
    Calculate the mass of water in the basin.

    Parameters
    ----------
    volume : float
        Water volume (m³)

    Returns
    -------
    float
        Water mass (kg)
    """

    if volume <= 0:
        raise ValueError("Volume must be greater than zero.")

    mass = volume * WATER_DENSITY

    return mass

def calculate_absorbed_energy(absorbed_power, operating_time_hours):
    """
    Calculate the total absorbed solar energy.

    Parameters
    ----------
    absorbed_power : float
        Absorbed solar power (W)

    operating_time_hours : float
        Operating time (hours)

    Returns
    -------
    float
        Total absorbed energy (J)
    """

    if absorbed_power < 0:
        raise ValueError("Absorbed power cannot be negative.")

    if operating_time_hours <= 0:
        raise ValueError("Operating time must be greater than zero.")

    # Convert hours to seconds
    operating_time_seconds = operating_time_hours * 3600

    absorbed_energy = absorbed_power * operating_time_seconds

    return absorbed_energy

def calculate_water_temperature_increase(absorbed_energy, water_mass):
    """
    Calculate the ideal water temperature increase.

    Note
    ----
    This is a simplified learning calculation based on Q = mcΔT.
    It assumes all absorbed energy heats the water, so it does not
    represent the final solar still model.
    """

    if absorbed_energy < 0:
        raise ValueError("Absorbed energy cannot be negative.")

    if water_mass <= 0:
        raise ValueError("Water mass must be greater than zero.")

    temperature_increase = absorbed_energy / (
        water_mass * SPECIFIC_HEAT_WATER
    )

    return temperature_increase
