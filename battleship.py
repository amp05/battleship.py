#Aldo Polanco and Madeline Goldberg
#CS111 Final Project
#Gregory the Battleship Machine

#-*- coding: utf-8 -*-
from graphics import *
import copy, random, math
from multiprocessing import Process

win = GraphWin("Battleship", 480, 480)
win.setBackground("sky blue") #main menu
win.setCoords(0.0, 0.0, 10.0, 10.0)
discoMode = False

board = [["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""], #board lay out
         ["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""],
         ["", "", "", "", "", "", "", "", "", ""]]

CPUShips = copy.deepcopy(board)
empty = copy.deepcopy(board)
numShips = 4 #number of ships of increasing length

def draw_board(win, board):
    # draw the grid lines
    batTitle.undraw()
    gregTitle.undraw()
    playButton.undraw()
    playText.undraw()
    for i in range(len(board)):
        Line(Point(i, 0), Point(i, 10)).draw(win)
        Line(Point(0, i), Point(10, i)).draw(win)

    for row in range(len(board)):
        for column in range(len(board)):
            cell = Text(Point(column + 0.5, row + 0.5), board[row][column])
            cell.setSize(36)
            cell.setStyle("bold")
            cell.setFace("courier")
            cell.draw(win)



gregTitle = Text(Point(4,8), "Gregory's") #Title menu, including play button
gregTitle.setSize(29)
gregTitle.setFace("courier")
batTitle = Text(Point(5.5,7), "Battleship")
batTitle.setSize(29)
batTitle.setStyle("bold")
batTitle.setFace("courier")
batTitle.draw(win)
gregTitle.draw(win)
playButton = Rectangle(Point(4,4), Point(6,5))
playButton.setWidth(3)
playButton.setFill("white")
playButton.draw(win)
playText = Text(Point(5,4.5), "Play")
playText.setFace("courier")
playText.setSize(26)
playText.draw(win)

insButton = Rectangle(Point(2,2), Point(8,3))
insButton.setWidth(3) #instructions button
insButton.setFill("white")
insButton.draw(win)
insText = Text(Point(5,2.5), "Instructions")
insText.setFace("courier")
insText.setSize(26)
insText.draw(win)
pressPlay = win.getMouse()
while pressPlay.getX() > 6 or pressPlay.getX() < 4 or \
      pressPlay.getY() < 4 or pressPlay.getY() > 5: #instructions button click
      if pressPlay.getX() < 8 and pressPlay.getX() > 2 and \
         pressPlay.getY() < 3 and pressPlay.getX() > 2:
        inst = GraphWin("Instructions", 480, 480)
        inst.setBackground("sky blue")
        inst.setCoords(0.0, 0.0, 10.0, 10.0)
        instTitle = Text(Point(5,9), "Placing Phase")
        instTitle.setSize(26)
        instTitle.setFace("courier")
        instTitle.setStyle("bold")
        instTitle.draw(inst)
        instImage = Image(Point(5,3),"instructions.png")
        instImage.draw(inst)
        instText = Text(Point(5, 7), "You have four ships: one ship that is 2 squares long, \n one ship that is 3 squares long,\n one ship that is 4 squares long, \n and one ship that is 5 squares long. \n You must place your ships in ascending order by size. \n  To place, click the squares \n that mark the start and end points of your ships. \n Please note that you cannot place your ships diagonally, \n and nor can you place your ships on top of one another.")
        instText.setSize(10)
        instText.setFace("courier")
        instText.draw(inst)
        clickAnywhere = Text(Point(5, 1),"Click anywhere to continue")
        clickAnywhere.setSize(10)
        clickAnywhere.setFace("courier")
        clickAnywhere.draw(inst)
        instClick = inst.getMouse()
        if instClick.getX() > 3 and instClick.getX() < 3.64 and \
           instClick.getY() > 3.798 and instClick.getY() < 4.41: #EASTER EGG :)
           discoModeText = Text(Point(5,5.5), "Gregory Mode Activated")
           discoModeText.setFace("courier")
           discoModeText.setStyle("bold")
           discoModeText.setSize(26)
           discoMode = True
           discoModeText.draw(inst)
           time.sleep(0.75)
           discoModeText.undraw()
           inst.getMouse()

        instText.undraw()
        instTitle.undraw()
        instImage.undraw()
        instImage = Image(Point(5,3),"instructions1.png") #instruction text and image
        instTitle = Text(Point(5,9), "Attacking Phase")
        instText = Text(Point(5, 6.6), "Once you've placed your ships a second grid will appear, \n this labeled Attack Panel. This is your view of your \n opponent's board. You cannot see where their ships are placed,\n but you can drop a bomb anywhere on their side by simply clicking \n a square. If your attack does not hit any of your opponent's ships, \n the word MISS will flash across the screen and the empty square \n you hit will turn red. If you hit, the word HIT will flash \n and the empty square you hit will turn blue. The word SUNK \n will flash when any ship is successfully sunk in its entirety. \n When all of one player's ships are sunk the game \n is over, and that player loses. \n Please note that you cannot strike the same square twice \n")
        instTitle.setSize(26)
        instTitle.setFace("courier")
        instTitle.setStyle("bold")
        instText.setSize(9)
        instText.setFace("courier")
        instText.draw(inst)
        instTitle.draw(inst)
        instImage.draw(inst)
        inst.getMouse()
        inst.close()

      pressPlay = win.getMouse()
win.close() #Closes window to start placement phase
userBoard = GraphWin("Your Ships", 480, 480) #Opens board where placement will begin
userBoard.setBackground("sky blue")
userBoard.setCoords(0.0, 0.0, 10.0, 10.0)
draw_board(userBoard, board)

#Placement phase

def validateMove(spot1, spot2, ship): #Validates a move, returns true if valid, false + invalid text if invalid
    if (abs(int(spot1.getX()) - int(spot2.getX())) == ship and \
        int(spot1.getY()) == int(spot2.getY())) or \
        (abs(int(spot1.getY()) - int(spot2.getY())) == ship and \
            int(spot1.getX()) == int(spot2.getX())):
        return True
    else:
        invalidMove(userBoard)
        return False

def invalidMove(board): #Flashes invalid move text
    selectionSquare.undraw()
    tryAgain = Text(Point(5,5.5), "Invalid Move")
    tryAgain.setFace("courier")
    tryAgain.setStyle("bold")
    tryAgain.setFill("black")
    tryAgain.setSize(26)
    tryAgain.draw(board)
    time.sleep(0.75)
    tryAgain.undraw()

shipsPlaced = 0 #Counts ships placed and helps with ship length
placeText = Text(Point(5,5.5),("Place your " + str(shipsPlaced+2) + " ship")) #Text  telling which ship to place
placeText.setSize(26)
placeText.setStyle("bold")
placeText.setFace("courier")
while shipsPlaced < numShips and userBoard.isOpen(): #Placing phase loop
    placeText = Text(Point(5,5.5),("Place your " + str(shipsPlaced+2) + " ship"))
    placeText.setSize(26)
    placeText.setStyle("bold")
    placeText.setFace("courier")
    time.sleep(0.10)
    placeText.draw(userBoard)
    time.sleep(0.75)
    placeText.undraw()
    spot1 = userBoard.getMouse()
    x1 = int(spot1.getX())
    y1 = int(spot1.getY())
    if board[y1][x1] != "":
        invalidMove(userBoard)
        continue
    selectionSquare = Rectangle(Point(x1, y1), Point(x1+1,y1+1))
    selectionSquare.setFill("white")
    selectionSquare.draw(userBoard) #shows selection
    spot2 = userBoard.getMouse()
    x2 = int(spot2.getX())
    y2 = int(spot2.getY())
    if board[y2][x2] != "":
        invalidMove(userBoard)
        continue
    if validateMove(spot1, spot2, shipsPlaced + 1):
        selectionSquare.undraw()
        invalid = 0
        if x2 == x1: #Checks validity and ticks ships placed if valid
            for dy in range(abs(y2-y1)):
                if board[min(y1, y2) + dy][x1] != "":
                    invalidMove(userBoard)
                    invalid = 1
            if invalid == 1:
                continue
            for dy in range(abs(y2-y1)):
                board[y2][x2] = str(shipsPlaced+2)
                board[y1][x1] = str(shipsPlaced+2)
                board[min(y1, y2) + dy][x1] = str(shipsPlaced+2)
            shipsPlaced += 1
        elif y2 == y1:
            for dx in range(abs(x2-x1)):
                if board[y1][min(x1,x2) + dx] != "":
                    invalidMove(userBoard)
                    invalid = 1
            if invalid == 1:
                continue
            for dx in range(abs(x2-x1)):
                board[y2][x2] = str(shipsPlaced+2)
                board[y1][x1] = str(shipsPlaced+2)
                board[y1][min(x1, x2) + dx] = str(shipsPlaced+2)
            shipsPlaced += 1
        else:
            invalidMove(userBoard)
        draw_board(userBoard, board)
    else:
        continue

CPUBoard = GraphWin("Attack Panel", 480, 480) #Opens board to keep track of attacks to AI board
CPUBoard.setBackground("sky blue")
CPUBoard.setCoords(0.0, 0.0, 10.0, 10.0)
draw_board(CPUBoard, CPUShips)

#CPU Placement

def validList(shiplength): #Function for every single place CPU can place
    validPlaces = []
    for y in range(len(CPUShips)):
        for x in range(len(CPUShips[y])):
            countv = 0
            counth = 0
            for l in range(shiplength): #vertical loop
                if len(CPUShips) <= y+l:
                    break
                elif CPUShips[y+l][x] == "":
                    countv += 1
            if countv == shiplength:
                validPlaces.append((y,x, "v")) #append a valid coordinate considering ship length, v for vertical
            for l in range(shiplength):
                if len(CPUShips[y]) <= x+l:
                    break
                elif CPUShips[y][x+l] == "":
                    counth += 1
            if counth == shiplength:
                validPlaces.append((y,x, "h"))
    return validPlaces

shipList = [2, 3, 4, 5] #length of
for shiplength in shipList:
    spot = random.choice(validList(shiplength)) #spot[0] is y coord, spot[1] is x, spot[2] is vert or horiz
    for l in range(shiplength):
        if spot[2] == "v":
            CPUShips[spot[0]+l][spot[1]] = str(shiplength)
        elif spot[2] == "h":
            CPUShips[spot[0]][spot[1]+l] = str(shiplength)
draw_board(CPUBoard, empty) #draws board but without ships

#Playing phase

missText = Text(Point(5,5.5), "MISS") #descripts miss hit and sunk texts to be spawned
missText.setFill("black")
missText.setSize(26)
missText.setFace("courier")
missText.setStyle("bold")
hitText = Text(Point(5,5.5), "HIT")
hitText.setFill("black")
hitText.setSize(26)
hitText.setFace("courier")
hitText.setStyle("bold")
sunkText = Text(Point(5,5.5), "SUNK")
sunkText.setFill("black")
sunkText.setSize(26)
sunkText.setFace("courier")
sunkText.setStyle("bold")

userShipCount = {"2":2, #keeps track of what ships are still alive
                "3":3,
                "4":4,
                "5":5}
cpuShipCount = {"2":2,
                "3":3,
                "4":4,
                "5":5}

def sunk(atty, attx, player): #checks if ship is destroyed
    if player == "User":
        cpuShipCount[CPUShips[atty][attx]] -= 1
        if cpuShipCount[CPUShips[atty][attx]] == 0:
            return True
        else:
            return False
    if player == "CPU":
        userShipCount[board[atty][attx]] -= 1
        if userShipCount[board[atty][attx]] == 0:
            return True
        else:
            return False

def getWinner(): #checks for a winner every turn
    if sum(userShipCount.values()) <= 0:
        return "CPU"
    elif sum(cpuShipCount.values()) <= 0:
        return "User"
    else:
        return ""

colorR = 0
colorG = 0
colorB = 0
cpuChoices = []
cpuHit = []
userHit = []
winner = ""
direc = ""
turn = "User" #starts user turn
while winner == "" and userBoard.isOpen() and CPUBoard.isOpen(): #main play loop
    if discoMode == True: #greg mode :)
        colorR = random.randint(0,255)
        colorG = random.randint(0,255)
        colorB = random.randint(0,255)
        userBoard.setBackground(color_rgb(colorR, colorG, colorB))
        CPUBoard.setBackground(color_rgb(colorR, colorG, colorB))
    if turn == "User":
        attack = CPUBoard.getMouse()
        attx = int(attack.getX())
        atty = int(attack.getY())
        if (attx, atty) in userHit:
            continue
        userHit.append((attx, atty))
        if CPUShips[atty][attx] != "":
            if sunk(atty, attx, turn):
                sunkText.draw(CPUBoard)
                time.sleep(0.5)
                sunkText.undraw()
            else:
                hitText.draw(CPUBoard)
                time.sleep(0.50)
                hitText.undraw()
            hitSquare = Rectangle(Point(attx, atty), Point(attx+1,atty+1))
            hitSquare.setFill("dark slate blue")
            hitSquare.draw(CPUBoard)
            draw_board(CPUBoard, empty)
            winner = getWinner()
            continue
        else:
            missText.draw(CPUBoard)
            time.sleep(0.50)
            missText.undraw()
            missSquare = Rectangle(Point(attx, atty), Point(attx+1,atty+1))
            missSquare.setFill("firebrick")
            missSquare.draw(CPUBoard)
            draw_board(CPUBoard, empty)
            turn = "CPU"
    elif turn == "CPU":
        if len(cpuChoices) == 0: #CPU's logic to choose where to attack
            attx = random.randint(0,9)
            atty = random.randint(0,9)
            direc = ""
        else:
            if direc == "" or direc == cpuChoices[0][2]:
                if len(cpuChoices) == 0:
                    continue
                attx = cpuChoices[0][0]
                atty = cpuChoices[0][1]
                direc = cpuChoices[0][2]
                del cpuChoices[0]
            elif cpuChoices[0][2] != direc and direc != "":
                while cpuChoices[0][2] != direc:
                    if len(cpuChoices) > 1:
                        del cpuChoices[0]
                    else:
                        break
                attx = cpuChoices[0][0]
                atty = cpuChoices[0][1]
                direc = cpuChoices[0][2]
        if (attx, atty) in cpuHit:
            continue
        cpuHit.append((attx, atty))
        if board[atty][attx] != "":
            if sunk(atty, attx, turn):
                sunkText.draw(userBoard)
                time.sleep(0.5)
                sunkText.undraw()
                cpuChoices = []
            else:
                hitText.draw(userBoard)
                if attx+1 < len(CPUShips[atty]) and (attx+1, atty) not in cpuHit:
                    cpuChoices.append((attx+1,atty, "h"))
                if atty+1 < len(CPUShips) and (attx, atty+1) not in cpuHit:
                    cpuChoices.append((attx,atty+1, "v"))
                if attx-1 >= 0 and (attx-1, atty) not in cpuHit:
                    cpuChoices.append((attx-1,atty, "h"))
                if atty-1 >= 0 and (attx, atty-1) not in cpuHit:
                    cpuChoices.append((attx,atty-1, "v"))
                time.sleep(0.50)
                hitText.undraw()
            hitSquare = Rectangle(Point(attx, atty), Point(attx+1,atty+1))
            hitSquare.setFill("firebrick")
            hitSquare.draw(userBoard)
            draw_board(userBoard, board)
            winner = getWinner()
            continue
        else:
            missText.draw(userBoard)
            time.sleep(0.50)
            missText.undraw()
            direc = ""
            missSquare = Rectangle(Point(attx, atty), Point(attx+1,atty+1))
            missSquare.setFill("dark slate blue")
            missSquare.draw(userBoard)
            draw_board(userBoard, board)
            turn = "User"

draw_board(CPUBoard, CPUShips) #reveals where cpu ships where after games over
if winner == "User":
    winnerText = Text(Point(5,5.5),("YOU WIN!"))
    winnerText2 = Text(Point(5,5.5),("YOU WIN!"))
elif winner == "CPU":
    winnerText = Text(Point(5,5.5),("You lose :("))
    winnerText2 = Text(Point(5,5.5),("You lose :("))
winnerText2.setFace("courier")
winnerText2.setStyle("bold")
winnerText.setFace("courier")
winnerText.setStyle("bold")
winnerText.setSize(30)
winnerText2.setSize(30)
winnerText.draw(userBoard) #shows winner text
winnerText2.draw(CPUBoard)


while CPUBoard.isOpen() and discoMode == True: #Easter egg surprise
    freq = 0.3
    for i in range(32):
        colorR = int(math.sin(freq*i) * 127 + 128)
        colorG = int(math.sin(freq*i + 2) * 127 + 128)
        colorB = int(math.sin(freq*i + 4) * 127 + 128)
        userBoard.setBackground(color_rgb(colorR, colorG, colorB))
        CPUBoard.setBackground(color_rgb(colorR, colorG, colorB))
CPUBoard.getMouse()
