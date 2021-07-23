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

    # return numpy array with cards and their symbols         
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

    # return numpy array's with players first and second cards        
    return firstCards,secondCards
    

def burnCards(deck):
    playingCards = np.empty(shape=[5,2])
    for i in range(3):
        discard(playingCards,deck,i)
    return playingCards

def discard(playingCards,deck,flag):

    if flag==0:
        num = 3
    else: 
        num = 1

    for j in range(num):
        indx = randint(0, (len(deck)-1))
        while(deck[indx][0]==99):
            indx = randint(0, (len(deck)-1))
        if(flag==0):
            playingCards[j] = deck[indx]
            deck[indx] = 99
        elif(flag ==1) :
            playingCards[3] = deck[indx]
            deck[indx] = 99
        else:
            playingCards[4] = deck[indx]
            deck[indx] = 99

    indx = randint(0, (len(deck)-1))
    while(deck[indx][0]==99):
        indx = randint(0, (len(deck)-1))
    deck[indx] = 99

# Straight
def hasStraight(firstCards,secondCards,playingCards,numOfPlayers):

    winningHands = []
    for i in range (numOfPlayers):
        mixArray = np.empty(shape=[7,2])
        for j in range(len(playingCards)):
            mixArray[j] = playingCards[j]

        mixArray[5] = firstCards[i] # insert first player's card
        mixArray[6] = secondCards[i] # insert second player's card
        sortedArr = mixArray[mixArray[:,0].argsort()]
        straightFound = 0

        # Now try to find if there is an actual straight of 5 or more cards
        for c in range(len(sortedArr)):
                if(straightFound==4 or (c==6 and straightFound==3 and sortedArr[0,0]==1)) : # the second condition reffers to the only option of having a 10,J,Q,K,A and the sorting cannot distinguish
                    winningHands.append(firstCards[i],secondCards[i])
                if (sortedArr[c,0] == (sortedArr[c+1,0] - 1) and c!=6):
                    straightFound += 1 
                else: 
                    straightFound = 0
    if(winningHands):
        return winningHands,True
    else:
        return winningHands,False

# Flash
def hasFlush(firstCards,secondCards,playingCards,numOfPlayers):
    winningHands = []
    for i in range (numOfPlayers):
        mixArray = np.empty(shape=[7,2])
        for j in range(len(playingCards)):
            mixArray[j] = playingCards[j]

        mixArray[5] = firstCards[i] # insert first player's card
        mixArray[6] = secondCards[i] # insert second player's card
        sortedArr = mixArray[mixArray[:,0].argsort()]

        clubs = 0
        diamonds = 0
        hearts = 0
        spades = 0

        # Now try to find if there is an actual cards of 5 or more same shapes
        for c in range(len(sortedArr)):
                if(clubs==4 or diamonds == 4 or hearts == 4 or spades == 4) : # flash found
                    winningHands.append(firstCards[i],secondCards[i])
                if(sortedArr[c,1] == 0):
                    clubs += 1
                if(sortedArr[c,1] == 1):
                    diamonds += 1
                if(sortedArr[c,1] == 2):
                    hearts += 1
                if(sortedArr[c,1] == 3):
                    spades += 1
                    
    if(winningHands):
        return winningHands,True
    else:
        return winningHands,False

def hasThreeOfAKind(firstCards,secondCards,playingCards,numOfPlayers):
    print("")

def hasPair(firstCards,secondCards,playingCards,numOfPlayers):
    print("")

def hasHighCard(firstCards,secondCards,playingCards,numOfPlayers):
    print("")

def hasFourOfAKind(firstCards,secondCards,playingCards,numOfPlayers):
    print("")

if __name__ == "__main__":
    symbols =  [0,1,2,3] # ['clubs','diamonds','hearts','spades']
    numOfPlayers = int(input("Welcome to Badger Map's poker, please give the number of players \n")) # define the number of players 
    while numOfPlayers<2  and numOfPlayers>7:
        numOfPlayers = int(input(" The number you specified is not between the authorized limits, please give number of players between 2 and 7 \n"))

    answer = int(input("Give a positive number to start the game\n")) # Starting round
    while answer>0:
        deckOfCards = filldeck(symbols)
        firstCards,secondCards = splitDeck(deckOfCards,numOfPlayers) # retrieve players cards
        playingCards = burnCards(deckOfCards) # retrieve shown up cards
        hasStraight(firstCards,secondCards,playingCards,numOfPlayers)

        answer = int(input("Give a positive number to play another round\n"))


   



