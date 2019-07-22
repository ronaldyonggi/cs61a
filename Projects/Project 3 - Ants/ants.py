"""CS 61A presents Ants Vs. SomeBees."""

import random
from ucb import main, interact, trace
from collections import OrderedDict

""" =============== Core Concept ================
1. The insect's armor attribute represents the amount of health the insect has. The insect
    is eliminated when the armor reaches 0
2. 'damage' is a class attribute of the insect class
3. The 'armor' attribute of the Ant class is an instance attribute instead of a class attribute
    because each Ant instance needs its own armor value
4. The 'damage' attribute of an Ant subclass (i.e. ThrowerAnt) is a class attribute instead of
    instance attribute because all Ants of the same subclass deal the same damage
5. Both Ant and Bee inherit from Insect class
6. The following are the attributes both instances of Ant and instances of Bee have in common:
    armor, damage, place, 'reduce_armor' method, action
7. There can only be one Ant in one place but there can be multiple bees
"""

################
# Core Classes #
################

class Place(object):
    """A Place holds insects and has an exit to another Place."""

    def __init__(self, name, exit=None):
        """Create a Place with the given NAME and EXIT.

        name -- A string; the name of this Place.
        exit -- The Place reached by exiting this Place (may be None).
        """
        self.name = name
        self.exit = exit
        self.bees = []        # A list of Bees
        self.ant = None       # An Ant
        self.entrance = None  # A Place
        #Entrance = to the right, exit = to the left
        #In tests, place0 is the most left, while place1 is to the right of place0. This means
        # place0.entrance is place1.

        # Phase 1: Add an entrance to the exit
        # BEGIN Problem 2
        """ Hint from -u: The entrance attribute of a Place instance is set to another Place WHEN 
        the entrance of that Place instance (another Place instance) is initialized
        
        Most helpful hint: Recall that when inside the definition of an __init__ method, 'self' is bound
        to the newly created object
        """

        #Example: Assume right now we're initializing a Place 'PlaceRight'. The if conditional below indicates that 
        # PlaceRight has an exit (let's say PlaceLeft). This way, we need to state that PlaceLeft's entrance is PlaceRight.
        if self.exit is not None:
            self.exit.entrance = self

        # END Problem 2

    def add_insect(self, insect):
        """Add an INSECT to this Place.

        There can be at most one Ant in a Place, unless exactly one of them is
        a BodyguardAnt (Phase 6), in which case there can be two. If add_insect
        tries to add more Ants than is allowed, an assertion error is raised.

        There can be any number of Bees in a Place.
        """
        if insect.is_ant:
            if self.ant is None:
                self.ant = insect
            #This else occurs if there's already a Ant present in Place
            else:
                # BEGIN Problem 9
# 1. If:
# a. The Ant already present in the Place is a container 
# b. The container is not containing any Ant
# c. The insect that's going to be added is another container
# Then set the ant being contained = insect argument
# 2. If:
# a. The Ant already present in the Place is NOT a container
# b. The insect that's going to be added is a container
# Then set the ant in the place to be the container, and set 
# the ant that was previously in Place's to be the contained Ant
                if self.ant.container and not self.ant.ant and not insect.container:
                    self.ant.ant = insect
                elif not self.ant.container and insect.container:
                    self.ant, self.ant.ant = insect, self.ant
                else:
                    assert self.ant is None, 'Two ants in {0}'.format(self)
                # END Problem 9
        else:
            self.bees.append(insect)
        insect.place = self

    def remove_insect(self, insect):
        """Remove an INSECT from this Place.

        A target Ant may either be directly in the Place, or be contained by a
        container Ant at this place. The true QueenAnt may not be removed. If
        remove_insect tries to remove an Ant that is not anywhere in this
        Place, an AssertionError is raised.

        A Bee is just removed from the list of Bees.
        """
        if insect.is_ant:
            # Special handling for QueenAnt
            # BEGIN Problem 13
            if insect.name == 'Queen':
                if insect.true_queen:
                    return
            # END Problem 13

            # Special handling for BodyguardAnt
            if self.ant is insect:
                if hasattr(self.ant, 'container') and self.ant.container:
                    self.ant = self.ant.ant
                else:
                    self.ant = None
            else:
                if hasattr(self.ant, 'container') and self.ant.container and self.ant.ant is insect:
                    self.ant.ant = None
                else:
                    assert False, '{0} is not in {1}'.format(insect, self)
        else:
            self.bees.remove(insect)

        insect.place = None

    def __str__(self):
        return self.name


class Insect(object):
    """An Insect, the base class of Ant and Bee, has armor and a Place."""

    is_ant = False
    damage = 0
    # watersafe is an attribute that determines if the following Insect can be
    #deployed in water
    watersafe = False

    def __init__(self, armor, place=None):
        """Create an Insect with an ARMOR amount and a starting PLACE."""
        self.armor = armor
        self.place = place  # set by Place.add_insect and Place.remove_insect

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and remove the insect from its place if it
        has no armor remaining.

        >>> test_insect = Insect(5)
        >>> test_insect.reduce_armor(2)
        >>> test_insect.armor
        3
        """
        self.armor -= amount
        if self.armor <= 0:
            self.place.remove_insect(self)

    def action(self, colony):
        """The action performed each turn.

        colony -- The AntColony, used to access game state information.
        """

    def __repr__(self):
        cname = type(self).__name__
        return '{0}({1}, {2})'.format(cname, self.armor, self.place)


class Bee(Insect):
    """A Bee moves from place to place, following exits and stinging ants."""

    name = 'Bee'
    damage = 1
    watersafe = True #Bees fly, so they are watersafe

    def sting(self, ant):
        """Attack an ANT, reducing its armor by 1."""
        ant.reduce_armor(self.damage)

    def move_to(self, place):
        """Move from the Bee's current Place to a new PLACE."""
        self.place.remove_insect(self)
        place.add_insect(self)

    def blocked(self):
        """Return True if this Bee cannot advance to the next Place."""
        # Phase 4: Special handling for NinjaAnt
        # BEGIN Problem 7
        #If there's no ant in place, return False
        if self.place.ant is None:
            return False
        else:
        #Return True/False depending on the Ant's blocks_path attribute
            return self.place.ant.blocks_path
        # END Problem 7

    def action(self, colony):
        """A Bee's action stings the Ant that blocks its exit if it is blocked,
        or moves to the exit of its current place otherwise.

        colony -- The AntColony, used to access game state information.
        """
        if self.blocked():
            self.sting(self.place.ant)
        elif self.armor > 0 and self.place.exit is not None:
            self.move_to(self.place.exit)


class Ant(Insect):
    """An Ant occupies a place and does work for the colony."""

    is_ant = True
    implemented = False  # Only implemented Ant classes should be instantiated
    # food_cost is a class attribute since all Ants of the same subclass cost the same to deploy
    food_cost = 0
    """ blocks_path is a class attribute that when it's True, it indicates that
    the Ant blocks the Bee's path until the Ant dies. This attribute was implemented
    for the sake of creating NinjaAnt, in which its blocks_path attribute is False"""
    blocks_path = True
    """ container is a class attribute that when it's True, it means the Ant is 
    a container type. This attribute is only True for BodyGuardAnt and TankAnt"""
    container = False

    def __init__(self, armor=1):
        """Create an Ant with an ARMOR quantity."""
        Insect.__init__(self, armor)

    def can_contain(self, other):
        # BEGIN Problem 9
        """Make sure the logic check of whether the Ant is a container comes first
        because non-container Ants don't have the self.ant attribute"""
        #If the container attribute of the Ant is True
        if self.container:
            #If it's currenty not containing any ant and the 'other' Ant is not also a container
            if self.ant is None and other.container is False:
                return True
            """If container Attribute is True but either there's an Ant being contained already
            or the 'other' Ant is a container"""
            return False
        else:
            return False

        # END Problem 9


class HarvesterAnt(Ant):
    """HarvesterAnt produces 1 additional food per turn for the colony."""

    name = 'Harvester'
    implemented = True
    food_cost = 2

    def action(self, colony):
        """Produce 1 additional food for the COLONY.

        colony -- The AntColony, used to access game state information.
        """
        # BEGIN Problem 1
        """A few notes:
        1. In the tests, note that INITIALIZING an Ant doesn't cost food. Deploying an Ant in the
        game simulation does.
        2. When an action involves the colony, we call it with colony.something, NOT
        self.colony.something."""
        colony.food += 1
        # END Problem 1


class ThrowerAnt(Ant):
    """ThrowerAnt throws a leaf each turn at the nearest Bee in its range."""

    name = 'Thrower'
    implemented = True
    food_cost = 3
    damage = 1
    min_range = 0 
    max_range = float('inf') #default max_range is infinity

    def nearest_bee(self, hive):
        """Return the nearest Bee in a Place that is not the HIVE, connected to
        the ThrowerAnt's Place by following entrances.

        This method returns None if there is no such Bee (or none in range).

        The word RANDOM here doesn't mean it'll throw a leaf to a random bee in front of it. Imagine there are 2 or more bees
        in the same place. Then the ThrowerAnt will throw leaf at a random bee among the 2 or more bees that's in that Place.

        Hint from -u: 
        1. You can get the Place object in front of another Place object by taking the Place's entrance
        instance attribute.
        2. The entrance of the first Place in a tunnel is The Hive
        3. If there is no Bee in front of the ThrowerAnt in the tunnel, nearest_bee function should
        return None.

        Additional hint:
        1. The class Insect has an instance attribute 'place'.
        2. This ants.py file imported random module

        =================== Below is what the test look like: ========================
        >>> from ants import *
        >>> hive, layout = Hive(AssaultPlan()), dry_layout
        >>> dimensions = (1, 9)
        >>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
        >>> # Testing nearest_bee
        >>> thrower = ThrowerAnt()
        >>> near_bee = Bee(2) # A Bee with 2 armor
        >>> far_bee = Bee(3)  # A Bee with 3 armor
        >>> ant_place = colony.places['tunnel_0_0']
        >>> near_place = colony.places['tunnel_0_3']
        >>> far_place = colony.places['tunnel_0_6']
        >>> ant_place.add_insect(thrower)
        >>> near_place.add_insect(near_bee)
        >>> far_place.add_insect(far_bee)
        >>> nearest_bee = thrower.nearest_bee(colony.hive)
        ***Note above that nearest_bee should return the near_bee
        >>> nearest_bee.armor
        2
        ***Above: The ThrowerAnt haven't done any action yet, so the armor should be still full
        >>> thrower.action(colony)    # Attack! ThrowerAnts do 1 damage
        >>> near_bee.armor
        1
        ***Above: since nearest_bee refers to the near_bee, currently the armor of nearest_bee = 
        the armor of near_bee = 1
        """

        # BEGIN Problem 3 and 4
        """
        We can't change self.place because if we do, that means we're changing
        the ThrowerAnt's place. Instead, we'll use a variable that keeps track
        of the selected place."""
        current_selected_place = self.place
        """
        In addition to currently selected place, we'll implement a place COUNTER
        to make sure nearest_bee works within the range."""
        current_place_counter = 0
        #This while loop runs until current_place_counter is greater than max_range
        while current_place_counter <= self.max_range:
            #If the current selected place is hive, then return None
            if current_selected_place is hive:
                return None
            else:
                # If the bees list isn't empty and if the counter is equal or greater than the minimum range
                if len(current_selected_place.bees) > 0 and self.min_range <= current_place_counter:
                    #Below statement basically returns a random bee within the bee list
                    return random.choice(current_selected_place.bees)
                #If there's no bee in the current selected place, update it to its entrance
                else:
                    current_selected_place = current_selected_place.entrance
                    current_place_counter +=1 
        #The while loop ends when counter reaches outside max_range. When this happens, return None.
        return None

        # END Problem 3 and 4

    def throw_at(self, target):
        """Throw a leaf at the TARGET Bee, reducing its armor."""
        if target is not None:
            target.reduce_armor(self.damage)

    def action(self, colony):
        """Throw a leaf at the nearest Bee in range."""
        self.throw_at(self.nearest_bee(colony.hive))

def random_or_none(s):
    """Return a random element of sequence S, or return None if S is empty."""
    if s:
        return random.choice(s)


##############
# Extensions #
##############

class Water(Place):
    """Water is a place that can only hold 'watersafe' insects.
    The followings are hint from ok -u:
    1. When an Insect is added to a Water Place, if the Insect is not watersafe,
    its armor is reduced to 0. Otherwise, nothing happens
    2. The reduce_armor method in the Insect class deals damage to
    an Insect and removes it from its place if its armor reaches 0
    
    """


    def add_insect(self, insect):
        """Add INSECT if it is watersafe, otherwise reduce its armor to 0."""
        # BEGIN Problem 11
        #First, we add the insect
        Place.add_insect(self, insect)
        #And then if the insect is not watersafe, execute 'instant kill' method
        if not insect.watersafe:
            insect.reduce_armor(insect.armor)
        # END Problem 11


class FireAnt(Ant):
    """FireAnt cooks any Bee in its Place when it expires."""

    """Hints from ok -u:
    1. We can obtain the current place of FireAnt by accessing the place instance attribute, which is
    a Place object
    2. We can obtain all of the Bees currently in some place by accessing the bees instance attribute, 
    which is a list of Bee objects
    3. We can iterate over a list while mutating it, but we should iterate over a copy of the
    list to avoid skipping elements (i.e. current_selected_place at ThrowerAnt problem)

    >>> from ants import *
    >>> hive, layout = Hive(AssaultPlan()), dry_layout
    >>> dimensions = (1, 9)
    >>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
    >>> # Testing fire does damage to all Bees in its Place
    >>> place = colony.places['tunnel_0_4']
    >>> place.add_insect(FireAnt())   # Add a FireAnt with 1 armor
    >>> place.add_insect(Bee(3))      # Add a Bee with 3 armor
    >>> place.add_insect(Bee(5))      # Add a Bee with 5 armor
    >>> len(place.bees)               # How many bees are there?
    2

    >>> place.bees[0].action(colony)  # The first Bee attacks FireAnt
    >>> len(place.bees)               # How many bees are left?
    1
    ***Only 1 bee is left because when the first Bee attacks FireAnt, the FireAnt dies and
    the FireAnt does it action: reducing all bees armor by 3.

    >>> place.bees[0].armor           # What is the armor of the remaining Bee?
    2"""

    name = 'Fire'
    damage = 3
    food_cost = 5
    # BEGIN Problem 5
    implemented = True   # Change to True to view in the GUI
    # END Problem 5

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and remove the FireAnt from its place if it
        has no armor remaining. If the FireAnt dies, damage each of the bees in
        the current place.
        """
        # BEGIN Problem 5
        copy = list(self.place.bees) #Create a copy of the bees list
        self.armor -= amount
        if self.armor <= 0:
            for bee in copy:
                bee.reduce_armor(self.damage)
            self.place.remove_insect(self)
        
        """Explanation: If we didn't create a copy of self.place.bees and iterates
        directly each bee in self.place.bees, when the first bee dies and got deleted,
        the second bee moves to the first bee's index. When this happens, the second bee
        "escaped" from the reduce_armor iteration.

        Meanwhile, if we create a copy of self.place.bees and iterate through the copy,
        if we try to interactively test the code, it'll be as the following:

        >>> hive, layout = Hive(AssaultPlan()), dry_layout
        >>> dimensions = (1, 9)
        >>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
        >>> place = colony.places['tunnel_0_4']
        >>> place.add_insect(FireAnt())
        >>> place.add_insect(Bee(3))
        >>> place.add_insect(Bee(5))
        >>> copy = list(place.bees)
        >>> copy
        [Bee(3, tunnel_0_4), Bee(5, tunnel_0_4)]
        >>> place.bees
        [Bee(3, tunnel_0_4), Bee(5, tunnel_0_4)]
        >>> place.bees[0].action(colony)
        Bee(tunnel_0_4) ran out of armor and expired
        >>> place.bees
        [Bee(2, tunnel_0_4)]
        >>> copy
        [Bee(0, None), Bee(2, tunnel_0_4)]

        Notice that the first bee in place.bees is gone, but it's still present in the copy. However
        in 'copy', the armor of the 1st bee shows as 0 and the location is None. This way, the 2nd
        bee won't be able to "escape" from the reduce_armor iteration"""
            
        # END Problem 5


class LongThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at least 5 places away."""

    name = 'Long'
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    food_cost = 2
    min_range = 5
    # END Problem 4


class ShortThrower(ThrowerAnt):
    """A ThrowerAnt that only throws leaves at Bees at most 3 places away."""

    name = 'Short'
    # BEGIN Problem 4
    implemented = True   # Change to True to view in the GUI
    food_cost = 2
    max_range = 3
    # END Problem 4


# BEGIN Problem 8
# The WallAnt class
class WallAnt(Ant):
    """A WallAnt does nothing each turn but it has 4 armor value"""

    """Hint from ok -u:
    1. The WallAnt class inherits from Ant class
    2. A WallAnt takes no action each turn
    3. Ant subclasses inherit the action method from the Insect class
    (If you look up Insect's action method, it actually does nothing)
    4. If a subclass Ant does not override the action method, the default
    action is nothing"""
    name = 'Wall'
    implemented = True
    food_cost = 4

    """Need to override the Insect's 'armor' method so that we can set
    the armor to 4"""
    def __init__(self):
        Ant.__init__(self, 4)
    
# END Problem 8


class NinjaAnt(Ant):
    """NinjaAnt does not block the path and damages all bees in its place."""

    name = 'Ninja'
    damage = 1
    # BEGIN Problem 7
    implemented = True   # Change to True to view in the GUI
    food_cost = 5
    blocks_path = False
    # END Problem 7

    def action(self, colony):
        # BEGIN Problem 7
        copy = list(self.place.bees)
        for bee in copy:
            bee.reduce_armor(self.damage)
        # END Problem 7


# BEGIN Problem 12
# The ScubaThrower class
class ScubaThrower(ThrowerAnt):
    """Basically a ThrowerAnt that is watersafe"""
    name = "Scuba"
    food_cost = 6
    implemented = True
    watersafe = True

# END Problem 12


class HungryAnt(Ant):
    """HungryAnt will take three turns to digest a Bee in its place.
    While digesting, the HungryAnt can't eat another Bee.
    """
    name = 'Hungry'
    # BEGIN Problem 6
    implemented = True   # Change to True to view in the GUI
    food_cost = 4
    time_to_digest = 3 #How man turns it take to digest a bee
    # END Problem 6

    """Hint from ok -u:
    1. 'digesting' should be an instance attribute instead of class attribute
    because each HungryAnt instance digests independently of other 
    HungryAnt instances.
    2. A HungryAnt is able to eat a Bee when it is not digesting (i.e. when
    its digesting attribute is 0)
    3. When a HungryAnt is able to eat, it eats a random Bee in the same
    place as itself"""

    def __init__(self):
        # BEGIN Problem 6
        Ant.__init__(self, armor=1)
        """ 'digesting' indicates whether the HungryAnt is currently digesting
        or not. If 'digesting' is greater than 0, it means it is currently
        digesting an ant"""
        self.digesting = 0
        # END Problem 6

    def eat_bee(self, bee):
        # BEGIN Problem 6
        """Since we're calling another object's method, we don't need
        to input the 'self' as an argument.
        The statement below basically means reduce the bee's armor
        by the amount of armor that bee currently has (instant kill)"""
        bee.reduce_armor(bee.armor)
        # END Problem 6

    def action(self, colony):
        # BEGIN Problem 6
        #If HungryAnt is still digesting, then the action decrements digesting by 1
        if self.digesting > 0:
            self.digesting -= 1
        else:
            #If there are currently at least a bee in the same place as the HungryAnt
            if len(self.place.bees) > 0:
                self.eat_bee(random.choice(self.place.bees))
                #Reset the digesting back to 'time_to_digest'
                self.digesting = self.time_to_digest
        # END Problem 6


class BodyguardAnt(Ant):
    """BodyguardAnt provides protection to other Ants."""
    name = 'Bodyguard'
    # BEGIN Problem 9
    implemented = True   # Change to True to view in the GUI
    food_cost = 4
    # END Problem 9
    container = True

    """Hint from ok -u:
    1. BodyguardAnt guard its ant by hiding the ant from Bees and acting
    in its place
    2. The Ant contained by a BodyguardAnt is stored In the Bodyguard's
    ant instance attribute
    3. 2 Ant instances are allowed to occupy the same Place when
    exactly one of the Ant instances is a container and the container ant
    does not already contain another ant
    4. If 2 Ants occupy the same Place, the container Ant is stored in
    that place's ant"""

    def __init__(self):
        Ant.__init__(self, 2)
        """self.ant represents the Ant that's being contained. When we first
        created BodyguardAnt, it starts with None"""
        self.ant = None  # The Ant hidden in this bodyguard

    def contain_ant(self, ant):
        # BEGIN Problem 9
        """This method sets the Ant that's being contained to be the passed
        'ant' argument"""
        self.ant = ant
        # END Problem 9

    def action(self, colony):
        # BEGIN Problem 9
        #Case 1: If BodyguardAnt currently doesn't contain any Ant
        if not self.ant:
            # Do nothing
            pass
        #Case 2: If BodyguardAnt currently containing an Ant
        else:
            # Execute the contained Ant's action
            self.ant.action(colony)
        # END Problem 9

class TankAnt(BodyguardAnt):
    """TankAnt provides both offensive and defensive capabilities."""
    name = 'Tank'
    damage = 1
    # BEGIN Problem 10
    implemented = True   # Change to True to view in the GUI
    food_cost = 6
    # END Problem 10

    #Hint from ok -u:
    # The only difference between a TankAnt and a BodyguardAnt is that
    # a TankAnt does damage to all Bees in its place each turn

    def action(self, colony):
        # BEGIN Problem 10
        #Does the BodyguardAnt's action
        BodyguardAnt.action(self, colony)
        # and damage each bees in place by 1
        copy = list(self.place.bees)
        for bee in copy:
            bee.reduce_armor(self.damage)

        # END Problem 10

# BEGIN Problem 13
class QueenAnt(ScubaThrower):  # You should change this line
# END Problem 13
    """The Queen of the colony. The game is over if a bee enters her place.
    
    Hints from ok -u:
    1. QueenAnt inherits from ScubaThrower Ant
    2. The first QueenAnt that is instantiated is the true QueenAnt
    3. The armor of any QueenAnt instance that is instantiated after the first one
    is reduced to 0 upon taking the first action
    4. Each turn, the true QueenAnt attacks the nearest bee and doubles the damage
    of all the ants behind her (that haven't already doubled)
    5. Bees win the game if either a Bee reaches the end of a tunnel or the 
    true QueenAnt dies
    """

    name = 'Queen'
    # BEGIN Problem 13
    implemented = True   # Change to True to view in the GUI
    food_cost = 7
    number_of_queens = 0
    #ants_upgraded is a list that contains all the Ants behind the QueenAnt 
    # whose damages are doubled
    ants_upgraded = []

    # END Problem 13

    def __init__(self):
        # BEGIN Problem 13
        ScubaThrower.__init__(self, armor=1)
        QueenAnt.number_of_queens += 1
        self.true_queen = True
        if QueenAnt.number_of_queens > 1:
            self.true_queen = False
        # END Problem 13

    def action(self, colony):
        """A queen ant throws a leaf, but also doubles the damage of ants
        in her tunnel.

        Impostor queens do only one thing: reduce their own armor to 0.
        """
        # BEGIN Problem 13
        # Make sure the fake queen's only action is dying. The fake queen doesn't even get to throw a leaf
        if not self.true_queen:
            self.reduce_armor(self.armor)
            return
        ScubaThrower.action(self, colony)
        #Starts iterating through each place behind QueenAnt
        current_selected_place = self.place
        while current_selected_place is not None:
            #If there is an Ant present in the place (it's not None)
            if current_selected_place.ant is not None:
                # If the Ant in the currently selected place is not a QueenAnt
                if not current_selected_place.ant.name is "Queen":
                    #If the Ant in the currently selected place is a container
                    if current_selected_place.ant.container:
                        #If the container is a Tank
                        if current_selected_place.ant.name is 'Tank':
                            #If the Tank hasn't been upgraded yet
                            if current_selected_place.ant not in QueenAnt.ants_upgraded:
                                current_selected_place.ant.damage *= 2
                                QueenAnt.ants_upgraded.append(current_selected_place.ant)
                        #(NOTE: This still runs even though the container is a Tank.
                        # If there is an Ant being contained
                        if current_selected_place.ant.ant is not None:
                            #If the Ant being contained hasn't been upgraded yet
                            if current_selected_place.ant.ant not in QueenAnt.ants_upgraded:
                                current_selected_place.ant.ant.damage *= 2
                                QueenAnt.ants_upgraded.append(current_selected_place.ant.ant)
                    #If the Ant in the currently selected place is not in a container and hasn't been upgraded
                    elif current_selected_place.ant not in QueenAnt.ants_upgraded:
                        current_selected_place.ant.damage *= 2
                        QueenAnt.ants_upgraded.append(current_selected_place.ant)
            current_selected_place = current_selected_place.exit

        # END Problem 13

    def reduce_armor(self, amount):
        """Reduce armor by AMOUNT, and if the True QueenAnt has no armor
        remaining, signal the end of the game.
        """
        # BEGIN Problem 13
        self.armor -= amount
        if self.armor <= 0:
            if self.true_queen:
                bees_win()
            self.place.remove_insect(self)
        # END Problem 13

class AntRemover(Ant):
    """Allows the player to remove ants from the board in the GUI."""

    name = 'Remover'
    implemented = False

    def __init__(self):
        Ant.__init__(self, 0)


##################
# Status Effects #
##################

""" Test from ok -u:
>>> from ants import *
>>> hive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
>>> # Testing if effects stack
>>> stun = StunThrower()
>>> bee = Bee(3)
>>> stun_place = colony.places["tunnel_0_0"]
>>> bee_place = colony.places["tunnel_0_4"]
>>> stun_place.add_insect(stun)
>>> bee_place.add_insect(bee)
>>> for _ in range(4): # stun bee four times
...    stun.action(colony)
>>> passed = True
>>> for _ in range(4):
...    bee.action(colony)
...    if bee.place.name != 'tunnel_0_4':
...        passed = False
>>> passed
True

>>> from ants import *
>>> hive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
>>> # Testing multiple stuns
>>> stun1 = StunThrower()
>>> stun2 = StunThrower()
>>> bee1 = Bee(3)
>>> bee2 = Bee(3)
>>> colony.places["tunnel_0_0"].add_insect(stun1)
>>> colony.places["tunnel_0_1"].add_insect(bee1)
>>> colony.places["tunnel_0_2"].add_insect(stun2)
>>> colony.places["tunnel_0_3"].add_insect(bee2)
>>> stun1.action(colony)
>>> stun2.action(colony)
>>> bee1.action(colony)
>>> bee2.action(colony)
>>> bee1.place.name
"tunnel_0_1"
>>> bee2.place.name
"tunnel_0_3"
>>> bee1.action(colony)
>>> bee2.action(colony)
>>> bee1.place.name
"tunnel_0_0"
>>> bee2.place.name
"tunnel_0_2"

>>> from ants import *
>>> hive, layout = Hive(AssaultPlan()), dry_layout
>>> dimensions = (1, 9)
>>> colony = AntColony(None, hive, ant_types(), layout, dimensions)
>>> # Testing long effect stack
>>> stun = StunThrower()
>>> slow = SlowThrower()
>>> bee = Bee(3)
>>> colony.places["tunnel_0_0"].add_insect(stun)
>>> colony.places["tunnel_0_1"].add_insect(slow)
>>> colony.places["tunnel_0_4"].add_insect(bee)
>>> for _ in range(3): # slow bee three times
...    slow.action(colony)
>>> stun.action(colony) # stun bee once
>>> colony.time = 0
>>> bee.action(colony) # stunned
>>> bee.place.name
"tunnel_0_4"
>>> colony.time = 1
>>> bee.action(colony) # slowed thrice
>>> bee.place.name
"tunnel_0_4"
>>> colony.time = 2
>>> bee.action(colony) # slowed thrice
>>> bee.place.name
"tunnel_0_3"
>>> colony.time = 3
>>> bee.action(colony) # slowed twice
>>> bee.place.name
"tunnel_0_3"
>>> colony.time = 4
>>> bee.action(colony) # slowed twice
>>> bee.place.name
"tunnel_0_2"
>>> colony.time = 5
>>> bee.action(colony) # slowed once
>>> bee.place.name
"tunnel_0_2"
>>> colony.time = 6
>>> bee.action(colony) # slowed once
>>> bee.place.name
"tunnel_0_1"
>>> colony.time = 7
>>> bee.action(colony) # status effects have worn off
>>> slow.armor
0"""

def make_slow(action):
    """Return a new action method that calls ACTION every other turn.

    action -- An action method of some Bee
    """
    # BEGIN Problem EC
    def new_action(colony):
        #If colony.time is even, then the bee can do action normally
        if colony.time % 2 == 0:
            return action(colony)
    return new_action
    # END Problem EC

def make_stun(action):
    """Return a new action method that does nothing.

    action -- An action method of some Bee
    """
    # BEGIN Problem EC
    def new_action(colony):
        pass
    return new_action
    # END Problem EC

def apply_effect(effect, bee, duration):
    """Apply a status effect to a BEE that lasts for DURATION turns."""
    # BEGIN Problem EC
    
    turn = 0 #if turn = duration, then the status ailment wear off
    new = effect(bee.action)
    old = bee.action
    def replace_action(colony):
        nonlocal turn
        #as long as turn < duration, the status ailment is still in effect, so the bee
        # still do the new action
        if turn < duration:
            new(colony)
        #if turn = duration, then the bee action goes back to normal
        else:
            old(colony)
        turn += 1
    
    bee.action = replace_action

    # END Problem EC


class SlowThrower(ThrowerAnt):
    """ThrowerAnt that causes Slow on Bees."""

    name = 'Slow'
    # BEGIN Problem EC
    implemented = True   # Change to True to view in the GUI
    food_cost = 4
    # END Problem EC

    def throw_at(self, target):
        if target:
            apply_effect(make_slow, target, 3)


class StunThrower(ThrowerAnt):
    """ThrowerAnt that causes Stun on Bees."""

    name = 'Stun'
    # BEGIN Problem EC
    implemented = True   # Change to True to view in the GUI
    food_cost = 6
    # END Problem EC

    def throw_at(self, target):
        if target:
            apply_effect(make_stun, target, 1)


##################
# Bees Extension #
##################

class Wasp(Bee):
    """Class of Bee that has higher damage."""
    name = 'Wasp'
    damage = 2

class Hornet(Bee):
    """Class of bee that is capable of taking two actions per turn, although
    its overall damage output is lower. Immune to status effects.
    """
    name = 'Hornet'
    damage = 0.25

    def action(self, colony):
        for i in range(2):
            if self.armor > 0:
                super().action(colony)

    def __setattr__(self, name, value):
        if name != 'action':
            object.__setattr__(self, name, value)

class NinjaBee(Bee):
    """A Bee that cannot be blocked. Is capable of moving past all defenses to
    assassinate the Queen.
    """
    name = 'NinjaBee'

    def blocked(self):
        return False

class Boss(Wasp, Hornet):
    """The leader of the bees. Combines the high damage of the Wasp along with
    status effect immunity of Hornets. Damage to the boss is capped up to 8
    damage by a single attack.
    """
    name = 'Boss'
    damage_cap = 8
    action = Wasp.action

    def reduce_armor(self, amount):
        super().reduce_armor(self.damage_modifier(amount))

    def damage_modifier(self, amount):
        return amount * self.damage_cap/(self.damage_cap + amount)

class Hive(Place):
    """The Place from which the Bees launch their assault.

    assault_plan -- An AssaultPlan; when & where bees enter the colony.
    """

    def __init__(self, assault_plan):
        self.name = 'Hive'
        self.assault_plan = assault_plan
        self.bees = []
        for bee in assault_plan.all_bees:
            self.add_insect(bee)
        # The following attributes are always None for a Hive
        self.entrance = None
        self.ant = None
        self.exit = None

    def strategy(self, colony):
        exits = [p for p in colony.places.values() if p.entrance is self]
        for bee in self.assault_plan.get(colony.time, []):
            bee.move_to(random.choice(exits))
            colony.active_bees.append(bee)


class AntColony(object):
    """An ant collective that manages global game state and simulates time.

    Attributes:
    time -- elapsed time
    food -- the colony's available food total
    queen -- the place where the queen resides
    places -- A list of all places in the colony (including a Hive)
    bee_entrances -- A list of places that bees can enter
    """

    def __init__(self, strategy, hive, ant_types, create_places, dimensions, food=2):
        """Create an AntColony for simulating a game.

        Arguments:
        strategy -- a function to deploy ants to places
        hive -- a Hive full of bees
        ant_types -- a list of ant constructors
        create_places -- a function that creates the set of places
        dimensions -- a pair containing the dimensions of the game layout
        """
        self.time = 0
        self.food = food
        self.strategy = strategy
        self.hive = hive
        self.ant_types = OrderedDict((a.name, a) for a in ant_types)
        self.dimensions = dimensions
        self.active_bees = []
        self.configure(hive, create_places)

    def configure(self, hive, create_places):
        """Configure the places in the colony."""
        self.queen = QueenPlace('AntQueen')
        self.places = OrderedDict()
        self.bee_entrances = []
        def register_place(place, is_bee_entrance):
            self.places[place.name] = place
            if is_bee_entrance:
                place.entrance = hive
                self.bee_entrances.append(place)
        register_place(self.hive, False)
        create_places(self.queen, register_place, self.dimensions[0], self.dimensions[1])

    def simulate(self):
        """Simulate an attack on the ant colony (i.e., play the game)."""
        num_bees = len(self.bees)
        try:
            while True:
                self.hive.strategy(self)            # Bees invade
                self.strategy(self)                 # Ants deploy
                for ant in self.ants:               # Ants take actions
                    if ant.armor > 0:
                        ant.action(self)
                for bee in self.active_bees[:]:     # Bees take actions
                    if bee.armor > 0:
                        bee.action(self)
                    if bee.armor <= 0:
                        num_bees -= 1
                        self.active_bees.remove(bee)
                if num_bees == 0:
                    raise AntsWinException()
                self.time += 1
        except AntsWinException:
            print('All bees are vanquished. You win!')
            return True
        except BeesWinException:
            print('The ant queen has perished. Please try again.')
            return False

    def deploy_ant(self, place_name, ant_type_name):
        """Place an ant if enough food is available.

        This method is called by the current strategy to deploy ants.
        """
        constructor = self.ant_types[ant_type_name]
        if self.food < constructor.food_cost:
            print('Not enough food remains to place ' + ant_type_name)
        else:
            ant = constructor()
            self.places[place_name].add_insect(ant)
            self.food -= constructor.food_cost
            return ant

    def remove_ant(self, place_name):
        """Remove an Ant from the Colony."""
        place = self.places[place_name]
        if place.ant is not None:
            place.remove_insect(place.ant)

    @property
    def ants(self):
        return [p.ant for p in self.places.values() if p.ant is not None]

    @property
    def bees(self):
        return [b for p in self.places.values() for b in p.bees]

    @property
    def insects(self):
        return self.ants + self.bees

    def __str__(self):
        status = ' (Food: {0}, Time: {1})'.format(self.food, self.time)
        return str([str(i) for i in self.ants + self.bees]) + status

class QueenPlace(Place):
    """QueenPlace at the end of the tunnel, where the queen resides."""

    def add_insect(self, insect):
        """Add an Insect to this Place.

        Can't actually add Ants to a QueenPlace. However, if a Bee attempts to
        enter the QueenPlace, a BeesWinException is raised, signaling the end
        of a game.
        """
        assert not insect.is_ant, 'Cannot add {0} to QueenPlace'
        raise BeesWinException()

def ants_win():
    """Signal that Ants win."""
    raise AntsWinException()

def bees_win():
    """Signal that Bees win."""
    raise BeesWinException()

def ant_types():
    """Return a list of all implemented Ant classes."""
    all_ant_types = []
    new_types = [Ant]
    while new_types:
        new_types = [t for c in new_types for t in c.__subclasses__()]
        all_ant_types.extend(new_types)
    return [t for t in all_ant_types if t.implemented]

class GameOverException(Exception):
    """Base game over Exception."""
    pass

class AntsWinException(GameOverException):
    """Exception to signal that the ants win."""
    pass

class BeesWinException(GameOverException):
    """Exception to signal that the bees win."""
    pass

def interactive_strategy(colony):
    """A strategy that starts an interactive session and lets the user make
    changes to the colony.

    For example, one might deploy a ThrowerAnt to the first tunnel by invoking
    colony.deploy_ant('tunnel_0_0', 'Thrower')
    """
    print('colony: ' + str(colony))
    msg = '<Control>-D (<Control>-Z <Enter> on Windows) completes a turn.\n'
    interact(msg)

def start_with_strategy(args, strategy):
    """Reads command-line arguments and starts a game with those options."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Ants vs. SomeBees")
    parser.add_argument('-d', type=str, metavar='DIFFICULTY',
                        help='sets difficulty of game (test/easy/medium/hard/insane)')
    parser.add_argument('-w', '--water', action='store_true',
                        help='loads a full layout with water')
    parser.add_argument('--food', type=int,
                        help='number of food to start with when testing', default=2)
    args = parser.parse_args()

    assault_plan = make_normal_assault_plan()
    layout = dry_layout
    tunnel_length = 9
    num_tunnels = 3
    food = args.food

    if args.water:
        layout = wet_layout
    if args.d in ['t', 'test']:
        assault_plan = make_test_assault_plan()
        num_tunnels = 1
    elif args.d in ['e', 'easy']:
        assault_plan = make_easy_assault_plan()
        num_tunnels = 2
    elif args.d in ['n', 'normal']:
        assault_plan = make_normal_assault_plan()
        num_tunnels = 3
    elif args.d in ['h', 'hard']:
        assault_plan = make_hard_assault_plan()
        num_tunnels = 4
    elif args.d in ['i', 'insane']:
        assault_plan = make_insane_assault_plan()
        num_tunnels = 4

    hive = Hive(assault_plan)
    dimensions = (num_tunnels, tunnel_length)
    return AntColony(strategy, hive, ant_types(), layout, dimensions, food).simulate()


###########
# Layouts #
###########

def wet_layout(queen, register_place, tunnels=3, length=9, moat_frequency=3):
    """Register a mix of wet and and dry places."""
    for tunnel in range(tunnels):
        exit = queen
        for step in range(length):
            if moat_frequency != 0 and (step + 1) % moat_frequency == 0:
                exit = Water('water_{0}_{1}'.format(tunnel, step), exit)
            else:
                exit = Place('tunnel_{0}_{1}'.format(tunnel, step), exit)
            register_place(exit, step == length - 1)

def dry_layout(queen, register_place, tunnels=3, length=9):
    """Register dry tunnels."""
    wet_layout(queen, register_place, tunnels, length, 0)


#################
# Assault Plans #
#################

class AssaultPlan(dict):
    """The Bees' plan of attack for the Colony.  Attacks come in timed waves.

    An AssaultPlan is a dictionary from times (int) to waves (list of Bees).

    >>> AssaultPlan().add_wave(4, 2)
    {4: [Bee(3, None), Bee(3, None)]}
    """

    def add_wave(self, bee_type, bee_armor, time, count):
        """Add a wave at time with count Bees that have the specified armor."""
        bees = [bee_type(bee_armor) for _ in range(count)]
        self.setdefault(time, []).extend(bees)
        return self

    @property
    def all_bees(self):
        """Place all Bees in the hive and return the list of Bees."""
        return [bee for wave in self.values() for bee in wave]

def make_test_assault_plan():
    return AssaultPlan().add_wave(Bee, 3, 2, 1).add_wave(Bee, 3, 3, 1)

def make_easy_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 3, time, 1)
    plan.add_wave(Wasp, 3, 4, 1)
    plan.add_wave(NinjaBee, 3, 8, 1)
    plan.add_wave(Hornet, 3, 12, 1)
    plan.add_wave(Boss, 15, 16, 1)
    return plan

def make_normal_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 3, time, 2)
    plan.add_wave(Wasp, 3, 4, 1)
    plan.add_wave(NinjaBee, 3, 8, 1)
    plan.add_wave(Hornet, 3, 12, 1)
    plan.add_wave(Wasp, 3, 16, 1)

    #Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Bee, 3, time, 2)
    plan.add_wave(Wasp, 3, 22, 2)
    plan.add_wave(Hornet, 3, 24, 2)
    plan.add_wave(NinjaBee, 3, 26, 2)
    plan.add_wave(Hornet, 3, 28, 2)
    plan.add_wave(Boss, 20, 30, 1)
    return plan

def make_hard_assault_plan():
    plan = AssaultPlan()
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 4, time, 2)
    plan.add_wave(Hornet, 4, 4, 2)
    plan.add_wave(Wasp, 4, 8, 2)
    plan.add_wave(NinjaBee, 4, 12, 2)
    plan.add_wave(Wasp, 4, 16, 2)

    #Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Bee, 4, time, 3)
    plan.add_wave(Wasp, 4, 22, 2)
    plan.add_wave(Hornet, 4, 24, 2)
    plan.add_wave(NinjaBee, 4, 26, 2)
    plan.add_wave(Hornet, 4, 28, 2)
    plan.add_wave(Boss, 30, 30, 1)
    return plan

def make_insane_assault_plan():
    plan = AssaultPlan()
    plan.add_wave(Hornet, 5, 2, 2)
    for time in range(3, 16, 2):
        plan.add_wave(Bee, 5, time, 2)
    plan.add_wave(Hornet, 5, 4, 2)
    plan.add_wave(Wasp, 5, 8, 2)
    plan.add_wave(NinjaBee, 5, 12, 2)
    plan.add_wave(Wasp, 5, 16, 2)

    #Boss Stage
    for time in range(21, 30, 2):
        plan.add_wave(Bee, 5, time, 3)
    plan.add_wave(Wasp, 5, 22, 2)
    plan.add_wave(Hornet, 5, 24, 2)
    plan.add_wave(NinjaBee, 5, 26, 2)
    plan.add_wave(Hornet, 5, 28, 2)
    plan.add_wave(Boss, 30, 30, 2)
    return plan


from utils import *
@main
def run(*args):
    Insect.reduce_armor = class_method_wrapper(Insect.reduce_armor,
            pre=print_expired_insects)
    start_with_strategy(args, interactive_strategy)
