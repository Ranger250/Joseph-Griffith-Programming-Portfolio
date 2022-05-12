class Player(object):
    __player_count = 0
    def __init__(self):
        Player.__player_count += 1
        self.health = 3
        self.attack_dmg = 1

    def __show_player_count__():
        print(Player.__player_count)

    def die(self):
        if self.health <= 0:
            print("the player has died")

    def shoot(self, target, dmg):
        target.take_dmg(dmg)

    def take_dmg(self, dmg):
        self.health -= dmg
        self.die()


class Alien(object):
    def __init__(self):
        self.health = 3
        self.attack_dmg = 1

    def die(self):
        if self.health <= 0:
            print("the enemy has died")

    def take_dmg(self, dmg):
        self.health -= dmg
        self.die()

    def shoot(self, target, dmg):
        target.take_dmg(dmg)

player = Player()
enemy = Alien()

player.shoot(enemy, player.attack_dmg)
player.shoot(enemy, player.attack_dmg)
player.shoot(enemy, player.attack_dmg)
