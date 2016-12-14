"""
Added a store. The hero can now buy a tonic or a sword. A tonic will add 2 to the hero's health wherease a sword will add 2 power.
"""
import random
import time

class Character(object):
    '''
    Class definition for all in-game characters
    '''
    name = '<undefined>'
    health = 10
    power = 5
    coins = 20
    def alive(self):
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
    name = 'hero'
    health = 10
    coins = 20
    power = 5
    reset_power = power
    armor = 0
    evade = 0
    max_evade = 18
    using_shield = False
    inventory = {'armor': 0, 'evade': 0, 'reflective shield': 0, 'tonic': 0, 'super tonic': 0, 'sword': 0}

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
        self.coins += enemy_char.bounty

    def restore(self):
        self.health = 10
        print "%s's heath is restored to %d!" % (self.name, self.health)
        time.sleep(1)

    def buy(self, item):
        if self.coins - item.cost >=0:
            self.coins -= item.cost
            self.inventory[item.name] += 1
            # item.apply(hero)
        else:
            print "Not enough money to buy %s!" % item.name

    def apply_item(self):
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

# {'armor': 0, 'evade': 0, 'reflective shield': 0, 'tonic': 0, 'super tonic': 0, 'sword': 0}

# inventory = {Armor: 0, Evade: 0, ReflectiveShield: 0, Tonic: 0, SuperTonic: 0, Sword: 0}


class Goblin(Character):
    name = 'goblin'
    health = 6
    power = 2
    bounty = 8

class Wizard(Character):
    name = 'wizard'
    health = 8
    power = 1
    bounty = 10
    def attack(self, enemy_char):
        swap_power = random.random() > 0.5
        if swap_power:
            print "%s swaps power with %s during attack" % (self.name, enemy_char.name)
            self.power, enemy_char.power = enemy_char.power, self.power
        super(Wizard, self).attack(enemy_char)
        if swap_power:
            self.power, enemy_char.power = enemy_char.power, self.power

class Shadow(Character):
    name = 'shadow'
    health = 1
    power = 2
    bounty = 12
    def receive_damage(self, points):
        if random.random() < .1:
            super(Shadow, self).receive_damage(points)
        else:
            print "%s dodged your attack and received no damage!" % (self.name)

class Medic(Character):
    name = 'medic'
    health = 6
    power = 1
    bounty = 8
    def receive_damage(self, points):
        if random.random() < .2:
            print "%s recuperated two hitpoints!!!" % self.name
            points -= 2
        super(Medic, self).receive_damage(points)

class Zombie(Character):
    name = 'zombie'
    health = 8
    power = 2
    bounty = 60
    def alive(self):
        return True

class Battle(object):
    def do_battle(self, hero_char, enemy_char):
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
            hero.receive_bounty(enemy_char)
            print "You defeated the %s and received a bounty of %d coins" % (enemy_char.name, enemy_char.bounty)
            return True
        else:
            print "YOU LOSE!"
            return False

class Tonic(object):
    cost = 5
    name = 'tonic'
    def apply(self, character):
        character.health += 2
        print "%s's health increased to %d." % (character.name, character.health)

class SuperTonic(Tonic):
    cost = 20
    name = 'super tonic'
    def apply(self, character):
        for _ in range(5):
            super(SuperTonic, self).apply(character)

class Sword(object):
    cost = 10
    name = 'sword'
    def apply(self, hero_char):
        hero_char.power += 2
        print "%s's power increased to %d." % (hero_char.name, hero_char.power)

class Armor(object):
    cost = 5
    name = 'armor'
    def apply(self, hero_char):
        hero_char.armor += 2
        print "%s's armor increased to %s." % (hero_char.name, hero_char.armor)

class Evade(object):
    cost = 10
    name = 'evade'
    def apply(self, hero_char):
        if hero_char.evade >= hero_char.max_evade:
            print "Hero is already at max evasion!"
            print "No money used"
            hero_char.coins += self.cost
        else:
            hero_char.evade += 2
            print "%s's evade increased to %d." % (hero_char.name, hero_char.evade)

class ReflectShield(object):
    cost = 25
    name = 'reflective shield'
    used = False
    def apply(self, hero_char):
        if not self.used:
            print "%s now has a %s" % (hero_char.name, self.name)
            hero_char.using_shield = True
            self.used = True
        else:
            print "This %s has already been used!" % self.name

class Store(object):
    # If you define a variable in the scope of a class:
    # This is a class variable and you can access it like
    # Store.items => [Tonic, Sword]
    items = [Armor, Evade, ReflectShield, Tonic, SuperTonic, Sword]
    def do_shopping(self, hero_char):
        while True:
            print "====================="
            print "Welcome to the store!"
            print "====================="
            print "You have %d coins." % hero_char.coins
            print "What do you want to do?"
            for i in xrange(len(Store.items)):
                item = Store.items[i]
                print "%d. buy %s (%d)" % (i + 1, item.name, item.cost)
            print "10. leave"
            user_input = int(raw_input("> "))
            if user_input == 10:
                break
            else:
                ItemToBuy = Store.items[user_input - 1]
                item = ItemToBuy()
                hero_char.buy(item)

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
