from vsmntrobot import robot
x = 0

while True:
    robot.go()

while not robot.wall():
    robot.go()
    x += 1

robot.left()
robot.left()

while x > 0:
    robot.go()
    x -= 1
