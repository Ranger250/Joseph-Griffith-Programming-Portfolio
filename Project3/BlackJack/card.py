class Card(object):

    RANK = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUIT = ["♣", "♦", "♥", "♠"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = str.format("""
        -------------
        | {0}{1}       |
        |           |
        |           |
        |           |
        |           |
        |           |
        |       {1}{0} |
        -------------
        """, self.rank, self.suit)
        return rep


class Pos_card(Card):
    def __init__(self, rank, suit):
        super(Pos_card, self).__init__(rank, suit)
        self.face_up = False

    def __str__(self):
        if self.face_up:
            rep = super(Pos_card,self).__str__()
        else:
            rep = """
                                -------------
                                |♣  ♦   ♥  ♠|
                                |♦  ♥   ♠  ♣|
                                |♥  ♠   ♣  ♦|
                                |♠  ♣   ♦  ♥|
                                |♣  ♦   ♥  ♠|
                                |♦  ♥   ♠  ♣|
                                |♥  ♠   ♣  ♦|
                                -------------
                                """
        return rep

    def flip(self):
        self.face_up = not self.face_up


if __name__ == "__main__":
    print("this is not a program try importing and using the classes")
    input("\n\nPress the enter key to exit.")
