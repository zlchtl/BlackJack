import random
import os
import time

class Card:
    def __init__(self, id: int, suit: str, denomination: str, weight: int, _open: bool = False):
        self.id = id
        self.suit = suit
        self.weight = weight
        self.open = _open
        self.denomination = denomination
        self.s = suit + denomination

    def __repr__(self):
        return self.s

    def __str__(self):
        return self.s

class Deck:
    def __init__(self, seed = None):
        self.deck = []
        self.restart(seed)

    def __len__(self):
        return len(self.deck)

    def __repr__(self):
        return ' '.join(map(lambda x: f'\t|id={x.id} x={x}|', self.deck))

    def __str__(self):
        return ' '.join(map(str, self.deck))

    def remote(self, _id: int):
        self.deck = list(filter(lambda x: x.id != _id, self.deck))
        return self.deck

    def get(self,_id:int = -1):
        if len(self.deck) == 0:
            return
        if _id == -1:
            card = random.choice(self.deck)
        else:
            card = self.deck[_id]
        self.remote(card.id)
        return card

    def restart(self, seed = None):
        random.seed(seed)
        _id = 0
        weight = (2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11)
        for i in ('♠', '♥', '♦', '♣'):
            for j, jc in enumerate(('2','3','4','5','6', '7', '8', '9', '10', 'J', 'Q', 'K', 'T')):
                self.deck.append(Card(_id, i, jc, weight[j]))
                _id += 1

class Player:
    def __init__(self, name = 'anonymous'):
        self.name = f'PLAYER: {name}'
        self.hand = []

    def restart(self):
        self.hand = []

    def sum(self):
        _sum = 0
        hand = sorted(self.hand, key = lambda x: x.weight)
        for card in hand:
            if card.weight == 11 and _sum + card.weight > 21 and card.open:
                _sum += 1
            elif card.open:
                _sum += card.weight
            else:
                _sum += 0
        return _sum

class Dealer(Player):
    def __init__(self, name = '???'):
        super().__init__()
        self.name = f'DEALER: {name}'

class Manager:
    def __init__(self, seed = None):
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck(seed)
        while self.start():
            self.restart()

    def restart(self):
        self.deck.restart()
        self.dealer.restart()
        self.player.restart()

    def out_entity(self,entity, clr: bool = False):
        if clr:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(entity.name,'\n  ',end='')
        for card in entity.hand:
            if card.open:
                print(f'{card}', end=' ')
            else:
                print(f'??', end=' ')
        print(f'\nsum = {entity.sum()}\n')

    def out_command(self, *commands):
        for command in commands:
            print(command)
        return input()

    def addCard(self, entity, _open: bool = True):
        card = self.deck.get()
        if _open:
            card.open = True
        entity.hand.append(card)

    def start(self):
        self.addCard(self.dealer, False)
        self.addCard(self.dealer)
        self.addCard(self.player)
        self.addCard(self.player)
        return self.main()

    def main(self):
        while True:
            self.out_entity(self.dealer, True)
            self.out_entity(self.player)
            command = self.out_command('1.Take', '2.Stay', '3.Restart', '4.Exit')
            match command:
                case '1':
                    self.addCard(self.player)
                case '2':
                    break
                case '3':
                    return True
                case '4':
                    return False
                case _:
                    print('CommandError')

        self.dealer.hand[0].open = True

        while True:
            self.out_entity(self.dealer, True)
            self.out_entity(self.player)
            time.sleep(1)
            l = list(map(lambda x: x.weight, self.dealer.hand))
            l = [i  if i != 11 else 1 for i in l]
            s = self.dealer.sum()
            ps = self.player.sum()
            if 21 >= ps and s<21 and s<ps:
                self.addCard(self.dealer)
            elif 21 >= ps and sum(l)<21 and sum(l)<ps:
                self.addCard(self.dealer)
            else:
                break

        if (self.player.sum() < self.dealer.sum() <= 21) or self.player.sum() > 21:
            print('YOU LOSE')
        elif self.dealer.sum() == self.player.sum():
            print('DRAW')
        else:
            print('YOU WIN')
        input()
        return True

Manager()