"""
Testfälle der Ökosystem-Simulation.
"""


from blatt_8_klassen import Creature, Animal, Lion, Sheep, Monkey, Plant, Tree, Grass, Banana, Habitat



__author__ = "<8236539>, <Yakout>, <8408293>, <Alizadeh>"
__credit__ = "Written with assistance from ChatGPT and Gemini."



def test_creature():
    """
    >>> c = Creature(vitality=10, age=0, size=1)
    >>> c.grow()
    >>> c.age
    1
    >>> c.size
    1
    >>> creatures = [c]
    >>> c.die(available_area=10, creatures=creatures)
    False
    >>> c.vitality = 0
    >>> c.die(available_area=10, creatures=creatures)
    True
    """


def test_animal_feed_breed():
    """
    >>> s1 = Sheep(vitality=10, age=3, size=1, gender='male')
    >>> s2 = Sheep(vitality=10, age=3, size=1, gender='female')
    >>> creatures = [s1, s2]
    >>> baby = s1.breed(creatures, season='spring')
    >>> baby is None or isinstance(baby, Sheep)
    True
    >>> l = Lion(vitality=10, age=5, size=1, gender='male')
    >>> sheep = Sheep(vitality=5, age=3, size=1, gender='female')
    >>> creatures = [l, sheep]
    >>> victim = l.feed(creatures)
    >>> l.vitality >= 10
    True
    >>> (victim is sheep) or (victim is False) or (victim is None)
    True
    """ 


def test_lion_becoming_king():
    """
    >>> l = Lion(vitality=10, age=5, size=1, gender='male')
    >>> l.succ_hunts = 100
    >>> l.becoming_king()
    >>> l.king
    True
    >>> l.breeding_chance > 0.2
    True
    """


def test_sheep_breed_season():
    """
    >>> s1 = Sheep(vitality=10, age=3, size=1, gender='male')
    >>> s2 = Sheep(vitality=10, age=3, size=1, gender='female')
    >>> creatures = [s1, s2]
    >>> baby = s1.breed(creatures, season='spring')
    >>> baby is None or isinstance(baby, Sheep)
    True
    >>> s1.breeding_chance in [0.5, 0.4]
    True
    """


def test_monkey_feed_gorilla():
    """
    >>> m = Monkey(vitality=10, age=10, size=1, gender='male')
    >>> s = Sheep(vitality=10, age=3, size=1, gender='female')
    >>> creatures = [m, s]
    >>> m.feed(creatures)
    >>> isinstance(m.gorilla, bool)
    True
    >>> m.succ_hunts >= 0
    True
    """


def test_plant_feed_procreate():
    """
    >>> p = Plant()
    >>> p.max_vitality = 10
    >>> p.vitality = 5
    >>> p.feed('rainy')
    >>> p.vitality
    8
    >>> creatures = []
    >>> p.breeding_chance = 1
    >>> p.procreate(creatures)
    >>> len(creatures)
    1
    """


def test_tree_area_provided():
    """
    >>> t = Tree(vitality=10, age=5, size=3)
    >>> t.area_provided()
    4.5
    >>> t.size = 1
    >>> t.area_provided()
    0
    """


def test_grass_procreate():
    """
    >>> g = Grass()
    >>> g.breeding_chance = 1
    >>> creatures = []
    >>> g.procreate(creatures)
    >>> len(creatures)
    1
    """


def test_banana_procreate():
    """
    >>> b = Banana()
    >>> b.breeding_chance = 1
    >>> creatures = []
    >>> b.procreate(creatures)
    >>> len(creatures)
    1
    """


def test_habitat_methods():
    """
    >>> h = Habitat("TestHabitat", 10, "clear", "spring")
    >>> l = Lion(vitality=10, age=5, size=1, gender='male')
    >>> h.creatures.append(l)
    >>> h.calculate_areas()
    >>> hasattr(h, 'net_available')
    True
    >>> h.round_pday()
    >>> h.curr_days >= 1
    True
    >>> h.update()  # nur visuell
    >>> h.disastering()  # kein Fehler bei leerer Disaster-Trigger
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
