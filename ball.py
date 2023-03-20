import turtle
import math
import time
import random

import bouncer

baller = turtle.Turtle()

class configData():
	ballerStart = (0,0) # ball start coordinates
	shape = "circle" # shape of the ball, for science purposes.
	xSize, ySize, outLineSize = (1,1,1) # This tuple is changed into 3 variables for the size of the ball.
	bounceCoefficient = 1 #  the amount in which the speed changes (multiply) when the ball bounces
	# do not make bounceCoefficient negative (please I beg you)


def roundStart(screensize):
	movement.init_()
	events.init_(screensize)

	baller.penup()
	baller.ht()
	baller.goto(configData.ballerStart)
	baller.shape(configData.shape)
	baller.shapesize(configData.xSize, configData.ySize, configData.outLineSize)
	baller.showturtle()

	Vector1.roundStartVector()

class Vector1():
	heading = 0
	speed = 0

	'''
	This is an improvised Vector system.

	This class contains the heading, speed, and direction information.
	
	Heading and speed contain calculation methods, but are not used.

	Ball movement is managed by the moveOnVelocity() method within the movement class.

	Vector1 also includes the updateVector and roundStartVector methods.

	updateVector() - This method takes the xVelocity and yVelocity global variables and calulates the heading.
	If the heading would cause a 0 or undefined result from the math.atan() function, then it uses predetermined
	values for the heading.



	roundStartVector() - This method sets the starting values to xVelocity and yVelocity. By default these

	'''
	def updateHeading():
		if xVelocity != 0:
			Vector1.heading = math.degrees(math.atan(yVelocity / xVelocity))
		if yVelocity < 0 and xVelocity < 0 or yVelocity > 0 and xVelocity < 0:
			Vector1.heading -= 180
		elif yVelocity < 0: 
			Vector1.heading = 270
		else: 
			Vector1.heading = 90
	def updateSpeed():
		if(Vector1.speed < 0):
			raise ValueError("Speed less than 0")
		else:
			Vector1.speed = math.isqrt(math.pow(xVelocity, 2) + math.pow(yVelocity, 2))

	def roundStartVector():
		global xVelocity
		global yVelocity
		xVelocity = random.randint(15,30)
		yVelocity = random.randint(20,30)


class movement:
	'''
	This class manages the movement of the ball.

	It contains the init_(), updatePositions(), and moveOnVelocity() methods.

	init_() - This method initializes the values for xVelocity, yVelocity, xPosition, and yPosition.
	xVelocity and yVelocity are set to 0, while xPosition and yPosition are set to values based on 
	the ballerStart tuple contained within the configData class.

	updatePositions() - This method only changes the global variables xPosition and yPosition to the current
	position of the ball.

	moveOnVelocity() - This method calls movement.updatePositions() and events.collisionCheckAll() before
	setting the variables xTarget and yTarget. These variables are calculated by adding their corresponding 
	positions* and velocities*.

	*corresponding positons and velocities refers to their x and y variants.
	'''
	def init_():
		global xVelocity
		global yVelocity
		global xPosition
		global yPosition
		xVelocity = 0
		yVelocity = 0
		xPosition, yPosition = configData.ballerStart

	def updatePositions():
		global xPosition
		global yPosition
		xPosition = baller.xcor()
		yPosition = baller.ycor()

	def moveOnVelocity():
		movement.updatePositions()
		events.collisionCheckAll()
		xTarget = xPosition + xVelocity
		yTarget = yPosition + yVelocity
		baller.goto(xTarget, yTarget)


class events():
	'''
	This class contains the collision events for the Ball.

	collisionCheckAll() - This method only consolidates the other collision checkers.

	init_(screensize) - This initialization method calls the screen size to ensure that the ball is bouncing off of the edge
	of the screen.

	wallCollision() - This checks if the ball is colliding with the boundaries of the screen, causing the ball to
	reverse xVelocity on collision.

	reflectOnBouncer() - This method calls bouncer.eventChecker.collisionCheck() with the turtle ball as a parameter.
	If the method returns True, then the yVelocity is reversed.

	floorCollision() - This method is called to check if the ball collides with the bottom of the screen. 
	It returns True if the condition is met, and returns False when not met.

	reflectOnRoof() - This method checks if the ball is colliding with the roof and the yVelocity is greater than 0.
	If this condition is True, then the yVelocity of the ball is reversed.

	''' # for video events
	def collisionCheckAll():
		events.wallCollision()
		events.reflectOnBouncer()
		events.reflectOnRoof()

	def init_(screensize):
		global ScreenLength
		global ScreenWidth
		ScreenWidth, ScreenLength = 550,600

		if(configData.bounceCoefficient < 0):
			raise ValueError("bounceCoefficient cannot be negative")
		if(ScreenWidth <= 0) or (ScreenLength <= 0):
			print("ScreenWidth, ScreenLength: ", ScreenWidth, ", ", ScreenLength)
			raise ValueError("Negative dimensions detected")
		if(abs(baller.xcor()) > ScreenWidth) or (abs(baller.ycor()) > ScreenLength):
			raise Exception("Baller outside of screen boundaries")

	def wallCollision():
		if(abs(baller.xcor()) > ScreenWidth):
			global xVelocity
			xVelocity *= -1

	def reflectOnBouncer():
		if(bouncer.eventChecker.collisionCheck(baller)):
			global yVelocity
			yVelocity *= -1 * configData.bounceCoefficient
			print("Collision Activated")

	def floorCollision():
		if(baller.ycor() < -1*int(ScreenLength/2)):
			return True
		else:
			return False
	def reflectOnRoof():
		global yVelocity
		if(baller.ycor() > int((ScreenLength / 2))) and (yVelocity > 0):
			yVelocity *= -1 * configData.bounceCoefficient
			print("roof boinger")
	def collideWithBlock():
		global yVelocity
		yVelocity *= -1 * configData.bounceCoefficient