# %%
from game import *
import random
# %%
class Alex_bot(Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def get_play(self):
        return('p', random.randint(0,7))
    def get_draw(self):
        return('d', False)
# %%
game = LostCity(players = [('Erin', Alex_bot), ('Alex', Alex_bot)])
# %%
game.play()
# %%
