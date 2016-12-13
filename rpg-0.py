"""
In this simple RPG game, the hero fights the goblin. He has the options to:

1. fight goblin
2. do nothing - in which case the goblin will attack him anyway
3. flee

"""
class Character(object):
    health = 1
    power = 1
    name = "Default Name"
    words = ("has", "does")

    def attack(self, who):
        who.health -= self.power
        print "%s %s %d damage to %s." % (self.name, self.words[1], self.power, who.name)

    def alive(self):
        if self.health > 0:
            return True
        else:
            return False

    def print_alive(self):
        if not self.alive():
            print "%s died!" % self.name

    def print_health(self):
        print "%s %s %d health and %d power." % (self.name, self.words[0], self.health, self.power)

class Hero(Character):
    health = 10
    power = 5
    name = "You"
    words = ("have", "do")

class Goblin(Character):
    health = 6
    power = 2
    name = "Goblin"
    words = ("has", "does")

def main():
    hero = Hero()
    goblin1 = Goblin()
    while goblin1.alive() and hero.alive():
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
            # Goblin attacks hero
        hero.print_alive()
        goblin1.print_alive()
main()
