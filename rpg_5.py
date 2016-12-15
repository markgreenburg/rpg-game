"""
RPG text game with some different characters and items. Hero can carry items in
inventory and use them in battle as needed
"""
import random
import time

class Character(object):
    '''
    Class definition for all in-game characters
    '''
    def __init__(self):
        self.name = '<undefined>'
        self.health = 10
        self.power = 5
        self.coins = 20

    def alive(self):
        '''
        Checks health of character and returns True if greater than 0
        '''
        return self.health > 0

    def attack(self, enemy_char):
        '''
        Method by which character attacks another character.
        Damage is dictated by character's hitpoints
        '''
        if not self.alive():
            return
        print "%s attacks %s" % (self.name, enemy_char.name)
        enemy_char.receive_damage(self.power)
        time.sleep(1.5)

    def receive_damage(self, points):
        '''
        Method by which character receives damage during attack.
        Decrements character's health counter.
        '''
        self.health -= points
        print "%s received %d damage." % (self.name, points)
        if self.health <= 0:
            print "%s is dead." % self.name

    def print_status(self):
        '''
        Prints the current health and power of a given character.
        '''
        print "%s has %d health and %d power." % (self.name, self.health, self.power)

class Hero(Character):
    '''
    The main game character. Has special attribute and mods in
    receive_damage for incorporating armor.
    adding armor to self.
    '''

    def __init__(self):
        super(Hero, self).__init__()
        self.name = 'hero'
        self.health = 10
        self.coins = 20
        self.power = 5
        self.reset_power = self.power
        self.armor = 0
        self.evade = 0
        self.max_evade = 18
        self.using_shield = False
        self.inventory = {'armor': 0, 'evade': 0, 'reflective shield': 0,\
        'tonic': 0, 'super tonic': 0, 'sword': 0}

    def attack(self, enemy_char):
        '''
        Hero's attack class differs from super in that hero has
        20 percent chance of doubling power during each attack
        '''
        # Set up 1 in 5 chance of doing double damage
        double_power = random.random() < .2
        if double_power:
            self.power *= 2
            print "%s attacks with double power!!!" % self.name
        # Is hero using a shield to reflect enemy's attack?
        if self.using_shield:
            print "Reflecting %s's attack back to %s!" % (enemy_char.name, enemy_char.name)
            # Add enemy's power to own power
            self.power += enemy_char.power
        super(Hero, self).attack(enemy_char)
        # Reset shield power
        if self.using_shield:
            self.power -= enemy_char.power
        # Reset double power
        if double_power:
            self.power /= 2

    def receive_damage(self, points):
        '''
        Before calling super method, need to account for armor in
        determining by how much to decrease health. Also takes into account evade power.
        '''
        # Determine if hero evaded attack
        evades_attack = random.random() < (self.evade * .05)
        # If attack evaded, hero receives no damage
        if evades_attack:
            print "%s evades attack and receives no damage!" % self.name
        # If attack not evaded, subtract armor from points to get
        # total damage (but can't be less than 0)
        else:
            if points - self.armor < 0 or self.using_shield:
                points = 0
            else:
                points -= self.armor
            # Then call the super receive_damage method
            super(Hero, self).receive_damage(points)
        # Reset powers in case shield used on last turn. Shield
        # is lost even if attack was evaded
        self.using_shield = False

    def receive_bounty(self, enemy_char):
        '''
        Increase coin count by amount of enemy character's bounty
        '''
        self.coins += enemy_char.bounty

    def restore(self):
        '''
        Restores health to 10. If original health > 10, method does nothing.
        '''
        if self.health < 10:
            self.health = 10
            print "%s's health is restored to %d!" % (self.name, self.health)
        else:
            print "%s's health is already restored!" % self.name
        time.sleep(1)

    def buy(self, item):
        '''
        Deducts item cost from Hero's coin bank and adds bought item to
        inventory. If character doesn't have enough money left, purchase won't
        go through.
        '''
        if self.coins - item.cost >= 0:
            self.coins -= item.cost
            self.inventory[item.name] += 1
            # item.apply(hero)
        else:
            print "Not enough money to buy %s!" % item.name

    def apply_item(self):
        '''
        This method controls the logic for displaying and applying items to
        character from inventory. Also deducts items from character's inventory
        once applied.
        '''
        while True:
            print "====================="
            print "Pick an item to apply"
            print "====================="
            for i in range(len(Store.items)):
                item = Store.items[i]
                print "%d: %s (%d)" % (i + 1, item.name, self.inventory[item.name])
            print "10. leave"
            user_input = int(raw_input("> "))
            if user_input == 10:
                break
            else:
                itm_to_apply = Store.items[user_input - 1]
                instantiated_itm = itm_to_apply()
                if self.inventory[instantiated_itm.name] > 0:
                    instantiated_itm.apply(self)
                    self.inventory[instantiated_itm.name] -= 1
                else:
                    print "%s doesn't have any %s!" % (self.name, user_input)

class Goblin(Character):
    '''
    Goblin character subclass. Goblin has no special features, items, or
    attacks.
    '''
    def __init__(self):
        super(Goblin, self).__init__()
        self.name = 'goblin'
        self.health = 6
        self.power = 2
        self.bounty = 8

class Wizard(Character):
    '''
    Wizard character subclass. Wizards have 50 percent chance of swapping power
    with whatever character is attacking them. This behavior is defined in them
    attack method.
    '''
    def __init__(self):
        super(Wizard, self).__init__()
        self.name = 'wizard'
        self.health = 8
        self.power = 1
        self.bounty = 10

    def attack(self, enemy_char):
        '''
        Defines character's attack of another character. Wizard attack method
        has 50 percent chance of swapping power with player being attacked.
        Power resets after turn.
        '''
        swap_power = random.random() > 0.5
        if swap_power:
            print "%s swaps power with %s during attack" % (self.name, enemy_char.name)
            self.power, enemy_char.power = enemy_char.power, self.power
        super(Wizard, self).attack(enemy_char)
        if swap_power:
            self.power, enemy_char.power = enemy_char.power, self.power

class Shadow(Character):
    '''
    Shadow character subclass. Shadow character's special ability is dodging
    attacks ninety percent of the time.
    '''
    def __init__(self):
        super(Shadow, self).__init__()
        self.name = 'shadow'
        self.health = 1
        self.power = 2
        self.bounty = 12

    def receive_damage(self, points):
        '''
        Method for receiving damage for the Shadow character subclass. Shadow
        has a ninety percent chance of dodging each attack.
        '''
        if random.random() < .1:
            super(Shadow, self).receive_damage(points)
        else:
            print "%s dodged your attack and received no damage!" % (self.name)

class Medic(Character):
    '''
    Medic character subclass. Medic character has special ability to recoup
    two health after an attack twenty percent of the time.
    '''
    def __init__(self):
        super(Medic, self).__init__()
        self.name = 'medic'
        self.health = 6
        self.power = 1
        self.bounty = 8

    def receive_damage(self, points):
        if random.random() < .2:
            print "%s recuperated two hitpoints!!!" % self.name
            points -= 2
        super(Medic, self).receive_damage(points)

class Zombie(Character):
    '''
    Zombie character subclass. Zombies never die, regardless of remaining
    health. This special ability is defined in the Zombie's alive() method.
    '''
    def __init__(self):
        super(Zombie, self).__init__()
        self.name = 'zombie'
        self.health = 8
        self.power = 2
        self.bounty = 60

    def alive(self):
        '''
        Zombie never dies, so always returns true.
        '''
        return True

class Battle(object):
    '''
    Battle class controls the flow of each individual battle between characters.
    It also contains all of the decision logic that a player must choose
    between during each battle (fight, flee, apply item, pass).
    '''

    @staticmethod
    def do_battle(hero_char, enemy_char):
        '''
        Performs a battle between a hero character and a given enemy character.
        Battle continues until player exits, or one of the characters is not
        alive().
        '''
        print "====================="
        print "Hero faces the %s" % enemy_char.name
        print "====================="
        while hero_char.alive() and enemy_char.alive():
            hero_char.print_status()
            enemy_char.print_status()
            time.sleep(1.5)
            print "-----------------------"
            print "What do you want to do?"
            print "1. fight %s" % enemy_char.name
            print "2. do nothing"
            print "3. flee"
            print "4. apply item from inventory"
            print "> ",
            user_input = int(raw_input())
            if user_input == 1:
                hero_char.attack(enemy_char)
            elif user_input == 2:
                pass
            elif user_input == 3:
                print "Goodbye."
                exit(0)
            elif user_input == 4:
                hero_char.apply_item()
            else:
                print "Invalid input %r" % user_input
                continue
            enemy_char.attack(hero_char)
        if hero_char.alive():
            hero_char.receive_bounty(enemy_char)
            print "You defeated the %s and received a bounty of %d coins" \
            % (enemy_char.name, enemy_char.bounty)
            return True
        else:
            print "YOU LOSE!"
            return False

class Tonic(object):
    '''
    Tonic is an item available for purchase in the Store. Raises a character's
    health by two health points and is applied with the Apply() method.
    '''
    cost = 5
    name = 'tonic'

    @staticmethod
    def apply(character):
        '''
        Method for applying the Tonic's health effects to a character. Increases
        a character's health by 2 health points.
        '''
        character.health += 2
        print "%s's health increased to %d." % (character.name, character.health)

class SuperTonic(object):
    '''
    SuperTonic is an item available for purchase in the Store. Raises a
    character's health by 10 health points, by calling the Tonic class's
    apply() method multiple times. Change is sticky.
    '''
    cost = 20
    name = 'super tonic'

    @staticmethod
    def apply(character):
        '''
        Method for applying the SuperTonic's health effects to a character.
        Increases health by 10 by calling its parent Tonic's super apply() five
        times.
        '''
        character.health += 10
        print "%s's health increased to %d." % (character.name, character.health)

class Sword(object):
    '''
    Sword is an item available for purchase in the Store. Raises a character's
    power by 2 hit points. Change is sticky.
    '''
    cost = 10
    name = 'sword'

    @staticmethod
    def apply(hero_char):
        '''
        Method for applying the Sword's health effects to a character. Raises
        character's power by 2 points.
        '''
        hero_char.power += 2
        print "%s's power increased to %d." % (hero_char.name, hero_char.power)

class Armor(object):
    '''
    Armor is an item available for purchase in the Store. Raises a character's
    armor by 2 points, which aids in deflecting attack power.
    '''
    cost = 5
    name = 'armor'

    @staticmethod
    def apply(hero_char):
        '''
        Method by which armor is applied to a character. Increases character's
        armor by 2.
        '''
        hero_char.armor += 2
        print "%s's armor increased to %s." % (hero_char.name, hero_char.armor)

class Evade(object):
    '''
    Evade is an item available for purchase in the Store. Each time evade is
    applied, character's evasion increases by 2 to help character dodge attack.
    '''
    cost = 10
    name = 'evade'

    @classmethod
    def apply(cls, hero_char):
        '''
        Method to apply evade item to character. Increases character's evasion
        by 2 up to a max limit of 18.
        '''
        if hero_char.evade >= hero_char.max_evade:
            print "Hero is already at max evasion!"
            print "No money used"
            hero_char.coins += cls.cost
        else:
            hero_char.evade += 2
            print "%s's evade increased to %d." % (hero_char.name, hero_char.evade)

class ReflectShield(object):
    '''
    Single-use item abailable for purchase in the Store. Steals enemy's power
    for the turn and adds it to the attacking character's power. After one
    attack, uses itself up and disables itself.
    '''
    cost = 25
    name = 'reflective shield'
    used = False

    def apply(self, hero_char):
        '''
        Method to apply Reflectie Shield to character. Adds enemy's power to
        attacker's power for the turn, then uses itself up. Powers are resets
        for each character separately in the hero's attack method.
        '''
        if not self.used:
            print "%s now has a %s" % (hero_char.name, self.name)
            hero_char.using_shield = True
            self.used = True
        else:
            print "This %s has already been used!" % self.name

class Store(object):
    '''
    The in-game item store. Displays store, and the items within. Character
    can choose which items to buy and can then exit the store when done or out
    of money.
    '''
    items = [Armor, Evade, ReflectShield, Tonic, SuperTonic, Sword]

    @classmethod
    def do_shopping(cls, hero_char):
        '''
        Main store method that displays the store and items for purchase. Allows
        player to pick items from which to buy.
        '''
        while True:
            print "====================="
            print "Welcome to the store!"
            print "====================="
            print "You have %d coins." % hero_char.coins
            print "What do you want to do?"
            for i in xrange(len(cls.items)):
                item = cls.items[i]
                print "%d. buy %s (%d)" % (i + 1, item.name, item.cost)
            print "10. leave"
            user_input = int(raw_input("> "))
            if user_input == 10:
                break
            else:
                item_to_buy = cls.items[user_input - 1]
                item = item_to_buy()
                hero_char.buy(item)

def main():
    '''
    Runs the RPG game
    '''
    hero = Hero()
    enemies = [Goblin(), Wizard(), Medic(), Shadow(), Zombie()]
    battle_engine = Battle()
    shopping_engine = Store()
    for enemy in enemies:
        hero_won = battle_engine.do_battle(hero, enemy)
        if not hero_won:
            print "YOU LOSE!"
            exit(0)
        shopping_engine.do_shopping(hero)
    print "YOU WIN!"

if __name__ == "__main__":
    main()
