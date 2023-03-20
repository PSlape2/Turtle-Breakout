import turtle
import time
import threading

import ball
import bouncer
import leaderboard
import squares

# initialize important turtles
screen = turtle.Screen()
score = turtle.Turtle()
life = turtle.Turtle()
timer = turtle.Turtle()
timen = turtle.Turtle()

def _init_():
    screen.tracer(False)
    ball.roundStart(screen.screensize())
    bouncer.movement.init()
    gameData._init()
    fromBouncer._init()
    squares.blockMethods.init(screen)
    ballCol = threading.Thread(target=squares.blockMethods.collisionCheck,args=(gameData,squares.turtles,squares.inactive))
    ballCol.start()
    events.gameStart()
    screen.ontimer(events.roundStart(), 100)
    screen.tracer(True)
    
class config():
    scoreLocation = (200,425) # location for the playerScore writing turtle (score)
    lifeLocation = (150, 400) # location for the lifeScore writing turtle (life)
    nameLocation = (-200, 400) # location for the playerName writing turtle (name) (turtle not global)
    startLife = 5
    leaderDirectory = "leaderboard.txt"

class gameData():
    def _init():
        '''
        This initialization method contains all of the initialization for most of the gameData, including
        the playerScore, playerName, and lifeScore.

        It sends each turtle responsible for writing out current scores to their respective locations*. Next,
        the method takes the input of the playerName, followed by writing the starting scores for playerScore,
        lifeScore*, and the previously entered playerName.

        *defined in the config class 
        '''
        global gameRun
        gameRun = True

        global playerScore
        global lifeScore
        playerScore = 0

        if(config.startLife < 0):
            raise Exception("Starting life cannot be less than 0")
        else:
            lifeScore = config.startLife

        name = turtle.Turtle()

        score.penup()
        score.hideturtle()
        score.goto(config.scoreLocation)
        score.pendown()

        life.penup()
        life.hideturtle()
        life.goto(config.lifeLocation)
        life.pendown()

        name.penup()
        name.ht()
        name.goto(config.nameLocation)
        name.pendown()

        global leaderNames
        global leaderScores

        ''''
        This section of code below is designed to open the leaderboard file. The first if statement checks if
        the leaderboard file exists at the directory. If the file is not there, the program then creates a new
        leaderboard file then attempts to reopen it. If the reopen fails, then it throws a FileNotFoundError
        exception. If the file is reopened, then it adds the placeholder scores to the file.

        Afterward, it retrieves the leaderNames and leaderScores from the leaderboard file.

        '''
        

        leaderNames = leaderboard.get_names(config.leaderDirectory)
        leaderScores = leaderboard.get_scores(config.leaderDirectory)
        
        # for video string manipulation
        global playerName
        playerName = screen.textinput("Turtle Breakout", "Enter your name")
        timer.hideturtle()
        try:
            playerChecker = playerName.strip()
            playerChecker = playerChecker.replace(" ", "")
        except:
            raise Exception("Name Error")
        else:
            if(playerChecker == ""):
                raise Exception("Please add a name")
        playerPrint = "Score:" + str(playerScore)
        lifePrint = "Life: " + str(lifeScore)
        namePrint = "Name: " + playerName
        score.write(playerPrint, False, align="center", font = ("Verdana", 20, "normal"))
        life.write(lifePrint, False, align="center", font = ("Verdana", 20, "normal"))
        name.write(namePrint, False, align="center", font = ("Verdana", 20, "normal"))
      
    def scoreUpdate():
        global playerScore
        playerScore += 1
        if(playerScore != (squares.turtleCount * squares.rowCount)):
            score.clear()
            playerPrint = "Score:" + str(playerScore)
            score.write(playerPrint, False, align="center", font=("Verdana", 20, "normal"))
        else:
            events.endgame()

    def lifeUpdate():
        '''
        Removes one from the lifeScore, then writes out the current lifeScore
        '''
    # TODO: Add code segment which checks if lifeScore <= 0.
        global lifeScore
        if(lifeScore >= 1):
            lifeScore -= 1
            life.clear()
            lifePrint = "Life: " + str(lifeScore)
            life.write(lifePrint, False, align="center", font=("Verdana", 20, "normal"))
        else:
            events.endgame()
      

        
class events():
    textFont = ("Verdana", 50, "normal")
    def gameStart():
        '''
        gameStart is called during the _init_() function. It shows the "Turtle Breakout" text at the end of the
        loading stage for 3 seconds.
        '''
        starter = turtle.Turtle()
        starter.write("Turtle Breakout", False, align="center", font=events.textFont)
        screen.update()
        time.sleep(3)
        starter.clear()
        screen.update()
    def roundStart():
        global gameRun
        if(ball.events.floorCollision()):
            gameData.lifeUpdate()
            gameRun = False
            screen.tracer(False)
            ball.roundStart(screen.screensize())
            bouncer.movement.init()
            screen.update()
            for n in range(3):
                timer.write((3-n), False, align="center", font=events.textFont)
                screen.update()
                time.sleep(1)
                timer.clear()
            gameRun = True
            screen.tracer(True)
            
        screen.ontimer(events.roundStart, 100)
    def nothing():
        m = 2
    def endgame():
        screen.onkeypress(events.nothing, bouncer.config.moveLeft_key)
        screen.onkeypress(events.nothing, bouncer.config.moveRight_key)
        end = turtle.Turtle()
        global gameRun
        global leaderNames
        global leaderScores
        global playerName
        global playerScore
        gameRun = False
      
        leaderboard.update_leaderboard(config.leaderDirectory, leaderNames, leaderScores, playerName, playerScore)
        leaderNames = leaderboard.get_names(config.leaderDirectory)
        leaderScores = leaderboard.get_scores(config.leaderDirectory)

        if(playerName in leaderNames):
            scorer = True
        else:
            scorer = False

        screen.clear()
        leaderboard.draw_leaderboard(scorer, leaderNames, leaderScores, end, playerScore)
        time.sleep(10)
        turtle.done()
    
            
class fromBouncer():
    def _init():
        '''
        _init() starts the onkeypress functions for the bouncer movement. It also begins the ball movement checks.
        '''
        try:
            screen.onkeypress(fromBouncer.moveLeft, bouncer.config.moveLeft_key)
            screen.onkeypress(fromBouncer.moveRight, bouncer.config.moveRight_key)
        except:
            print("Right Key: ", bouncer.config.moveRight_key)
            print("Left Key: ", bouncer.config.moveLeft_key)
            raise KeyError()
        screen.listen()

        screen.ontimer(fromBouncer.movementBall, 33)
    def moveLeft():
        '''
        Checks first if the bouncer turtle is within the x limits, if True, it moves the turtle backwards (left)
        by a number of units equal to the movementAmount variable within the config class of the bouncer file
        '''
        if (bouncer.bouncer.xcor() >= (-1*bouncer.config.xlims)) and gameRun:
            bouncer.bouncer.backward(bouncer.config.movementAmount)

    def moveRight():
        '''Does the same thing as moveLeft but to the right'''
        if (bouncer.bouncer.xcor() <= bouncer.config.xlims) and gameRun:
            bouncer.bouncer.forward(bouncer.config.movementAmount)
    def movementBall():
        '''
        This class allows the ball movement class to be called every 33 milliseconds without needing to call the
        movementBall class directly, nor needing to add the ontimer line there. Removes cross-imports.
        '''
        global gameRun
        if gameRun:
            ball.movement.moveOnVelocity()
        screen.ontimer(fromBouncer.movementBall, 33)




_init_()
screen.mainloop()