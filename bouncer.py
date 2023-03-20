import turtle
import ball

bouncer = turtle.Turtle()

class config():
    xlims = 500 # +- xlims equals the limits of the bouncer on each side
    xSize = 5
    ySize = 1
    startPos = (0,-100)
    movementAmount = 15 # amount in which the bouncer moves when the moveLeft or moveRight methods are called
    moveLeft_key = 'a'
    moveRight_key = 'd'
class movement():
    def init():
        bouncer.penup()
        bouncer.goto(0,-200)
        bouncer.shape('square')
        bouncer.shapesize(config.ySize, config.xSize, 1)
    

class eventChecker():
    def collisionCheck(balla):
        if (abs(balla.xcor() - bouncer.xcor()) < (8*config.xSize) and (abs(balla.ycor() - bouncer.ycor()) < (10 + config.ySize))):
            print("Collision True")
            return True
            
        else:
            return False