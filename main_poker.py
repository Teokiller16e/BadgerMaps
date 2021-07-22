import numpy as np
from random import randint


def filldeck(symbols):
    deck = np.empty(shape=[52,2])# Initialize the shape of the deck
    for j in range(deck.shape[0]): # basically create 13 different cards with 4 different shapes
        
        if(j<13):
            deck[j][0] = j+1
            deck[j][1] = symbols[0]
        elif (j>=13 and j<26):
            deck[j][0] = (j+1) - 13
            deck[j][1] = symbols[1]
        elif(j>=26 and j<39):
            deck[j][0] = (j+1) - 26
            deck[j][1] = symbols[2]
        else:
            deck[j][0] = (j+1) - 39
            deck[j][1] = symbols[3]
    number = len(deck)
    return deck 

def splitDeck (deck,numPlayers):
    firstCards = np.empty(shape=[numPlayers,2])
    secondCards = np.empty(shape=[numPlayers,2])
    for i in range(numPlayers):
        firstCard = randint(0, (len(deck)-1))
        while(deck[firstCard][0]==99):
            firstCard = randint(0, (len(deck)-1))
        firstCards[i] = deck[firstCard]
        deck[firstCard] = 99
        # Same thing for the second card :
        secondCard = randint(0, (len(deck)-1))
        while(deck[secondCard][0]==99):
            secondCard = randint(0, (len(deck)-1))
        secondCards[i] = deck[secondCard]
        deck[secondCard] = 99

    return firstCards,secondCards
    

if __name__ == "__main__":
    symbols =  [0,1,2,3] # ['clubs','diamonds','hearts','spades']
    deckOfCards = filldeck(symbols)
    numOfPlayers = int(input("Welcome to Badger Map's poker, please give the number of players \n")) # define the number of players 
    while numOfPlayers<2  and numOfPlayers>7:
        numOfPlayers = int(input(" The number you specified is not between the authorized limits, please give number of players between 2 and 7 \n"))
    splitDeck(deckOfCards,numOfPlayers)

   



