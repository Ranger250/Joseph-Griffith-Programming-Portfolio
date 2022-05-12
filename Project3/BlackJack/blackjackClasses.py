import card as c
import hands as h
from commonGameFunctions import *


class Bj_Card(c.Pos_card):
    ACE_VALUE = 1

    @property
    def value(self):
        if self.face_up:
            v = Bj_Card.RANK.index(self.rank) + 1
            if v > 10:
                v = 10

        else:
            v = None

        return v


class Bj_Hand(h.Hand):

    def __init__(self, name):
        super(Bj_Hand, self).__init__()
        self.name = name

    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None

        # add up card values, treat each ace as 1
        t = 0
        for c in self.cards:
            t+=c.value
        # determine if hand contains an Ace
        contains_ace = False
        for c in self.cards:
            if c.value == Bj_Card.ACE_VALUE:
                contains_ace = True
        if contains_ace and t <= 11:
            t += 10
        return t

    def fliphand(self):
        for card in self.cards:
            card.face_up = True

    def is_busted(self):
        return self.total > 21

    def __str__(self):
        rep = h.Hand.__str__(self)
        rep += self.name+"\t"+"("+str(self.total)+")"
        return rep


class Bj_Deck(h.Deck):

    def populate(self):
        for suit in Bj_Card.SUIT:
            for rank in Bj_Card.RANK:
                temp_card = Bj_Card(rank, suit)
                self.add(temp_card)



class Bj_Player(Bj_Hand):

    def is_hitting(self):
        response = ask_yes_no("\n" + self.name + ", do you want a hit? (Y/N): ")
        return response == "yes"

    def lose(self):
        print(self.name, "loses.")

    def win(self):
        print(self.name, "wins.")

    def push(self):
        print(self.name, "pushes.")

    def bust(self):
        print(self.name, "busts")
        self.lose()




class Bj_Dealer(Bj_Hand):

    def is_hitting(self):
        soft = True
        for card in self.cards:
            if card.value >= 10:
                soft = False
        if self.total < 17 or (self.total == 17 and soft):
            return True
        else:
            return False

    def bust(self):
        print(self.name, "busts")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class Bj_Game(object):

    def __init__(self, names):
        self.players = []
        for name in names:
            player = Bj_Player(name)
            self.players.append(player)
        self.dealer = Bj_Dealer("Dealer Eric")
        self.deck = Bj_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards__(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            player.fliphand()
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):
        self.deck.deal(self.players+[self.dealer], per_hand=2)
        self.dealer.flip_first_card()
        for hand in self.players:
            hand.fliphand()

        for player in self.players:
            print(player)

        print(self.dealer)

        for player in self.players:
            print(player)
            self.__additional_cards__(player)
        if not self.still_playing:
            self.dealer.fliphand()
            print(self.dealer)
        else:
            self.dealer.fliphand()
            print(self.dealer)
            self.__additional_cards__(self.dealer)

        if self.dealer.is_busted():
            for player in self.still_playing:
                player.win()
        else:
            for player in self.still_playing:
                if player.total > self.dealer.total:
                    player.win()
                elif player.total < self.dealer.total:
                    player.lose()
                else:
                    player.push()

        for player in self.players:
            player.clear()
        self.dealer.clear()
