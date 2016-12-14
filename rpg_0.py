"""
In this simple RPG game, the hero fights the goblin. He has the options to:

1. fight goblin
2. do nothing - in which case the goblin will attack him anyway
3. flee
"""

class Character(object):
    '''
    Super class for all in-game characters.
    '''
    health = 1
    power = 1
    name = "Default Name"
    words = ("has", "does")

    def attack(self, who):
        '''
        Allows current character to attack any other character,
        subtracting the current character's power from the target
        character's health. Prints attack's damage details.
        '''
        who.health -= self.power
        print "%s %s %d damage to %s." % (self.name, self.words[1], self.power, who.name)

    def alive(self):
        '''
        Checks whether the current character is alive. Returns bool.
        '''
        if self.health > 0:
            return True
        else:
            return False

    def print_alive(self):
        '''
        Prints death notice for current character if no health left.
        '''
        if not self.alive():
            print "%s died!" % self.name

    def print_health(self):
        '''
        Prints the current character's health and power
        '''
        print "%s %s %d health and %d power." % (self.name, self.words[0], self.health, self.power)

class Hero(Character):
    '''
    Hero character. Presets health, power, name, and modified words
    '''
    health = 10
    power = 5
    name = "You"
    words = ("have", "do")

class Goblin(Character):
    '''
    Goblin character. Presets health, power, name, and modified words
    '''
    health = 6
    power = 2
    name = "Goblin"
    words = ("has", "does")

def main():
    '''
    Runs the game
    '''
    hero = Hero()
    goblin1 = Goblin()
    while goblin1.alive() and hero.alive():
        # prints health first, so we don't print negative once dead
        hero.print_health()
        goblin1.print_health()
        print
        print "What do you want to do?"
        print "1. fight goblin"
        print "2. do nothing"
        print "3. flee"
        print "> ",
        user_choice = raw_input()
        if user_choice == "1":
            hero.attack(goblin1)
        elif user_choice == "2":
            goblin1.attack(hero)
        elif user_choice == "3":
            print "Goodbye."
            break
        else:
            print "Invalid input %r" % user_choice
        hero.print_alive()
        goblin1.print_alive()
main()
