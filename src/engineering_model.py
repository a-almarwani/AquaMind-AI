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
    LATENT_HEAT_VAPORIZATION,
    STEFAN_BOLTZMANN,
    EFFECTIVE_EMISSIVITY,
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

def calculate_water_temperature_increase(
    net_energy,
    water_mass,
):
    """
    Calculate the water temperature increase.

    Parameters
    ----------
    net_energy : float
        Net thermal energy available to heat the basin water (J)

    water_mass : float
        Mass of water in the basin (kg)

    Returns
    -------
    float
        Water temperature increase (°C or K)
    """

    if net_energy < 0:
        raise ValueError("Net energy cannot be negative.")

    if water_mass <= 0:
        raise ValueError("Water mass must be greater than zero.")

    temperature_increase = (
        net_energy
        / (water_mass * SPECIFIC_HEAT_WATER)
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
        (vapor_pressure_difference * (water_temperature_c + 273.15))
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

def calculate_evaporative_heat_transfer(
    heat_transfer_coefficient,
    basin_area,
    water_vapor_pressure,
    glass_vapor_pressure,
    water_temperature_c,
    glass_temperature_c,
):
    """
    Calculate evaporative heat transfer from the basin water
    surface to the glass cover using Dunkle's model.

    Parameters
    ----------
    heat_transfer_coefficient : float
        Convective heat transfer coefficient (W/m²·K)

    basin_area : float
        Basin area (m²)

    water_vapor_pressure : float
        Saturation vapor pressure at the water surface (Pa)

    glass_vapor_pressure : float
        Saturation vapor pressure at the glass cover (Pa)

    water_temperature_c : float
        Basin water temperature (°C)

    glass_temperature_c : float
        Glass cover temperature (°C)

    Returns
    -------
    float
        Evaporative heat transfer rate (W)

    References
    ----------
    Dunkle, R. V. (1961). Solar water distillation.
    """

    if heat_transfer_coefficient < 0:
        raise ValueError("Heat transfer coefficient cannot be negative.")

    if basin_area <= 0:
        raise ValueError("Basin area must be greater than zero.")

    if water_vapor_pressure <= glass_vapor_pressure:
        raise ValueError(
            "Water vapor pressure must be greater than glass vapor pressure."
        )

    if water_temperature_c <= glass_temperature_c:
        raise ValueError(
            "Water temperature must be greater than glass temperature."
        )

    evaporative_heat_transfer = (
        0.016273
        * heat_transfer_coefficient
        * basin_area
        * (water_vapor_pressure - glass_vapor_pressure)
        / (water_temperature_c - glass_temperature_c)
    )

    return evaporative_heat_transfer


def calculate_radiative_heat_transfer_coefficient(
    water_temperature_c,
    glass_temperature_c,
):
    """
    Calculate the radiative heat transfer coefficient between
    the basin water surface and the glass cover.

    Parameters
    ----------
    water_temperature_c : float
        Basin water temperature (°C)

    glass_temperature_c : float
        Glass cover temperature (°C)

    Returns
    -------
    float
        Radiative heat transfer coefficient (W/m²·K)

    References
    ----------
    Based on the Stefan–Boltzmann law as commonly applied
    in solar still engineering literature.
    """

    if water_temperature_c <= glass_temperature_c:
        raise ValueError(
            "Water temperature must be greater than glass temperature."
        )

    # Convert Celsius to Kelvin
    water_temperature_k = water_temperature_c + 273.15
    glass_temperature_k = glass_temperature_c + 273.15

    heat_transfer_coefficient = (
        EFFECTIVE_EMISSIVITY
        * STEFAN_BOLTZMANN
        * (
            water_temperature_k ** 2
            + glass_temperature_k ** 2
        )
        * (
            water_temperature_k
            + glass_temperature_k
        )
    )

    return heat_transfer_coefficient

def calculate_radiative_heat_transfer(
    heat_transfer_coefficient,
    basin_area,
    water_temperature_c,
    glass_temperature_c,
):
    """
    Calculate radiative heat transfer from the basin water
    surface to the glass cover.

    Parameters
    ----------
    heat_transfer_coefficient : float
        Radiative heat transfer coefficient (W/m²·K)

    basin_area : float
        Basin area (m²)

    water_temperature_c : float
        Basin water temperature (°C)

    glass_temperature_c : float
        Glass cover temperature (°C)

    Returns
    -------
    float
        Radiative heat transfer rate (W)
    """

    if heat_transfer_coefficient < 0:
        raise ValueError("Heat transfer coefficient cannot be negative.")

    if basin_area <= 0:
        raise ValueError("Basin area must be greater than zero.")

    if water_temperature_c <= glass_temperature_c:
        raise ValueError(
            "Water temperature must be greater than glass temperature."
        )

    radiative_heat_transfer = (
        heat_transfer_coefficient
        * basin_area
        * (water_temperature_c - glass_temperature_c)
    )

    return radiative_heat_transfer

def calculate_total_internal_heat_transfer(
    convective_heat_transfer,
    evaporative_heat_transfer,
    radiative_heat_transfer,
):
    """
    Calculate the total internal heat transfer from the basin
    water surface to the glass cover.

    Parameters
    ----------
    convective_heat_transfer : float
        Convective heat transfer (W)

    evaporative_heat_transfer : float
        Evaporative heat transfer (W)

    radiative_heat_transfer : float
        Radiative heat transfer (W)

    Returns
    -------
    float
        Total internal heat transfer (W)
    """

    if convective_heat_transfer < 0:
        raise ValueError(
            "Convective heat transfer cannot be negative."
        )

    if evaporative_heat_transfer < 0:
        raise ValueError(
            "Evaporative heat transfer cannot be negative."
        )

    if radiative_heat_transfer < 0:
        raise ValueError(
            "Radiative heat transfer cannot be negative."
        )

    total_heat_transfer = (
        convective_heat_transfer
        + evaporative_heat_transfer
        + radiative_heat_transfer
    )

    return total_heat_transfer

def calculate_net_energy(
    absorbed_energy,
    total_internal_heat_transfer,
    operating_time_hours,
):
    """
    Calculate the net thermal energy available to heat the basin water.

    Parameters
    ----------
    absorbed_energy : float
        Total absorbed solar energy (J)

    total_internal_heat_transfer : float
        Total internal heat transfer rate (W)

    operating_time_hours : float
        Operating time (hours)

    Returns
    -------
    float
        Net thermal energy available (J)

    Note
    ----
    The total internal heat transfer rate is converted from
    power (W) to energy (J) before calculating the remaining
    thermal energy stored in the basin water.
    """

    if absorbed_energy < 0:
        raise ValueError("Absorbed energy cannot be negative.")

    if total_internal_heat_transfer < 0:
        raise ValueError(
            "Total internal heat transfer cannot be negative."
        )

    if operating_time_hours <= 0:
        raise ValueError(
            "Operating time must be greater than zero."
        )

    # Convert hours to seconds
    operating_time_seconds = operating_time_hours * 3600

    # Convert heat transfer rate (W) into energy (J)
    total_heat_loss = (
        total_internal_heat_transfer
        * operating_time_seconds
    )

    net_energy = (
        absorbed_energy
        - total_heat_loss
    )

    return net_energy

def calculate_distilled_water_mass(
    evaporative_heat_transfer,
    operating_time_hours,
):
    """
    Calculate the mass of distilled water produced.

    Parameters
    ----------
    evaporative_heat_transfer : float
        Evaporative heat transfer rate (W)

    operating_time_hours : float
        Operating time (hours)

    Returns
    -------
    float
        Distilled water produced (kg)

    References
    ----------
    Based on the latent heat of vaporization relationship used
    in solar desalination engineering.
    """

    if evaporative_heat_transfer < 0:
        raise ValueError(
            "Evaporative heat transfer cannot be negative."
        )

    if operating_time_hours <= 0:
        raise ValueError(
            "Operating time must be greater than zero."
        )

    operating_time_seconds = operating_time_hours * 3600

    evaporative_energy = (
        evaporative_heat_transfer
        * operating_time_seconds
    )

    distilled_water_mass = (
        evaporative_energy
        / LATENT_HEAT_VAPORIZATION
    )

    return distilled_water_mass

def convert_water_mass_to_litres(water_mass):
    """
    Convert water mass to volume in litres.

    Parameters
    ----------
    water_mass : float
        Water mass (kg)

    Returns
    -------
    float
        Water volume (litres)

    Note
    ----
    This assumes water density is approximately 1000 kg/m³,
    so 1 kg of water is approximately 1 litre.
    """

    if water_mass < 0:
        raise ValueError("Water mass cannot be negative.")

    water_volume_litres = water_mass

    return water_volume_litres
 
if __name__ == "__main__":

    # Example operating conditions
    irradiance = 800          # W/m²
    water_temperature = 60    # °C
    glass_temperature = 35    # °C
    basin_area = 1.0          # m²
    water_depth_cm = 2        # cm
    operating_time = 8        # hours

    # Solar energy
    solar_power = calculate_solar_energy(
        irradiance,
        basin_area,
    )

    absorbed_power = calculate_absorbed_solar_energy(
        solar_power,
    )

    absorbed_energy = calculate_absorbed_energy(
        absorbed_power,
        operating_time,
    )

    # Water properties
    water_volume = calculate_water_volume(
        basin_area,
        water_depth_cm,
    )

    water_mass = calculate_water_mass(
        water_volume,
    )

    # Vapor pressures
    pw = calculate_saturation_vapor_pressure(
        water_temperature,
    )

    pg = calculate_saturation_vapor_pressure(
        glass_temperature,
    )

    # Convective heat transfer
    hc = calculate_convective_heat_transfer_coefficient(
        water_temperature,
        glass_temperature,
        pw,
        pg,
    )

    qc = calculate_convective_heat_transfer(
        hc,
        basin_area,
        water_temperature,
        glass_temperature,
    )

    # Evaporative heat transfer
    qe = calculate_evaporative_heat_transfer(
        hc,
        basin_area,
        pw,
        pg,
        water_temperature,
        glass_temperature,
    )

    # Radiative heat transfer
    hr = calculate_radiative_heat_transfer_coefficient(
        water_temperature,
        glass_temperature,
    )

    qr = calculate_radiative_heat_transfer(
        hr,
        basin_area,
        water_temperature,
        glass_temperature,
    )

    # Total internal heat transfer
    qt = calculate_total_internal_heat_transfer(
        qc,
        qe,
        qr,
    )

    # Energy balance
    net_energy = calculate_net_energy(
        absorbed_energy,
        qt,
        operating_time,
    )

    temperature_increase = calculate_water_temperature_increase(
        net_energy,
        water_mass,
    )

    # Freshwater production
    distilled_mass = calculate_distilled_water_mass(
        qe,
        operating_time,
    )

    distilled_volume = convert_water_mass_to_litres(
        distilled_mass,
    )

    # Results
    print("Solar power:", solar_power)
    print("Absorbed solar power:", absorbed_power)
    print("Absorbed energy:", absorbed_energy)
    print("Water volume:", water_volume)
    print("Water mass:", water_mass)
    print("Water vapor pressure:", pw)
    print("Glass vapor pressure:", pg)
    print("Convective heat transfer coefficient:", hc)
    print("Convective heat transfer:", qc)
    print("Evaporative heat transfer:", qe)
    print("Radiative heat transfer coefficient:", hr)
    print("Radiative heat transfer:", qr)
    print("Total internal heat transfer:", qt)
    print("Net energy:", net_energy)
    print("Water temperature increase:", temperature_increase)
    print("Distilled water mass:", distilled_mass)
    print("Distilled water volume:", distilled_volume)