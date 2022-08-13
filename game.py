# %%
import random
# %%
class Deck(): # 还没发的牌
    def __str__(self):
        return('\n'.join(['---- Deck info -----',
            f'Cards dealt: {self.dealt}',
            f'Cards remaining: {self.count()}']))
    def __init__(self, num_of_color):
        nums = [0, 0, 0] + list(range(2,11))
        full_deck = [(c, num) for c in range(num_of_color) for num in nums]
        random.shuffle(full_deck)
        self._deck = full_deck
        self.dealt = 0 # the number of 已经发了的扑克牌
    def deal(self):
        if self.dealt >= len(self._deck):
            return(False)
        card = self._deck[self.dealt]
        self.dealt += 1
        return(card)
    def count(self):
        return(len(self._deck) - self.dealt)
class Player():
    
    def __str__(self):
        self.hand.sort()
        return('\n'.join([
            f'----- Round {self.round} Player {self.name} info -----',
            f'Player hand: {[(i, c, num) for i, (c, num) in enumerate(self.hand)]}',
            f'Player maps: {self.maps}'
        ]))
    def __init__(self, name, num_of_color, deck, discard, game):
        self.game = game
        self.name = name
        self.hand = []
        self.maps = [[] for _ in range(num_of_color)]
        self.deck = deck
        self.discard = discard
        self.round = 0
    def play(self, i):
        self.round += 1
        color, num = self.hand[i]
        if len(self.maps[color]) == 0 or self.maps[color][-1] < num:
            self.maps[color].append(num)
            del self.hand[i]
        else:
            return(False)

    def trash(self, i):
        color, num = self.hand[i]
        self.discard[num].append(color)
        del self.hand[i]

    def draw(self):
        self.hand.append(self.deck.deal())

    def steal(self, color):
        self.hand.append(self.discard[color].pop())
    
    def tally(self):
        score = 0
        for col in self.maps:
            if col:
                score += (sum(col) - 20) * (col.count(0) + 1)
        return(score)
    def get_play(self):
        todo = input(f'What do you want to do, {self.name}? >')
        if ' ' in todo:
            action, card = todo.split(' ')
        return(action, card)
    def get_draw(self):
        todo = input(f'What next, {self.name}? >')
        if todo == 'd':
            return(todo, False)
        else:
            action, color = todo.split(' ')
            return(action, color)

class LostCity:
    def __str__(self):
        for player in self.players:
            print(player)
        print('\n'.join([
            '----- Discarded -----',
            f'{self.discard}'
        ]))
        return('')
    def __init__(self, num_of_color = 5, initial_deal = 8, players = [('Erin', Player), ('Alex', Player)]):
        self.deck = Deck(num_of_color)
        self.discard = [[] for _ in range(num_of_color)]
        self.players = [bot(name, num_of_color, self.deck, self.discard, self) 
                            for name, bot in players]
        for _ in range(initial_deal):
            for player in self.players:
                player.draw()
    def play(self):
        i = 1
        while self.deck.count() > 0:
            for player in self.players:

                #print(self)
                action, target = player.get_play()
                if action == 'p':
                    player.play(target)
                elif action == 't':
                    player.trash(target)
                
                #print(self)
                action, target = player.get_draw()
                if action == 'd':
                    player.draw()
                elif action == 's':
                    player.steal(target)
            i += 1
        print(f'**** Game ends in {i} rounds ****')
        for player in self.players:
            print(f'{player.name}: {player.tally()}')

# %%