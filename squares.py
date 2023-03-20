import turtle
import time
import ball

prison = turtle.Turtle()
wn = turtle.Screen()

prisonImg = "prison.gif"
wn.addshape(prisonImg)
prison.shape(prisonImg)

turtle_green = "turtle_green.gif"
turtle_red = "turtle_red.gif"
turtle_yellow = "turtle_yellow.gif"

turtleCount = 9
rowCount = 3
turtles = [[]]
inactive = []
rowShapes = [turtle_green, turtle_yellow, turtle_red]


class blockMethods():

  def init(window):
    if rowCount > 5:
       raise ValueError("Greater than maximum allowed row count")
    for m in range(rowCount):
      w = []
      turtles.append(w)
      j = m
      window.addshape(rowShapes[m])
      for n in range(turtleCount):
        if j > 2:
           j = m - 2
        curTurtle = turtle.Turtle()
        curTurtle.penup()
        curTurtle.shape(rowShapes[j])
        curTurtle.goto((-400 + (100 * n)), (90 + (100 * m)))
        turtles[m].append(curTurtle)

  def collisionCheck(gameData, turtless, inact):
    while(True):
        for y in range(len(turtless)):
            for turt in turtless[y]:
                if (ball.baller.distance(turt.pos()) < 55) and not turt in inact:
                    turt.ht()
                    inactive.append(turt)
                    gameData.scoreUpdate()
                    ball.events.collideWithBlock()
        time.sleep(0.1) # for video function
