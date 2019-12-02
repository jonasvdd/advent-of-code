# part one
calc_fuel_mass = lambda x: int(x)//3 -2
with open('data/01_01.txt', 'r') as f:
    total_fuel = sum(list(map(calc_fuel_mass, f.readlines())))
print('part one total_fuel:', total_fuel)

# part two
def calc_fuel_fuel(fuel):
    fuel_for_fuel = 0
    adjusted_fuel =  calc_fuel_mass(fuel)
    while adjusted_fuel > 0:
        fuel_for_fuel += adjusted_fuel
        adjusted_fuel = calc_fuel_mass(adjusted_fuel)
    return fuel_for_fuel

with open('data/01_01.txt', 'r') as f:
    module_fuel = list(map(calc_fuel_mass, f.readlines()))
    module_fuel_fuel = list(map(calc_fuel_fuel, module_fuel))

print('module fuel', sum(module_fuel))
print('total total fuel:', sum(module_fuel) + sum(module_fuel_fuel))
