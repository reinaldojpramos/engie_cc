import os

CO2_RATIO = float(os.getenv('CO2_RATIO', 0.3))
CO2_COST_PER_TON = float(os.getenv('CO2_COST_PER_TON', 20))


def calculate_gas_cost(fuel_price_per_mwh, efficiency):
    return (fuel_price_per_mwh / efficiency) + (CO2_RATIO * CO2_COST_PER_TON)

def calculate_kerosine_cost(fuel_price_per_mwh, efficiency):
    return fuel_price_per_mwh / efficiency
