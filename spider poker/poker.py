
# coding: utf-8

# In[65]:


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        self.show = False
    def print_card(self):
        print(self.suit + ' ' + str(self.number))


# In[66]:


class Poker:
    def __init__(self, included_suits, number_for_each_suit, number_for_jokers):
        self.suits = included_suits
        self.number = number_for_each_suit
        self.joker = number_for_jokers
        self.cards = []
    def check_card(self, suit, number): 
        # Poker.check_card() checks if a card is in the pool; if a card is invalid, return INVALID_CARD
        # Poker.check_card(): Str Int -> anyof(Bool, INVALID_CARD)
        if number < 1 or number > 13 or suit not in self.suits:
            return 'INVALID_CARD'
        else:
            for card in self.cards:
                if suit == card.suit and number == card.number:
                    return True
            return False
    def get_card(self, suit, number):
        # Poker.get_card(suit, number) draws a card in the pool and returns it; if it's not in the pool, return false
        # if invalid, return INVALID_CARD
        # Poker.get_card(): Str Int -> Card
        if check_card(self, suit, number) == True:
            card = Card(suit, number)
            self.cards.remove(card)
            return card
        else:
            return check_card(self, suit, number)
    def draw_card(self):
        # Poker.draw_card() draws the first card in the pool and returns it; if
        # the cardpool is empty, return false
        # Poker.draw_card(): None -> anyof (Card, False)
        if len(self.cards) == 0:
            return False
        else:
            card = self.cards[0]
            self.cards.pop(0)
            return card
    def fill_cards(self):
        # Poker.fill_cards() refreshes the cardpool to contain the included suits with the given number of times
        self.cards = []
        for suit in self.suits:
            for num in range (self.number):
                for i in range (1, 14):
                    card = Card(suit, i)
                    self.cards.append(card)
    def add_card(self, card):
        # Poker.add_card(suit, number) adds a card to the cardpool
        self.cards.append(card)
    
