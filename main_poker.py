from typing import Counter
import numpy as np
from random import randint
import collections
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


# HasRoyal Flush
def hasRoyalFlush(firstCards,secondCards,playingCards,numOfPlayers):
    winningHands = []
    for i in range (numOfPlayers):
        mixArray = np.empty(shape=[7,2])
        for j in range(len(playingCards)):
            mixArray[j] = playingCards[j]

        mixArray[5] = firstCards[i] # insert first player's card
        mixArray[6] = secondCards[i] # insert second player's card
        sortedArr = mixArray[mixArray[:,0].argsort()]

    # the condition reffers to the only option of having a 10,J,Q,K,A  and same color
        if(sortedArr[0,0]==1 and sortedArr[3,0]==10 and sortedArr[4,0]==11 and sortedArr[5,0]==12 and sortedArr[6,0]==13) :
            if(sortedArr[0,1]== sortedArr[3,1]== sortedArr[4,1]== sortedArr[5,1]== sortedArr[6,1]) :
                winningHands.append(firstCards[i])
                winningHands.append(secondCards[i])
        
    arr = np.array(winningHands)
    if(winningHands):
        return arr,True
    else:
        return arr,False   

# Straight Flush
def hasStraightFlush(firstCards,secondCards,playingCards,numOfPlayers):
    
    winningHandsFlush,flagFLS = hasFlush(firstCards,secondCards,playingCards,numOfPlayers)
    winningHandsStraight,flagSTR = hasStraight(firstCards,secondCards,playingCards,numOfPlayers)
    winningHandsFourOfAKind,flagFour = hasFourOfAKind(firstCards,secondCards,playingCards,numOfPlayers)
    test = []

    
    if(flagFLS and flagSTR):
        if(winningHandsFlush == winningHandsStraight):
            return "STRAIGHTFLUSH",winningHandsStraight
    elif(flagFour): 
        return "FOUROFAKIND",winningHandsFourOfAKind
    elif(flagFLS and flagSTR==False):
        return "FLUSH",winningHandsFlush
    elif(flagFLS==False and flagSTR):
        return "STRAIGHT",winningHandsStraight
    else: return "none",test

# Not yet implemented
def hasFullHouse(firstCards,secondCards,playingCards,numOfPlayers):
    print("hello")
    # basically we have to call the three of a kind and the has two pair function and if we find 3 cards and 2 different from the 2/3 then we have a full house

# Straight
def hasStraight(firstCards,secondCards,playingCards,numOfPlayers):

    winningHands = []
    for i in range (numOfPlayers):
        mixArray = np.empty(shape=[7,2])
        for j in range(len(playingCards)):
            mixArray[j] = playingCards[j]

        mixArray[5] = firstCards[i] # insert first player's card (of course we can j +1 but since we know it's final there is no use)
        mixArray[6] = secondCards[i] # insert second player's card
        sortedArr = mixArray[mixArray[:,0].argsort()]
        straightFound = 0

        # Now try to find if there is an actual straight of 5 or more cards
        for c in range(len(sortedArr)-1):    
            if (sortedArr[c,0] == (sortedArr[c+1,0] - 1) ):
                straightFound += 1 
            elif(sortedArr[c,0] == (sortedArr[c+1,0])): # because it might be that we have duplicate cards to the sorted array
                continue
            elif(straightFound<4): 
                straightFound = 0

        # the second condition reffers to the only option of having a 10,J,Q,K,A and the sorting cannot distinguish
        if(straightFound==4 or(sortedArr[0,0]==1 and sortedArr[3,0]==10 and sortedArr[4,0]==11 and sortedArr[5,0]==12 and sortedArr[6,0]==13)) : 
                    winningHands.append(firstCards[i])
                    winningHands.append(secondCards[i])
                    

    arr = np.array(winningHands)
    if(winningHands):
        return arr,True
    else:
        return arr,False

# Flush
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
                if(clubs>4 or diamonds > 4 or hearts >4  or spades > 4) : # flash found
                    winningHands.append(firstCards[i])
                    winningHands.append(secondCards[i])
                elif(sortedArr[c,1] == 0):
                    clubs += 1
                elif(sortedArr[c,1] == 1):
                    diamonds += 1
                elif(sortedArr[c,1] == 2):
                    hearts += 1
                else:
                    spades += 1
                    
    arr = np.array(winningHands)
    if(winningHands):
        return arr,True
    else:
        return arr,False

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
                #break

                
    arr = np.array(winningHands)
    if(winningHands):
        return arr,True
    else:
        return arr,False

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
                #break in this case contrary to four of a kind there can be 2 x three of a kind

                
    arr = np.array(winningHands)
    if(winningHands):
        return "ThreeOfAKind",arr
    else:
        return "False",arr

def hasTwoPair(firstCards,secondCards,playingCards,numOfPlayers):
    winningHands,flag = hasPair(firstCards,secondCards,playingCards,numOfPlayers) 
    twoPairs = []

    arr = np.array(winningHands)

    if(flag):
        for i in range(len(arr)):
            count = 0
            for j in range(len(arr)-i):
                if ((arr[i,0] == arr[j+i,0]) and arr[i,1] == arr[j+i,1]):
                    count += 1
            if(count>=2):
                twoPairs.append(arr[i])
        
    twoPairs = list(dict.fromkeys(twoPairs))

    if(twoPairs):
        return "TwoPairs",twoPairs
    elif(len(winningHands)>=2):
        return "OnePair",winningHands
    else: return "False",[]

# HasPair
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
            pair = 0
            for k in range(len(sortedArr)-c): # because if until the 4th element we didn't found any four of a kind the we wont either way
                if(k<6):
                    if (sortedArr[c,0] == (sortedArr[k+c,0])):
                        pair += 1
            if(pair==2):
                winningHands.append(firstCards[i])
                winningHands.append(secondCards[i])
                
    arr = np.array(winningHands)
    if(winningHands):
        return arr,True
    else:
        return arr,False

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

    arr = np.array(winningHands)
    
    return arr # because it's the least strong combination and therefore there will always be a max number 

# Print players initial hands 
def printInitialHands(firstCards,secondCards):
    initialCards = []
    for i in range (len(firstCards)):
            initialCards.append(firstCards[i])
            initialCards.append(secondCards[i])

    arr = np.array(initialCards)
    print("Initial hand cards, 2 for each player : \n")
    printWinner(arr)

# Print winner with symbol strings
def printWinner(resultCards):
    for i in range(len(resultCards)):
        if(resultCards[i,1] == 0):
            print(resultCards[i,0],"  clubs ",)
        elif (resultCards[i,1] == 1):
            print(resultCards[i,0],"  diamonds ",)
        elif (resultCards[i,1]==2):
            print(resultCards[i,0],"  hearts ",)
        else : print(resultCards[i,0],"  spades ",)
    print(" \n")

# Outcome possible conditions:
def outcomes(res,strAnswer):
    if(len(res)==2):
        print(strAnswer)
        print("Cards on the table : \n")
        printWinner(playingCards)
        print("Winning hand : \n")
        printWinner(res)
    elif(len(result)== 2*numOfPlayers):
        highCardSplit = hasHighCard(firstCards,secondCards,numOfPlayers)

if __name__ == "__main__":

    symbols =  [0,1,2,3] # ['clubs','diamonds','hearts','spades']
    numOfPlayers = int(input("Welcome to Badger Map's poker, please give the number of players \n")) # define the number of players 
    while numOfPlayers<2  or numOfPlayers>7:
        numOfPlayers = int(input(" The number you specified is not between the authorized limits, please give number of players between 2 and 7 \n"))

    answer = int(input("Give a positive number to start the game\n")) # Starting round:

    while answer>0:
        deckOfCards = filldeck(symbols)
        firstCards,secondCards = splitDeck(deckOfCards,numOfPlayers) # retrieve players cards
        playingCards = burnCards(deckOfCards) # retrieve shown up cards
        printInitialHands(firstCards,secondCards)
        # We have to check from the higher to the lower hand payoff so we can exclude as much as we can:
        result,RF = hasRoyalFlush(firstCards,secondCards,playingCards,numOfPlayers)


        # In this step we will check if have Royal Flush and in the Straight Flush all the between hierarchical winner hand will be checked one by one 
        if(RF):
            outcomes(res,"ROYALFLUSH") # Case that royal flush is already on the table
        else:
            strOrFl,res = hasStraightFlush(firstCards,secondCards,playingCards,numOfPlayers)

            if (strOrFl=="STRAIGHTFLUSH"):
                outcomes(res,strOrFl) # Case that straight flush is already on the table 
            elif (strOrFl=="FOUROFAKIND"):
                outcomes(res,strOrFl)# Case that four of a kind is already on the table
            elif (strOrFl=="FLUSH"):
                outcomes(res,strOrFl)# Case that flush is already on the table
            elif (strOrFl=="STRAIGHT"):
                outcomes(res,strOrFl) # Case that straight is already on the table
            else:
                strOfThree,res = hasThreeOfAKind(firstCards,secondCards,playingCards,numOfPlayers)
                if (strOfThree=="ThreeOfAKind"):
                    outcomes(res,strOfThree) # Case that straight is already on the table
                else:
                    strOfPairs,res = hasTwoPair(firstCards,secondCards,playingCards,numOfPlayers)
                    if(strOfPairs == "TwoPairs"):
                        outcomes(res,strOfPairs)
                    elif(strOfPairs=="OnePair"):
                        outcomes(res,strOfPairs)
                    else:
                        highCardSplit = hasHighCard(firstCards,secondCards,numOfPlayers)
                        printWinner(highCardSplit)
        answer = int(input("Give a positive number to play another round\n"))
    print("Today's match is over !!")

   



