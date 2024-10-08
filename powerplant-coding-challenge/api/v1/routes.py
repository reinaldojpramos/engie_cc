from flask import Blueprint, jsonify, request
from utils import math_utils, cost_utils

v1_blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')


@v1_blueprint.route('/productionplan', methods=['POST'])
def post_production_plan():
    """
    Calculate and allocate power production to meet a given load using available powerplants,
    prioritizing the most cost-effective options.

    This endpoint handles the power allocation based on the following principles:

    - Prioritize Wind Power:
       - Wind turbines are used first because they have no fuel costs and thus offer the lowest cost for power generation.
       - The amount of power from wind turbines depends on the percentage of wind available (e.g., 60% wind means a turbine with a 100 MW capacity will produce 60 MW).
       - Wind turbines don't produce CO2 and have no fuel cost, so they are fully utilized before considering other powerplants.

    - Attribute the remaining load to non-wind power:
       - After using wind power, the remaining energy demand (load) is assigned to non-wind powerplants, (gas-fired and turbojet).
       - Non-wind plants are chosen based on their cost-efficiency, with cheaper options being used first.

    - Costs:
       - Gas-Fired Plants: Cost of gas and CO2 emissions costs.
       - Turbojets: Cost based on the price of kerosine (more expensive than gas) and efficiency.

    - Merit Order:
       - Non-wind powerplants are sorted by their cost. The plants with the lowest cost are used first to cover the remaining load.

    Returns:
        A JSON response listing each powerplant's allocated power output to meet the total load efficiently.

    Example Input:
        {
          "load": 910,
          "fuels": {
            "gas(euro/MWh)": 13.4,
            "kerosine(euro/MWh)": 50.8,
            "co2(euro/ton)": 20,
            "wind(%)": 60
          },
          "powerplants": [
            {"name": "gasfiredbig1", "type": "gasfired", "efficiency": 0.53, "pmin": 100, "pmax": 460},
            {"name": "windpark1", "type": "windturbine", "efficiency": 1, "pmin": 0, "pmax": 150},
            # (...),
          ]
        }

    Example Output:
        [
          {"name": "windpark1", "p": 90.0},
          {"name": "gasfiredbig1", "p": 460.0},
          # (...),
        ]
    """
    # ACQUIRE DATA
    data = request.json
    load = data['load']
    fuels = data['fuels']
    powerplants = data['powerplants']

    response = []
    non_wind_plants = []

    for plant in powerplants:
        if plant['type'] == 'windturbine':
            generated_power = plant['pmax'] * (fuels['wind(%)'] / 100)
            rounded_power = math_utils.round_to_nearest_0_1(generated_power)
            response.append({'name': plant['name'], 'p': rounded_power})
            load -= rounded_power
            continue
        if plant['type'] == 'gasfired':
            cost_per_mwh = cost_utils.calculate_gas_cost(fuels['gas(euro/MWh)'], plant['efficiency'])
        elif plant['type'] == 'turbojet':
            cost_per_mwh = cost_utils.calculate_kerosine_cost(fuels['kerosine(euro/MWh)'], plant['efficiency'])
        else:
            continue

        non_wind_plants.append({
            'name': plant['name'],
            'type': plant['type'],
            'efficiency': plant['efficiency'],
            'pmin': plant['pmin'],
            'pmax': plant['pmax'],
            'cost_per_mwh': cost_per_mwh
        })

    # SORT NON WIND POWERPLANTS BY ASCENDING COST
    non_wind_plants.sort(key=lambda p: p['cost_per_mwh'])

    # ALLOCATE REMAINING LOAD TO NON-WIND PLANTS
    produced_power = []

    for plant in non_wind_plants:
        # PREVENT NEGATIVE LOAD VALUES
        if load <= 0:
            response.append({'name': plant['name'], 'p': 0.0})
            produced_power.append(0.0)
            continue

        # DETERMINE AMOUNT OF POWER GENERATED BY PLANT
        power_to_allocate = min(plant['pmax'], max(plant['pmin'], load))
        rounded_power = math_utils.round_to_nearest_0_1(power_to_allocate)

        # MAKE SURE POWER IS AT LEAST THE MINIMUM REQUIRED
        if rounded_power < plant['pmin']:
            rounded_power = 0.0

        response.append({'name': plant['name'], 'p': rounded_power})
        produced_power.append(rounded_power)
        load -= rounded_power

    # ENSURE THE TOTAL MATCHES THE LOAD
    final_total_produced = sum([p['p'] for p in response])
    if final_total_produced != data['load']:
        return jsonify({'error': 'Unable to match the exact load'}), 400

    return jsonify(response)
