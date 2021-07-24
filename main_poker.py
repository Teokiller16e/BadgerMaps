import numpy as np
from random import randint

from numpy.lib.function_base import append


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


def hasRoyalFlush(firstCards,secondCards,playingCards,numOfPlayers):
    print("hello")

def hasStraightFlush(firstCards,secondCards,playingCards,numOfPlayers):
    print("hello")

def hasFullHouse(firstCards,secondCards,playingCards,numOfPlayers):
    print("hello")

# Straight
# has to be tested
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
            if (sortedArr[c,0] == (sortedArr[c+1,0] - 1) and c!=6):
                straightFound += 1 
            else: 
                straightFound = 0
        if(straightFound==4 or(sortedArr[0]==0 and sortedArr[3]==10 and sortedArr[4]==11 and sortedArr[5]==12 and sortedArr[6]==13)) : # the second condition reffers to the only option of having a 10,J,Q,K,A and the sorting cannot distinguish
                    winningHands.append(firstCards[i])
                    winningHands.append(secondCards[i])
                    break
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
                    winningHands.append(firstCards[i])
                    winningHands.append(secondCards[i])
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

# Four of A Kind
def hasFourOfAKind(firstCards,secondCards,playingCards,numOfPlayers):
    winningHands = []
    for i in range (numOfPlayers):
        mixArray = np.empty(shape=[7,2])
        for j in range(len(playingCards)):
            mixArray[j] = playingCards[j]

        mixArray[5] = firstCards[i] # insert first player's card
        mixArray[6] = secondCards[i] # insert second player's card
        sortedArr = mixArray[mixArray[:,0].argsort()]

        
        # Now try to find if there is an actual straight of 5 or more cards
        for c in range(len(sortedArr)):
            fourOfAKind = 0
            for k in range(len(sortedArr)-c): # because if until the 4th element we didn't found any four of a kind the we wont either way
                if(k<6):
                    if (sortedArr[c,0] == (sortedArr[k+c,0])):
                        fourOfAKind += 1
            if(fourOfAKind==4):
                winningHands.append(firstCards[i])
                winningHands.append(secondCards[i])
                break

                
    if(winningHands):
        return winningHands,True
    else:
        return winningHands,False

# Three of A Kind
def hasThreeOfAKind(firstCards,secondCards,playingCards,numOfPlayers):
    winningHands = []
    for i in range (numOfPlayers):
        mixArray = np.empty(shape=[7,2])
        for j in range(len(playingCards)):
            mixArray[j] = playingCards[j]

        mixArray[5] = firstCards[i] # insert first player's card
        mixArray[6] = secondCards[i] # insert second player's card
        sortedArr = mixArray[mixArray[:,0].argsort()]

        
        # Now try to find if there is an actual straight of 5 or more cards
        for c in range(len(sortedArr)):
            threeOfAKind = 0
            for k in range(len(sortedArr)-c): # because if until the 4th element we didn't found any four of a kind the we wont either way
                if(k<6):
                    if (sortedArr[c,0] == (sortedArr[k+c,0])):
                        threeOfAKind += 1
            if(threeOfAKind==3):
                winningHands.append(firstCards[i])
                winningHands.append(secondCards[i])
                break

                
    if(winningHands):
        return winningHands,True
    else:
        return winningHands,False

def hasTwoPair(firstCards,secondCards,playingCards,numOfPlayers):
    print("")

# To be tested
def hasPair(firstCards,secondCards,playingCards,numOfPlayers):
    winningHands = []
    for i in range (numOfPlayers):
        mixArray = np.empty(shape=[7,2])
        for j in range(len(playingCards)):
            mixArray[j] = playingCards[j]

        mixArray[5] = firstCards[i] # insert first player's card
        mixArray[6] = secondCards[i] # insert second player's card
        sortedArr = mixArray[mixArray[:,0].argsort()]

        
        # Now try to find if there is an actual straight of 5 or more cards
        for c in range(len(sortedArr)):
            threeOfAKind = 0
            for k in range(len(sortedArr)-c): # because if until the 4th element we didn't found any four of a kind the we wont either way
                if(k<6):
                    if (sortedArr[c,0] == (sortedArr[k+c,0])):
                        threeOfAKind += 1
            if(threeOfAKind==2):
                winningHands.append(firstCards[i])
                winningHands.append(secondCards[i])
                break

    if(winningHands):
        return winningHands,True
    else:
        return winningHands,False

# High Card 
def hasHighCard(firstCards,secondCards,numOfPlayers):
    winningHands = []
    higherCards = []
    for i in range (numOfPlayers):
        if(firstCards[i][0] >= secondCards[i][0] or firstCards[i][0] == 1):
            higherCards.append(firstCards[i][0])
        elif(firstCards[i][0] <= secondCards[i][0] or secondCards[i][0] == 1): 
            higherCards.append(secondCards[i][0])
    
    maximum = max(higherCards) 

    indices = [index for index, value in enumerate(higherCards) if value == maximum or value == 1]

    for i in range (len(indices)):
        winningHands.append(firstCards[indices[i]])
        winningHands.append(secondCards[indices[i]])

    return winningHands,True # because it's the least strong combination and therefore there will always be a max number 

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
        testingCards = np.ones(shape=[5,2])
        testingCards[3]= 0
        testingCards[4]= 0
        #hasFourOfAKind(firstCards,secondCards,testingCards,numOfPlayers)
        hasHighCard(firstCards,secondCards,numOfPlayers)
        answer = int(input("Give a positive number to play another round\n"))


   



