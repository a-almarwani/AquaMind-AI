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
    TIME_STEP,
    SIMULATION_DURATION,
)
# =============================================================================
# Solar Energy
# =============================================================================

# region Solar Energy

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

# endregion


# =============================================================================
# Water Properties
# =============================================================================

# region Water Properties

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

# endregion


# =============================================================================
# Vapor Pressure
# =============================================================================

# region Vapor Pressure

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

# endregion


# =============================================================================
# Internal Heat Transfer
# =============================================================================

# region Internal Heat Transfer

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

# endregion


# =============================================================================
# External Heat Transfer
# =============================================================================

# region External Heat Transfer

def calculate_external_convective_heat_transfer_coefficient(
    wind_speed,
):
    """
    Calculate the external convective heat transfer coefficient
    between the glass cover and the ambient air.

    Parameters
    ----------
    wind_speed : float
        Wind speed (m/s)

    Returns
    -------
    float
        External convective heat transfer coefficient (W/m²·K)

    References
    ----------
    Based on the empirical correlation commonly used in
    solar still engineering literature:

        h = 5.7 + 3.8V

    where V is the wind speed (m/s).
    """

    if wind_speed < 0:
        raise ValueError(
            "Wind speed cannot be negative."
        )

    external_convective_heat_transfer_coefficient = (
        5.7
        + (3.8 * wind_speed)
    )

    return external_convective_heat_transfer_coefficient

def calculate_external_convective_heat_transfer(
    external_convective_heat_transfer_coefficient,
    basin_area,
    glass_temperature_c,
    ambient_temperature_c,
):
    """
    Calculate external convective heat transfer from the glass
    cover to the ambient air.

    Parameters
    ----------
    external_convective_heat_transfer_coefficient : float
        External convective heat transfer coefficient (W/m²·K)
    basin_area : float
        Basin area (m²)

    glass_temperature_c : float
        Glass cover temperature (°C)

    ambient_temperature_c : float
        Ambient air temperature (°C)

    Returns
    -------
    float
        External convective heat transfer rate (W)
    """

    if external_convective_heat_transfer_coefficient < 0:
        raise ValueError(
            "Heat transfer coefficient cannot be negative."
        )

    if basin_area <= 0:
        raise ValueError(
            "Basin area must be greater than zero."
        )

    if glass_temperature_c <= ambient_temperature_c:
        raise ValueError(
            "Glass temperature must be greater than ambient temperature."
        )

    external_convective_heat_transfer = (
        external_convective_heat_transfer_coefficient
        * basin_area
        * (
            glass_temperature_c
            - ambient_temperature_c
        )
    )

    return external_convective_heat_transfer

def calculate_sky_temperature(
    ambient_temperature_c,
):
    """
    Calculate the effective sky temperature.

    Parameters
    ----------
    ambient_temperature_c : float
        Ambient air temperature (°C)

    Returns
    -------
    float
        Effective sky temperature (°C)

    References
    ----------
    Based on the commonly used approximation in
    solar still engineering literature:

        T_sky = T_ambient - 6°C
    """

    sky_temperature = (
        ambient_temperature_c
        - 6
    )

    return sky_temperature

def calculate_external_radiative_heat_transfer(
    basin_area,
    glass_temperature_c,
    sky_temperature_c,
):
    """
    Calculate external radiative heat transfer from the glass
    cover to the sky.

    Parameters
    ----------
    basin_area : float
        Basin area (m²)

    glass_temperature_c : float
        Glass cover temperature (°C)

    sky_temperature_c : float
        Effective sky temperature (°C)

    Returns
    -------
    float
        External radiative heat transfer rate (W)

    References
    ----------
    Based on the Stefan-Boltzmann law for radiative heat loss
    from the glass cover to the effective sky temperature.
    """

    if basin_area <= 0:
        raise ValueError(
            "Basin area must be greater than zero."
        )

    if glass_temperature_c <= sky_temperature_c:
        raise ValueError(
            "Glass temperature must be greater than sky temperature."
        )

    glass_temperature_k = glass_temperature_c + 273.15
    sky_temperature_k = sky_temperature_c + 273.15

    external_radiative_heat_transfer = (
        EFFECTIVE_EMISSIVITY
        * STEFAN_BOLTZMANN
        * basin_area
        * (
            glass_temperature_k ** 4
            - sky_temperature_k ** 4
        )
    )

    return external_radiative_heat_transfer

def calculate_total_external_heat_loss(
    external_convective_heat_transfer,
    external_radiative_heat_transfer,
):
    """
    Calculate the total external heat loss from the glass cover.

    Parameters
    ----------
    external_convective_heat_transfer : float
        External convective heat transfer (W)

    external_radiative_heat_transfer : float
        External radiative heat transfer (W)

    Returns
    -------
    float
        Total external heat loss (W)
    """

    if external_convective_heat_transfer < 0:
        raise ValueError(
            "External convective heat transfer cannot be negative."
        )

    if external_radiative_heat_transfer < 0:
        raise ValueError(
            "External radiative heat transfer cannot be negative."
        )

    total_external_heat_loss = (
        external_convective_heat_transfer
        + external_radiative_heat_transfer
    )

    return total_external_heat_loss

# endregion


# =============================================================================
# Water Production
# =============================================================================

# region Water Production

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
 
# endregion


# =============================================================================
# Overall Energy Balance
# =============================================================================

# region Overall Energy Balance

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

# endregion


# =============================================================================
# Transient Simulation Engine
# =============================================================================

# region Transient Simulation Engine

def run_transient_simulation(
    solar_irradiance,
    ambient_temperature,
    wind_speed,
    basin_area,
    water_depth_cm,
):
    """
    Run a transient simulation of a basin-type solar still.

    Parameters
    ----------
    solar_irradiance : float
        Solar irradiance (W/m²)

    ambient_temperature : float
        Ambient air temperature (°C)

    wind_speed : float
        Wind speed (m/s)

    basin_area : float
        Basin area (m²)

    water_depth_cm : float
        Water depth (cm)

    Returns
    -------
    dict
        Final simulation results.
    """

    if solar_irradiance < 0:
        raise ValueError(
            "Solar irradiance cannot be negative."
        )

    if wind_speed < 0:
        raise ValueError(
            "Wind speed cannot be negative."
        )

    if basin_area <= 0:
        raise ValueError(
            "Basin area must be greater than zero."
        )

    if water_depth_cm <= 0:
        raise ValueError(
            "Water depth must be greater than zero."
        )

    basin_temperature = ambient_temperature
    water_temperature = ambient_temperature
    glass_temperature = ambient_temperature

    total_distilled_water = 0.0

    water_volume = calculate_water_volume(
        basin_area,
        water_depth_cm,
    )

    water_mass = calculate_water_mass(
        water_volume,
    )

    number_of_steps = int(
        SIMULATION_DURATION / TIME_STEP
    )

    for step in range(number_of_steps):

        current_time = step * TIME_STEP

        solar_power = calculate_solar_energy(
            solar_irradiance,
            basin_area,
        )

        absorbed_solar_power = calculate_absorbed_solar_energy(
            solar_power,
        )

        water_vapor_pressure = (
            calculate_saturation_vapor_pressure(
                water_temperature,
            )
        )

        glass_vapor_pressure = (
            calculate_saturation_vapor_pressure(
                glass_temperature,
            )
        )

        convective_heat_transfer_coefficient = (
            calculate_convective_heat_transfer_coefficient(
                water_temperature,
                glass_temperature,
                water_vapor_pressure,
                glass_vapor_pressure,
            )
        )

        convective_heat_transfer = (
            calculate_convective_heat_transfer(
                convective_heat_transfer_coefficient,
                basin_area,
                water_temperature,
                glass_temperature,
            )
        )

        evaporative_heat_transfer = (
            calculate_evaporative_heat_transfer(
                convective_heat_transfer_coefficient,
                basin_area,
                water_vapor_pressure,
                glass_vapor_pressure,
                water_temperature,
                glass_temperature,
            )
        )

        radiative_heat_transfer_coefficient = (
            calculate_radiative_heat_transfer_coefficient(
                water_temperature,
                glass_temperature,
            )
        )

        radiative_heat_transfer = (
            calculate_radiative_heat_transfer(
                radiative_heat_transfer_coefficient,
                basin_area,
                water_temperature,
                glass_temperature,
            )
        )

        total_internal_heat_transfer = (
            calculate_total_internal_heat_transfer(
                convective_heat_transfer,
                evaporative_heat_transfer,
                radiative_heat_transfer,
            )
        )

        external_convective_heat_transfer_coefficient = (
            calculate_external_convective_heat_transfer_coefficient(
                wind_speed,
            )
        )

        external_convective_heat_transfer = (
            calculate_external_convective_heat_transfer(
                external_convective_heat_transfer_coefficient,
                basin_area,
                glass_temperature,
                ambient_temperature,
            )
        )

        sky_temperature = calculate_sky_temperature(
            ambient_temperature,
        )

        external_radiative_heat_transfer = (
            calculate_external_radiative_heat_transfer(
                basin_area,
                glass_temperature,
                sky_temperature,
            )
        )

        total_external_heat_loss = (
            calculate_total_external_heat_loss(
                external_convective_heat_transfer,
                external_radiative_heat_transfer,
            )
        )

    return {
        "basin_temperature": basin_temperature,
        "water_temperature": water_temperature,
        "glass_temperature": glass_temperature,
        "total_distilled_water": total_distilled_water,
        "number_of_steps": number_of_steps,
    }

# endregion


# =============================================================================
# Testing
# =============================================================================

# region Testing



# endregion