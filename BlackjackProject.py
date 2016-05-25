# BLACKJACK shell
from random import choice as rc
def total(hand):
    # how many aces in the hand
    aces = hand.count(11)
    # to complicate things a little the ace can be 11 or 1
    # this little while loop figures it out for you
    t = sum(hand)
    # you have gone over 21 but there is an ace
    if t > 21 and aces > 0:
        while aces > 0 and t > 21:
            # this will switch the ace from 11 to 1
            t -= 10
            aces -= 1
    return t

def hsupdate(money, highscore):  # updates the highscore
    if money > highscore:
        highscore = money
    with open("highscore.txt", "w") as file:
        file.write(str(highscore))
    return highscore

# a suit of cards in blackjack assume the following values
cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

# there are 4 suits per deck and usually several decks
# this way you can assume the cards list to be an unlimited pool
cwin = 0  # computer win counter
pwin = 0  # player win counter

with open("highscore.txt", "r") as file:
    highscore = int(file.readline())  # hs contains the highscore

with open("save.txt", "r") as file:
    money = int(file.readline())  # money contains the score

if money == 0:
    print("You are out of money.")
    print("We are going to give you a random amount of money between 100$ and 1000$.")
    wait = input("Press Enter.")
    money = rc(range(100, 1000, 10))

highscore = hsupdate(money, highscore)

bjp = False  # true if the player has a blackjack

print ("Let's play blackjack with the computer !")
print ("Your highscore is %d$." % highscore)

while True:
    bet = int(input("You have %d$. How much do you want to bet ? \n" % money)) 
    while bet > money:
        print("You can't bet %d$ because you only have %d$." % (bet,money))
        bet = int(input("You have %d$. How much do you want to bet ? \n" % money))
    
    player = []
    # draw 2 cards for the player to start
    player.append(rc(cards))
    player.append(rc(cards))
    # draw 2 cards for the computer to start
    comp = []
    comp.append(rc(cards))
    pbust = False  # player busted flag
    cbust = False  # computer busted flag
    while True:
        # loop for the player's play ...
        tp = total(player)
        tc = total(comp)
        print ("The player has these cards %s with a total value of %d" % (player, tp))
        print ("The computer has this card %s with a total value of %d" % (comp, tc))
        if tp > 21:
            print ("--> The player is busted!")
            pbust = True
            money -= bet
            with open("save.txt", "w") as file:
                file.write(str(money))
            break
        elif tp == 21:
            print ("BLACKJACK!!!")
            bjp = True
            money += int((1.5*bet))  # blackjack pays 3 for 2
            with open("save.txt", "w") as file:
                file.write(str(money))
            highscore = hsupdate(money, highscore)
            break
        else:
            hs = input("Hit or Stand/Done or hit & double & Stand (h or s or hds): ").lower()
            if hs == 'h':
                player.append(rc(cards))
            elif hs == 'hds': #ce n'est qu'une tentative
                bet=bet*2
                player.append(rc(cards))
                tp = total(player)
                print ("The player has these cards %s with a total value of %d" % (player, tp))
                break
            else:
                break
    while True:
        # loop for the computer's play ...
        comp.append(rc(cards))
        # dealer generally stands on 17
        while True:
            tc = total(comp)                
            if tc < 17:
                comp.append(rc(cards))
            else:
                break
        print ("the computer has %s for a total of %d" % (comp, tc))
        # now figure out who won ...
        if tc > 21:
            if bjp:
                break
            print ("--> The computer is busted!")
            cbust = True
            if pbust == False:
                print ("The player wins!")
                pwin += 1
                money += bet
                with open("save.txt", "w") as file:
                    file.write(str(money))
                highscore = hsupdate(money, highscore)
        elif tc > tp:
            print ("The computer wins!")
            cwin += 1
            money -= bet
            with open("save.txt", "w") as file:
                file.write(str(money))
        elif tc == tp:
            print ("It's a draw!")
        elif tp > tc:
            if bjp:
                break
            if pbust == False:
                print ("The player wins!")
                pwin += 1
                money += bet
                with open("save.txt", "w") as file:
                    file.write(str(money))
                highscore = hsupdate(money, highscore)
            elif cbust == False:
                print ("The computer wins!")
                cwin += 1
        break
    print ("Wins, player = %d  computer = %d" % (pwin, cwin))
    print ("You have %d$." % money)
    if money == 0:
        print ("You are out of money : GAME OVER.")
        print ("Your highscore is %d$." % highscore)
        break
    exit = input("Press Enter (q to quit): ").lower()
    if exit == 'q':
        break
    

print ("Thanks for playing blackjack with the computer!")
