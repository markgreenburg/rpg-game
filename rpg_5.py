"""
Added a store. The hero can now buy a tonic or a sword. A tonic will add 2 to the hero's health wherease a sword will add 2 power.
"""
import random
import time

class Character(object):
    name = '<undefined>'
    health = 10
    power = 5
    coins = 20
    def alive(self):
        return self.health > 0

    def attack(self, enemy_char):
        if not self.alive():
            return
        print "%s attacks %s" % (self.name, enemy_char.name)
        enemy_char.receive_damage(self.power)
        time.sleep(1.5)

    def receive_damage(self, points):
        self.health -= points
        print "%s received %d damage." % (self.name, points)
        if self.health <= 0:
            print "%s is dead." % self.name

    def print_status(self):
        print "%s has %d health and %d power." % (self.name, self.health, self.power)

class Hero(Character):
    name = 'hero'
    health = 10
    power = 5
    coins = 20
    armor = 0
    def __init__(self):
        super(Hero, self).__init__()
        self.base_power = self.power
        self.double_power = self.power * 2

    def attack(self, enemy_char):
        # Set up 1 in 5 chance of doing double damage
        if random.randint(1,5) == 1:
            self.power = self.double_power
            print "%s attacks with double power!!!" % self.name
        super(Hero, self).attack(enemy_char)
        # Reset damage
        self.power = self.base_power

    def receive_damage(self, points):
        points -= self.armor
        super(Hero, self).receive_damage(points)

    def restore(self):
        self.health = 10
        print "Hero's heath is restored to %d!" % self.health
        time.sleep(1)

    def buy(self, item):
        self.coins -= item.cost
        item.apply(hero)

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
        if random.randint(1, 10) == 1:
            super(Shadow, self).receive_damage(points)
        else:
            print "%s dodged your attack and received no damage!" % (self.name)

class Medic(Character):
    name = 'medic'
    health = 6
    power = 1
    bounty = 8
    def receive_damage(self, points):
        if random.randint(1, 5) == 1:
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
            print "> ",
            user_input = int(raw_input())
            if user_input == 1:
                hero_char.attack(enemy_char)
            elif user_input == 2:
                pass
            elif user_input == 3:
                print "Goodbye."
                exit(0)
            else:
                print "Invalid input %r" % user_input
                continue
            enemy_char.attack(hero_char)
        if hero_char.alive():
            print "You defeated the %s" % enemy_char.name
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

class Store(object):
    # If you define a variable in the scope of a class:
    # This is a class variable and you can access it like
    # Store.items => [Tonic, Sword]
    items = [Tonic, Sword]
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
enemies = [Goblin(), Wizard()]
battle_engine = Battle()
shopping_engine = Store()

for enemy in enemies:
    hero_won = battle_engine.do_battle(hero, enemy)
    if not hero_won:
        print "YOU LOSE!"
        exit(0)
    shopping_engine.do_shopping(hero)

print "YOU WIN!"
