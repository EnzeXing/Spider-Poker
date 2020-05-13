
# coding: utf-8

import pygame, sys, random, poker
from pygame.locals import *
pygame.init()


# Global constants
# Gaming window
WINDOWWIDTH = 800
WINDOWHEIGHT = 800
BACKGROUNDCOLOR = (0, 100, 0)
WHITE = (255, 255, 255)
# Poker cards
CARDWIDTH = 60
CARDHEIGHT = 84
CARDDISTANCE = 10
textFont = pygame.font.SysFont(None, 20)
# Card blocks
TOPDISTANCE = 10
SIDEDISTANCE = 19
DISTANCE_BETWEEN_BLOCKS = 18
BLOCKNUMBER = 10
TOTAL_HANDS = 8
REST_BLOCKS = 5
FINISHED_HANDS = 0
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # Game window
pygame.display.set_caption('Spider Poker')
windowSurface.fill(BACKGROUNDCOLOR)
mainClock = pygame.time.Clock()
clicked_before = False


# Global variables for easy mode
suits = ['spade']
number_of_each_suit = int(TOTAL_HANDS / len(suits))
total_cardpool = poker.Poker(suits, number_of_each_suit, 0) 
total_cardpool.fill_cards()
random.shuffle(total_cardpool.cards)
INITIAL_NUMBER_OF_CARDS1 = 6 # The first four blocks all have 6 cards initially
INITIAL_NUMBER_OF_CARDS2 = 5 # The last six blocks all have 5 cards initially
mouse_pos_list = [] # records the mouse position when pressing the mouse



# create cardpools for each block
cardpool1 = poker.Poker(suits, number_of_each_suit, 0)
cardpool2 = poker.Poker(suits, number_of_each_suit, 0)
cardpool3 = poker.Poker(suits, number_of_each_suit, 0)
cardpool4 = poker.Poker(suits, number_of_each_suit, 0)
cardpool5 = poker.Poker(suits, number_of_each_suit, 0)
cardpool6 = poker.Poker(suits, number_of_each_suit, 0)
cardpool7 = poker.Poker(suits, number_of_each_suit, 0)
cardpool8 = poker.Poker(suits, number_of_each_suit, 0)
cardpool9 = poker.Poker(suits, number_of_each_suit, 0)
cardpool10 = poker.Poker(suits, number_of_each_suit, 0)
cardpool_list = [cardpool1, cardpool2, cardpool3, cardpool4, cardpool5, cardpool6, cardpool7, cardpool8, cardpool9, cardpool10]



# terminate() terminates the program
def terminate():
    pygame.quit()
    sys.exit()
    


# draw_text(text, font, surface, x, y, color) displays specific text ar the surface with upleft position (x, y)
def draw_text(text, font, surface, x, y, color):
    textSurface = font.render(text, 1, color)
    textRect = textSurface.get_rect()
    textRect.center = (x, y)
    surface.blit(textSurface, textRect)



# get_card_pos(carpool_index, card_index) gets the upleft position (x, y) for a specific card in a cardpool
def get_card_pos(carpool_index, card_index):
    pos_x = SIDEDISTANCE + carpool_index * (CARDWIDTH + DISTANCE_BETWEEN_BLOCKS)
    pos_y = TOPDISTANCE + card_index * CARDDISTANCE
    return [pos_x, pos_y]
    


# display_card(card, left, top, surface) displays a poker card on the surface at upleft position (left, top)
def display_card(card, left, top, surface):
    image_name = ''
    if card.show: # gets the corresponding jpg name for the card
        start = 0
        if card.suit == 'spade':
            start = 0
        elif card.suit == 'heart':
            start = 13
        elif card.suit == 'club':
            start = 26
        else:
            start = 39

        number = card.number
        if number == 1 or number == 2:
            number += 13
        number += start
        image_name = str(number) + '.jpg'
    else:
        image_name = '55.jpg'
    image_surface = pygame.image.load(image_name) # gets the surface object for the card
    image_surface = pygame.transform.scale(image_surface, (CARDWIDTH, CARDHEIGHT))
    image_rect = image_surface.get_rect()
    image_rect.top = top
    image_rect.left = left
    surface.blit(image_surface, image_rect) # draws the card surface at the given position
    pygame.display.update()
        


# distribute_initial_cards() randomly distributes card objects into cardpool
def distribute_initial_cards():
    for i in range (4):
        for j in range (INITIAL_NUMBER_OF_CARDS1): # distributes 6 card objects to the first 4 pools
            card = total_cardpool.draw_card() # gets a card object from the total_cardpool
            if card != False:
                cardpool_list[i].add_card(card)
        cardpool_list[i].cards[len(cardpool_list[i].cards) - 1].show = True # The last card should be displayed
    for i in range (4, len(cardpool_list)):
        for j in range (INITIAL_NUMBER_OF_CARDS2): # distributes 5 card objects to the rest 6 pools
            card = total_cardpool.draw_card()
            if card != False:
                cardpool_list[i].add_card(card)
        cardpool_list[i].cards[len(cardpool_list[i].cards) - 1].show = True
    


def draw_cardpool(cardpool_index): # draws the cards inside of the cardpool, given the index in the list
    card_list = cardpool_list[cardpool_index].cards
    
    if len(card_list) == 0: # no cards in the cardpool, draw a block instead
        card_pos = get_card_pos(cardpool_index, 0)
        rect = pygame.Rect(card_pos, (CARDWIDTH, CARDHEIGHT))
        pygame.draw.rect(windowSurface, WHITE, rect, 2)
    else:
        for i in range (len(cardpool_list[cardpool_index].cards)):
            card = cardpool_list[cardpool_index].cards[i]
            card_pos = get_card_pos(cardpool_index, i)
            display_card(card, card_pos[0], card_pos[1], windowSurface)
    


# draw_rest_pool() represents all the cards remained in total_cardpool by
# drawing 5 cards (not displayed) at the downright corner
def draw_rest_pool():
    bottom = WINDOWHEIGHT - TOPDISTANCE
    right = WINDOWWIDTH - SIDEDISTANCE
    image_name = '55.jpg' # The image of the back of the card
    for i in range (REST_BLOCKS):
        image_surface = pygame.image.load(image_name)
        image_surface = pygame.transform.scale(image_surface, (CARDWIDTH, CARDHEIGHT))
        image_rect = image_surface.get_rect()
        image_rect.bottom = bottom
        image_rect.right = right
        windowSurface.blit(image_surface, image_rect)
        right -= CARDDISTANCE
    pygame.display.update()



# initial_setting() finished all the initial setting for the game
def initial_setting():
    distribute_initial_cards() # Distribute the initial cards
    for i in range (len(cardpool_list)):
        draw_cardpool(i)
    draw_rest_pool()
    pygame.display.update()



# refer_mouse_pos_to_cardpools(pos) determines which cardpool the pos_x coordinates lie in
def refer_mouse_pos_to_cardpools(pos_x):
    cardpool1_pos_x = SIDEDISTANCE
    pool_num = (pos_x - cardpool1_pos_x) // (CARDWIDTH + DISTANCE_BETWEEN_BLOCKS)
    if (pool_num <= 0):
        return 0
    elif (pool_num >= 9):
        return 9
    else:
        return pool_num



# find_consecutive_cards(cardpool) returns an index x so that the cards between x and the end
# are the same suit with decreasing numbers of 1
# requires: cardpool.cards is not empty
def find_consecutive_cards(cardpool):
    assert len(cardpool.cards) > 0
    bottom_num = cardpool.cards[-1].number
    bottom_suit = cardpool.cards[-1].suit
    for i in range (len(cardpool.cards) - 2, -1, -1):
        if cardpool.cards[i].number == bottom_num + 1 and cardpool.cards[i].suit == bottom_suit and cardpool.cards[i].show == True:
            bottom_num += 1
        else:
            return i + 1
    return 0



# draw_moved_card_list(moved_card_list, x, y, surface) draws the moving list of cards
def draw_moved_card_list(moved_card_list, x, y, surface): 
    for card in moved_card_list:
        display_card(card, x, y, surface)
        y += CARDDISTANCE
    pygame.display.update()



# reset_display(moved_list_x, moved_list_y, moved_card_list, surface) redisplays the windowSurface after each drag
def reset_display(moved_list_x, moved_list_y, moved_card_list, surface):
    left_pool_num = refer_mouse_pos_to_cardpools(moved_list_x)
    right_pool_num = refer_mouse_pos_to_cardpools(moved_list_x + CARDWIDTH)
    draw_cardpool(left_pool_num)
    draw_cardpool(right_pool_num)
    draw_moved_card_list(moved_card_list, moved_list_x, moved_list_y, surface)



# test_if_redistribute(x, y) determines if the player clicks the remaining card pool to redistribute cards
def test_if_redistribute(x, y):
    bottom = WINDOWHEIGHT - TOPDISTANCE
    right = WINDOWWIDTH - SIDEDISTANCE
    rest_pool_rect = pygame.Rect((right, bottom), (CARDWIDTH + (REST_BLOCKS - 1) * CARDDISTANCE, CARDHEIGHT))
    rest_pool_rect.bottom = bottom
    rest_pool_rect.right = right
    return rest_pool_rect.collidepoint(x, y)



# redistribute_cards() adds 1 more card for each cardpool and displays it
def redistribute_cards():
    global REST_BLOCKS
    bottom = WINDOWHEIGHT - TOPDISTANCE
    right = WINDOWWIDTH - SIDEDISTANCE
    rest_pool_rect = pygame.Rect((right, bottom), (CARDWIDTH + (REST_BLOCKS - 1) * CARDDISTANCE, CARDHEIGHT))
    rest_pool_rect.bottom = bottom
    rest_pool_rect.right = right
    pygame.draw.rect(windowSurface, BACKGROUNDCOLOR, rest_pool_rect)
    REST_BLOCKS -= 1
    draw_rest_pool()
    for i in range (BLOCKNUMBER):
        card = total_cardpool.draw_card() # gets a card from total_cardpool
        card.show = True
        cardpool_list[i].cards.append(card) # adds the card
        left = SIDEDISTANCE + i * (DISTANCE_BETWEEN_BLOCKS + CARDWIDTH)
        top = TOPDISTANCE + (len(cardpool_list[i].cards) - 1) * CARDDISTANCE
        display_card(cardpool_list[i].cards[-1], left, top, windowSurface)



# finish_hands(dest_cardpool_index) is called when a total hand from A to K has been displayed in a
# cardpool, and removes the hand and displays it in the downleft corner as a K.
def finish_hands(dest_cardpool_index):
    suit = cardpool_list[dest_cardpool_index].cards[-1].suit
    for i in range (13):
        cardpool_list[dest_cardpool_index].cards.pop()
    if len(cardpool_list[dest_cardpool_index].cards) > 0:
        cardpool_list[dest_cardpool_index].cards[-1].show = True
    tail_pos = get_card_pos(dest_cardpool_index, len(cardpool_list[dest_cardpool_index].cards))
    height = 12 * CARDDISTANCE + CARDHEIGHT
    hand_rect = pygame.Rect(tail_pos[0], tail_pos[1], CARDWIDTH, height)
    pygame.draw.rect(windowSurface, BACKGROUNDCOLOR, hand_rect)
    global FINISHED_HANDS
    FINISHED_HANDS += 1
    draw_cardpool(dest_cardpool_index) 
    King = poker.Card(suit, 13)
    King.show = True
    left = SIDEDISTANCE + FINISHED_HANDS * CARDDISTANCE
    top = WINDOWHEIGHT - TOPDISTANCE - CARDHEIGHT
    display_card(King, left, top, windowSurface)
        


initial_setting()
while True:
    for event in pygame.event.get():
        if event.type == QUIT: # Press Esc to quit
            terminate()
        elif event.type == MOUSEBUTTONDOWN and test_if_redistribute(event.pos[0], event.pos[1]):
            # Mouse press the remaining cardpool to redistribute
            redistribute_cards()
        elif event.type == MOUSEBUTTONDOWN: # moves card
            clicked_before = True
            mouse_pos = pygame.mouse.get_pos() # gets the mouse position
            pool_num_moved = refer_mouse_pos_to_cardpools(mouse_pos[0]) # decides which cardpool to move
            cardpool_length = len(cardpool_list[pool_num_moved].cards)
            if cardpool_length > 0:
                initial_mouse_pos = mouse_pos
                first_moved_card_index = find_consecutive_cards(cardpool_list[pool_num_moved]) # decides the start of moved_card_list
                moved_card_list = cardpool_list[pool_num_moved].cards[first_moved_card_index:cardpool_length]
                initial_card_pos = get_card_pos(pool_num_moved, first_moved_card_index) # records the initial upleft pos of moved_card_list
                moved_card_list_pos = initial_card_pos[:]
                for i in range (first_moved_card_index, cardpool_length):
                    cardpool_list[pool_num_moved].cards.pop() # removes the cards from their current cardpool
                
        if event.type == MOUSEMOTION and clicked_before and cardpool_length > 0: # dragging the moved_card_list
            mouse_pos = pygame.mouse.get_pos()
            moved_card_list_height = (len(moved_card_list) - 1) * CARDDISTANCE + CARDHEIGHT
            moved_card_list_rect = pygame.Rect(moved_card_list_pos, (CARDWIDTH, moved_card_list_height)) # the current pos of moved_card_list
            pygame.draw.rect(windowSurface, BACKGROUNDCOLOR, moved_card_list_rect) # removes the initial moved_card_list surface
            moved_card_list_pos[0] = initial_card_pos[0] + mouse_pos[0] - initial_mouse_pos[0]
            moved_card_list_pos[1] = initial_card_pos[1] + mouse_pos[1] - initial_mouse_pos[1] # gets the new pos of moved_card_list
            reset_display(moved_card_list_pos[0], moved_card_list_pos[1], moved_card_list, windowSurface)
        if event.type == MOUSEBUTTONUP and clicked_before and cardpool_length > 0: # Finished dragging
            clicked_before = False
            mouse_pos = pygame.mouse.get_pos()
            moved_card_list_height = (len(moved_card_list) - 1) * CARDDISTANCE + CARDHEIGHT
            dest_cardpool_index = refer_mouse_pos_to_cardpools(mouse_pos[0]) # gets the cardpool_index which mouse_pos is currently at
            if len(cardpool_list[dest_cardpool_index].cards) > 0:
                head_card = moved_card_list[0]
                tail_card = cardpool_list[dest_cardpool_index].cards[-1] # records the first card of moved_card_list and the last card at that cardpool
            moved_card_list_rect = pygame.Rect(moved_card_list_pos, (CARDWIDTH, moved_card_list_height))
            pygame.draw.rect(windowSurface, BACKGROUNDCOLOR, moved_card_list_rect) # removes the initial moved_card_list surface
            # checks if moved_card_list can be moved to this cardpool
            if len(cardpool_list[dest_cardpool_index].cards) == 0 or (tail_card.suit == head_card.suit and tail_card.number == head_card.number + 1):
                # moved_card_list can be moved to this cardpool
                cardpool_list[dest_cardpool_index].cards.extend(moved_card_list) # adds all the card objects in moved_card_list
                number = find_consecutive_cards(cardpool_list[dest_cardpool_index])
                if (number == len(cardpool_list[dest_cardpool_index].cards) - 13): # We have a total hand from A to K
                    finish_hands(dest_cardpool_index)
                draw_cardpool(dest_cardpool_index)
                if len(cardpool_list[pool_num_moved].cards) > 0:
                    cardpool_list[pool_num_moved].cards[-1].show = True # displays the last card from the initial cardpool
                draw_cardpool(pool_num_moved)
            else:
                cardpool_list[pool_num_moved].cards.extend(moved_card_list)
                # adds all the card objects in moved_card_list back to the initial cardpool
                draw_cardpool(dest_cardpool_index)
                draw_cardpool(pool_num_moved)
    if (FINISHED_HANDS == TOTAL_HANDS):
        terminate()
    mainClock.tick(100000)
