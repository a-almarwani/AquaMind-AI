"""
Engineering model for AquaMind AI.

This module contains research-informed calculations for
solar still performance.
"""

import math

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

def calculate_saturation_vapor_pressure(temperature_c):
    """
    Calculate saturation vapor pressure of water.

    Parameters
    ----------
    temperature_c : float
        Water or glass temperature (°C)

    Returns
    -------
    float
        Saturation vapor pressure (Pa)

    Note
    ----
    This is a helper function for the research-based evaporation model.
    """

    if temperature_c < 0:
        raise ValueError("Temperature cannot be below 0°C.")

    vapor_pressure = 610.78 * math.exp(
        (17.27 * temperature_c) / (temperature_c + 237.3)
    )

    return vapor_pressure

def calculate_convective_heat_transfer_coefficient(
    water_temperature_c,
    glass_temperature_c,
    water_vapor_pressure,
    glass_vapor_pressure,
):
    """
    Calculate the convective heat transfer coefficient between
    the basin water surface and the glass cover using Dunkle's model.

    Parameters
    ----------
    water_temperature_c : float
        Basin water temperature (°C)

    glass_temperature_c : float
        Glass cover temperature (°C)

    water_vapor_pressure : float
        Saturation vapor pressure at the water surface (Pa)

    glass_vapor_pressure : float
        Saturation vapor pressure at the glass cover (Pa)

    Returns
    -------
    float
        Convective heat transfer coefficient (W/m²·K)

    References
    ----------
    Dunkle, R. V. (1961). Solar water distillation.
    """

    if water_temperature_c <= glass_temperature_c:
        raise ValueError(
            "Water temperature must be greater than glass temperature."
        )

    if water_vapor_pressure <= glass_vapor_pressure:
        raise ValueError(
            "Water vapor pressure must be greater than glass vapor pressure."
        )

    temperature_difference = water_temperature_c - glass_temperature_c

    vapor_pressure_difference = (
        water_vapor_pressure - glass_vapor_pressure
    )

    dunkle_term = temperature_difference + (
        (vapor_pressure_difference * (water_temperature_c + 273))
        / (268900 - water_vapor_pressure)
    )

    heat_transfer_coefficient = 0.884 * (dunkle_term ** (1 / 3))

    return heat_transfer_coefficient

def calculate_convective_heat_transfer(
    heat_transfer_coefficient,
    basin_area,
    water_temperature_c,
    glass_temperature_c,
):
    """
    Calculate convective heat transfer from the basin water
    surface to the glass cover.

    Parameters
    ----------
    heat_transfer_coefficient : float
        Convective heat transfer coefficient (W/m²·K)

    basin_area : float
        Basin area (m²)

    water_temperature_c : float
        Basin water temperature (°C)

    glass_temperature_c : float
        Glass cover temperature (°C)

    Returns
    -------
    float
        Convective heat transfer rate (W)
    """

    if heat_transfer_coefficient < 0:
        raise ValueError("Heat transfer coefficient cannot be negative.")

    if basin_area <= 0:
        raise ValueError("Basin area must be greater than zero.")

    if water_temperature_c <= glass_temperature_c:
        raise ValueError(
            "Water temperature must be greater than glass temperature."
        )

    heat_transfer = (
        heat_transfer_coefficient
        * basin_area
        * (water_temperature_c - glass_temperature_c)
    )

    return heat_transfer

    print("Water vapor pressure:", pw)
    print("Glass vapor pressure:", pg)
    print("Convective heat transfer coefficient:", hc)

if __name__ == "__main__":
    water_temperature = 60
    glass_temperature = 40

    pw = calculate_saturation_vapor_pressure(water_temperature)
    pg = calculate_saturation_vapor_pressure(glass_temperature)

    hc = calculate_convective_heat_transfer_coefficient(
        water_temperature,
        glass_temperature,
        pw,
        pg,
    )

    qc = calculate_convective_heat_transfer(
        hc,
        1.0,
        water_temperature,
        glass_temperature,
    )

    print("Water vapor pressure:", pw)
    print("Glass vapor pressure:", pg)
    print("Convective heat transfer coefficient:", hc)
    print("Convective heat transfer:", qc)