"""
This module simulates an ecological habitat. All entities inherit from the
Creature base class. It models life cycles including growth, feeding,
reproduction, and environmental reactions for both animals and plants.
"""

import random

__author__ = "<8236539>, <Yakout>, <8408293>, <Alizadeh>"
__credit__ = "Written with assistance from ChatGPT and Gemini."


class Creature:
    """
    Base class for all living beings in the habitat.
    Defines general properties such as age, size, vitality, and life status.
    """
    max_age = None
    max_size = None
    grow_ratio = None
    max_vitality = None

    def __init__(self, vitality, age, size, alive=True):
        """Initializes a creature with vitality, age, and size."""
        self.vitality = vitality
        self.age = age
        self.size = float(size)
        self.alive = alive

    def grow(self):
        """Increases age and increments size by the grow_ratio until max_size is reached."""
        if self.size < self.max_size:
            self.age += 1
            self.size += self.grow_ratio
        else:
            self.age += 1

    def die(self, a_area, creatures):# available area, creatures
        """
        Checks death conditions: old age, lack of vitality, or being larger than available space.
        Removes the creature from the habitat list if it dies.
        """
        if (self.age >= self.max_age or 
            self.size > a_area or 
            self.vitality <= 0):       
                self.alive = False
                if self in creatures:
                    creatures.remove(self)


class Animal(Creature):
    """
    Abstract animal class incorporating feeding and breeding logic.
    Supports different feeding types (Carnivore, Herbivore, Omnivore).
    """
    breeding_chance = None
    feeding_chance = None
    mature_age = None
    feeding_type = None
    colours = None

    def __init__(self, vitality, age, size, gender, alive=True):
        """Initializes an animal with a gender and a random colour from its species palette."""
        super().__init__(vitality, age, size, alive)
        self.gender = gender
        self.colour = random.choice(self.colours)

    def feed(self, creatures):
        """
        Attempts to find food within the creature list. 
        Success increases vitality; failure results in starvation (vitality loss).
        """
        prey = []
        if isinstance(self, Lion):
            prey = [a for a in creatures if isinstance(a, Sheep) or isinstance(a, Monkey)]
        elif isinstance(self, Sheep):
            prey = [a for a in creatures if isinstance(a, Banana) or isinstance(a, Grass)]
        elif isinstance(self, Monkey):
            if self.gorilla:
                prey = [a for a in creatures
                        if isinstance(a, Banana) or isinstance(a, Sheep) or isinstance(a, Lion)]
            else:
                prey = [a for a in creatures if isinstance(a, Banana) or
                        isinstance(a, Grass) or isinstance(a, Sheep)]
        
        if prey == []:
            self.vitality -= 1
            return False
        else:
            victim = random.choice(prey)
            if random.random() <= self.feeding_chance:
                if self.max_vitality > self.vitality: 
                    self.vitality = min(self.max_vitality, self.vitality + 4)
                victim.alive = False
                creatures.remove(victim)
                return victim


    def breed(self, creatures):
        """
        Attempts to reproduce with a partner of the opposite gender.
        Requires the animal to have reached mature_age.
        """
        typ = type(self)
        poss_partners = [a for a in creatures if isinstance(a, type(self)) and 
                         a.gender != self.gender]
        if poss_partners:
            partner = random.choice(poss_partners)
            gender = random.choice(["male", "female"])
            if (random.random() < self.breeding_chance and
                partner is not None and self.age >= self.mature_age):
                new_animal = typ(vitality=8, age=0, size=1, gender=gender, alive=True)
                new_animal.colour = random.choice([self.colour, partner.colour])
                creatures += [new_animal]
                return new_animal
        else:
            return False 


class Lion(Animal):
    """
    Apex predator. Can become 'King' after a certain number of successful hunts, 
    granting improved stats and breeding chances.
    """
    max_age = 10
    max_size = 4
    grow_ratio = max_size / max_age
    max_vitality = 8
    breeding_chance = 0.001
    feeding_chance = 0.25
    mature_age = 3
    feeding_type = "carnivore"
    colours = ["yellow", "red", "white", "black", "brown"]

    def __init__(self, vitality, age, size, gender, alive):
        super().__init__(vitality, age, size, gender, alive)
        self.king = False
        self.succ_hunts = 0
    
    def becoming_king(self):
        """Transforms the lion into a King if hunting thresholds are met."""
        if self.succ_hunts >= 30:
            self.breeding_chance += 0.31
            self.feeding_chance += 0.3
            self.max_vitality = 10
            self.king = True
    
    def feed(self, animals):
        """Lion-specific feeding that tracks hunt success for the King transformation."""
        super().feed(animals)
        self.succ_hunts += 1
        self.becoming_king()
        

class Sheep(Animal):
    """
    Herbivore with a high breeding rate, especially during the Spring season.
    """
    max_age = 12
    max_size = 3
    grow_ratio = max_size / max_age
    max_vitality = 8
    breeding_chance = 0.4
    feeding_chance = 0.2
    mature_age = 3
    feeding_type = "herbivore"
    colours = ["white", "black", "brown", "grey"]

    def __init__(self, vitality, age, size, gender, alive):
        super().__init__(vitality, age, size, gender, alive=True)
        self.colour = random.choice(self.colours)
    
    def breed(self, animals, season):
        """Increases breeding chance significantly during Spring."""
        if season == "spring":
            self.breeding_chance = 0.5
        super().breed(animals)


class Monkey(Animal):
    """
    Omnivore that can evolve into a Gorilla once it grows large enough 
    and consumes enough protein (Sheep).
    """
    max_age = 20
    max_size = 3
    grow_ratio = max_size / max_age
    max_vitality = 8
    breeding_chance = 0.15
    feeding_chance = 0.25
    mature_age = 5
    feeding_type = "omnivore"
    colours = ["white", "black", "grey"] + ["brown"] * 3

    def __init__(self, vitality, age, size, gender, alive):
        super().__init__(vitality, age, size, gender, alive=True)
        self.colour = random.choice(self.colours)
        self.gorilla = False
        self.succ_hunts = 0
    
    def feed(self, creatures):
        """Monkey-specific feeding that tracks Sheep consumption for Gorilla evolution."""
        victim = super().feed(creatures) 
        if isinstance(victim, Sheep):
            self.succ_hunts += 1
        self.becoming_gorilla()
        return victim

    def becoming_gorilla(self):
        """Evolution logic: Increases size and vitality if requirements are met."""
        if (self.succ_hunts >= 50 and
        self.age >= 10 and
        self.size == self.max_size and
        self.gorilla is False):
            self.max_size = 5
            self.max_vitality = 12
            self.gorilla = True


class Plant(Creature):
    """
    Base class for flora. Responds to weather and reproduces asexually.
    """
    mature_age = None
    breeding_chance = None

    def __init__(self, vitality, age, size, alive):
        super().__init__(vitality, age, size, alive)
    
    def procreate(self, creatures):
        """Randomly generates a new plant of the same type in the creature list."""
        if random.random() <= self.breeding_chance:
            typ = type(self) 
            new_plant = typ(vitality=10, age=0, size=0, alive=True)
            creatures += [new_plant]
            return new_plant 
        else:
            return False
    
    def feed(self, weather):
        """Adjusts plant vitality based on rainfall or drought."""
        if weather == "rainy":
            self.vitality = min(self.max_vitality, self.vitality + 5)
        else:
            self.vitality -= 1


class Tree(Plant):
    """
    Large plant that provides 'extra_area' to the habitat as it grows.
    """
    max_age = 50
    max_size = 2
    grow_ratio = max_size / max_age
    max_vitality = 10
    mature_age = 5
    breeding_chance = 0.0001

    def __init__(self, vitality, age, size, alive):
        super().__init__(vitality, age, size, alive)
    
    def area_provided(self, grown_area):
        """Returns the amount of vertical/extra space this tree adds to the habitat."""
        if self.size >= 0.5:
            grown_area += 0.001
            return grown_area
        else:
            return grown_area


class Grass(Plant):
    """Fast-spreading ground cover with high vitality capacity."""
    max_age = 10
    max_size = 1
    grow_ratio = max_size / max_age
    max_vitality = 120
    mature_age = 1
    breeding_chance = 0.1
    
    def __init__(self, vitality, age, size, alive):
        super().__init__(vitality, age, size, alive)


class Banana(Plant):
    """Short-lived fruit plant, essential food for monkeys and sheep."""
    max_age = 3
    max_size = 0.02
    grow_ratio = max_size / max_age
    max_vitality = 10
    mature_age = 0
    breeding_chance = 0.085

    def __init__(self, vitality, age, size, alive):
        super().__init__(vitality, age, size, alive)


class Habitat():
    """
    Manages the overall simulation environment, including the creature list, 
    weather patterns, seasons, and spatial capacity.
    """
    disasters = ["plague", "comet", "volcanos"]
    temp = None
    
    def __init__(self, name, area, weather, season):
        """Initializes the habitat with geographic and environmental parameters."""
        self.name = name
        self.area = area
        self.weather = weather
        self.season = season
        self.creatures = []
        self.plus_area = 0
        self.curr_days = 0
        self.u_area = 0
        self.available_area = 0
    
    def used_area(self):
        """Calculates the total space currently occupied by animals and trees."""
        self.u_area = 0
        for i in [a for a in self.creatures if isinstance(a, Animal) or isinstance(a, Tree)]:
            self.u_area += i.size
    
    def extra_area(self):
        """Calculates the bonus space provided by the current tree population."""
        self.plus_area = 0 
        for i in [a for a in self.creatures if isinstance(a, Tree)]:
            self.plus_area += i.area_provided(i.size)
        return self.plus_area
    
    def a_area(self):
        """Calculates net space remaining (Base + Bonus - Occupied)."""
        self.available_area = (self.area + self.plus_area) - self.u_area

    def weather_season(self, curr_days):
        """Determines the current season and random weather based on a 336-day year."""
        day_of_year = curr_days % 336

        if day_of_year < 63 or day_of_year >= 308:
            self.season = "winter"
            self.temp = random.randint(-15, 2)
            self.weather = random.choice(["rainy", "rainy", "clear"])
        elif 63 <= day_of_year < 147:
            self.season = "spring"
            self.temp = random.randint(15, 25)
            self.weather = random.choice(["rainy", "clear"])
        elif 147 <= day_of_year < 231:
            self.season = "Summer"
            self.temp = random.randint(27, 39)
            self.weather = random.choices(["rainy", "clear","hot-dry", "hot-dry"])
        else:
            self.season = "autumn"
            self.temp = random.randint(3, 14)
            self.weather = random.choices(["rainy", "rainy", "clear"])
    
    def round_pyear(self):
        """Executes annual growth for all creatures and checks for status evolutions."""
        for i in [a for a in self.creatures if isinstance(a, Animal)]:
            i.grow()
        for i in [a for a in self.creatures if isinstance(a, Plant)]:
            i.grow()
        for i in [a for a in self.creatures if isinstance(a, Lion)]:
            i.becoming_king()
        for i in [a for a in self.creatures if isinstance(a, Monkey)]:
            i.becoming_gorilla()
    
    def round_pday(self):
        """
        Simulates a single 24-hour cycle. 
        Updates environment, allows creatures to feed and breed, and cleans up dead entities.
        """
        self.weather_season(self.curr_days)
        self.used_area()
        self.extra_area()
        self.a_area()

        for i in list(self.creatures):
            if isinstance(i, Animal):
                if isinstance(i, Sheep):
                    i.breed(self.creatures, self.season)
                    i.feed(self.creatures)
                else:
                    i.feed(self.creatures)
                    i.breed(self.creatures)
                i.die(self.area + self.plus_area, self.creatures)
            elif isinstance(i, Plant):
                i.feed(self.weather)
                i.procreate(self.creatures)
            i.die(self.area + self.plus_area, self.creatures)

        self.curr_days += 1
          
    def update(self):
        """Prints a comprehensive visual report of the habitat's current status."""
        print(f'''---------------------------------------------------------------------------------------------------------
              stats:
    ((current weather: {self.weather}  Season: {self.season}  Tempreture: {self.temp}  Year: {self.curr_days//336}  day: {self.curr_days}  area: {self.area} ))
all creatures: {len(self.creatures)}
the lions : {len([a for a in self.creatures if isinstance(a, Lion)])}, kings among them: {len([a for a in self.creatures if isinstance(a, Lion) and a.king is True])} 
the sheep : {len([a for a in self.creatures if isinstance(a, Sheep)])}
monkeys   : {len([a for a in self.creatures if isinstance(a, Monkey)])}, gorillas among them: {len([a for a in self.creatures if isinstance(a, Monkey) and a.gorilla is True])}
available:  {round(self.available_area)}
Trees : {len([a for a in self.creatures if isinstance(a, Tree)])}, and given areas by trees: {round(self.plus_area)}
number of bananas: {len([a for a in self.creatures if isinstance(a, Banana)])}   number of grass per 1m^2: {len([a for a in self.creatures if isinstance(a, Grass)])}
---------------------------------------------------------------------------------------------------------
''')
  
    def disastering(self):
        """Triggers rare catastrophic events that eliminate a percentage of the population."""
        disaster = random.choice(self.disasters)
        if disaster == "plague" and len(self.creatures) > 100 and random.random() < 0.009:
            for _ in range(int(len(self.creatures)*0.30)):
                if self.creatures: self.creatures.remove(random.choice(self.creatures))
            print(disaster.upper())
        if disaster == "comet" and random.random() < 0.001:
            for _ in range(int(len(self.creatures)*0.40)):
                if self.creatures: self.creatures.remove(random.choice(self.creatures))
            print(disaster.upper())
        if disaster == "volcanos" and random.random() < 0.005:
            for _ in range(int(len(self.creatures)*0.30)):
                if self.creatures: self.creatures.remove(random.choice(self.creatures))
            print(disaster.upper())