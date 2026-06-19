""" 
Starts and controls the ecosystem simulation.

This file initializes a habitat with animals and plants,
populates it with an initial population, and allows the user
to interactively run the simulation over days, months, or years.
During the simulation, growth, reproduction, weather effects,
disasters, and population changes are regularly updated and displayed.
"""


import random
import blatt_8_klassen as b


__author__ = "<8236539>, <Yakout>, <8408293>, <Alizadeh>"
__credit__ = "Written with assistance from ChatGPT and Gemini."
start_animals = []


def add_lions(creatures, count):
    for _ in range(count):
        v = random.randint(8, b.Lion.max_vitality)
        a = random.randint(1, b.Lion.max_age - 2)
        s = random.uniform(1.0, b.Lion.max_size)
        g = random.choice(["male", "female"])
        new = [b.Lion(v, a, s, g, alive=True)]
        creatures += new


def add_monkeys(creatures, count):
    for _ in range(count):
        v = random.randint(8, b.Monkey.max_vitality)
        a = random.randint(1, b.Monkey.max_age - 5)
        s = random.uniform(0.5, b.Monkey.max_size)
        g = random.choice(["male", "female"])
        new = [b.Monkey(v, a, s, g, alive=True)]
        creatures += new


def add_sheep(creatures, count):
    for _ in range(count):
        v = random.randint(6, b.Sheep.max_vitality)
        a = random.randint(1, b.Sheep.max_age - 2)
        s = random.uniform(0.5, b.Sheep.max_size)
        g = random.choice(["male", "female"])
        new = [b.Sheep(v, a, s, g, alive=True)]
        creatures += new


def add_plants(creatures, tree_count, grass_count, banana_count):
    for _ in range(tree_count):
        v = random.randint(10, b.Tree.max_vitality)
        a = random.randint(1, 10)
        s = random.uniform(1.0, 3.0)
        new = [b.Tree(v, a, s, True)]
        creatures += new
    for _ in range(grass_count):
        new =[b.Grass(vitality=50, age=0, size=0.1, alive=True)]
        creatures += new
    for _ in range(banana_count):
        new = [b.Banana(vitality=50, age=0, size=0.1, alive=True)]
        creatures += new


def main():
    # 1. Initialize and populate the environment
    env = b.Habitat("Serengeti", 1000, "clear", "spring")
    add_plants(env.creatures, tree_count=15, grass_count=100, banana_count=100)
    add_sheep(env.creatures, 20)
    add_monkeys(env.creatures, 10)
    add_lions(env.creatures, 2)

    simulated_years = 0
    simulated_months = 0
    simulated_days = 0
    #Standardizing time units
    days_in_month = 28
    days_in_year = 336 

    while True:
        type_per = input("for how long should the simulation run in (years/days/months): ").lower()
        n_per = int(input(f"for how many {type_per}? "))
    
        if type_per == "days":
            stop_day = n_per
        elif type_per == "months":
            stop_day = n_per * days_in_month
        elif type_per == "years":
            stop_day = n_per * days_in_year
        else:
            print("Unknown command.")
            break

        update_type = input("how would you like to see your update type (yearly/monthly/daily): ").lower()
        d = 0
        # Master Simulation Loop (Day-by-Day)
        while d <= stop_day:
        
            # 1. Start of Period Events (Occur on Day 0, 30, 60...)
            if simulated_days % days_in_year == 0:
                env.round_pyear()
                # Only increment visual counter if day > 0 to avoid double counting at start
                if simulated_days > 0: 
                    simulated_years += 1

            if simulated_days % days_in_month == 0:
                env.disastering()
                if simulated_days > 0:
                    simulated_months += 1

            # 2. Run the Daily Logic
            env.round_pday()
        
            # 3. Increment the counter AFTER the logic but BEFORE the update check
            simulated_days += 1
            d += 1
            if simulated_days % 50 == 0:
                print(f"Simulating... day {simulated_days}")
            # 4. Handle Updates/Pauses
            should_update = False
            if update_type == "daily":
                should_update = True
            # Check if the day we JUST finished makes a full month/year
            elif update_type == "monthly" and simulated_days % days_in_month == 0:
                should_update = True
            elif update_type == "yearly" and simulated_days % days_in_year == 0:
                should_update = True

            if should_update:
                env.update()
                # Added a helpful status print
                print(f"--- Progress: Year {simulated_days // days_in_year}, Month {simulated_days // days_in_month}, Day {simulated_days} ---")
                a = input("continue (enter) or end (end): ").lower()
                if a == "end":
                    quit()
        # Post-simulation options
        repeat_choice = input("restart, continue, or end?: ").lower()
        if repeat_choice == "restart":
            simulated_days, simulated_months, simulated_years = 0, 0, 0
            env = b.Habitat("Serengeti", 10000, "clear", "spring")
            env.creatures = []
            add_plants(env.creatures, tree_count=15, grass_count=100, banana_count=100)
            add_sheep(env.creatures, 70)
            add_monkeys(env.creatures, 35)
            add_lions(env.creatures, 8)
        elif repeat_choice == "end":
            break


_name_ = '_main_'


if _name_ == '_main_':
    main()