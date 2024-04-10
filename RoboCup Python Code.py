import subprocess
import math
import urllib.request
import requests

    


def run_command(command,target_word):
    global x
    x = 0
    process = subprocess.Popen(command,stdout=subprocess.PIPE,shell=True)
    output = b''
    while True and x <= 9:
        line = process.stdout.readline()
        if not line:
            break
        output += line

        decoded_line = line.decode().strip()
        #print(decoded_line) #PRINTS RAW DATA


        if target_word in decoded_line:
            i = decoded_line.index(target_word)
            start_index = i + length_of_blah
            end_index = start_index + length_of_wanted
            global extracted_numbers
            extracted_numbers = decoded_line[start_index:end_index]
            #print("EXTRACTED",item, coord,":" , extracted_numbers)
            ball_position = [float(extracted_numbers)]
            break
        else:
            
            if x>9:
                return (0,0)
            else :
                x+=1

       


    

    process.kill()
    return output.decode(), extracted_numbers

robHasBall = False
global x 
x = 0
while True:
    
    
    
    
    
    netX = -800
    netY = 0



    home = "home"
    matthans = "matthans"
    Desktop = "Desktop"
    USEDTHISONE = "USEDTHISONE"
    command = "./bin/client -s"
    directory = "home/matthans/Desktop/USEDTHISONE"    
    
    full_command = f"cd .. && cd .. && cd .. &&  cd .. && cd {home} && cd {matthans} && cd {Desktop} && cd {USEDTHISONE} && {command}"
    


    target_word = "-Robot(B) ( 1/ 1): "
    item = "Robot"
    coord = "X"
    #Robot X
    length_of_blah = 57
    length_of_wanted = 8
    output = run_command(full_command,target_word)
    RobotX = float(extracted_numbers)
    coord = "Y"
    #Robot Y
    length_of_blah = 67
    length_of_wanted = 8  
    output = run_command(full_command,target_word)   
    RobotY = float(extracted_numbers)
   
    robotPos = [RobotX,RobotY]

    #print("Robot Position = ", robotPos)


    #Robot Angle
    target_word = "-Robot(B) ( 1/ 1): "
    item = "Robot"
    coord = "Angle"
    #Robot X
    length_of_blah = 83
    length_of_wanted = 7
    output = run_command(full_command,target_word)
    robotAngle = float(extracted_numbers)
    output = (0,0)

    robotAngle = [robotAngle]
    robotAngle = robotAngle[0]




    if robHasBall == False:
        target_word = "Ball ( 1/ 1): "
        item = "ball"
        coord = "X"
        #Ball X
        length_of_blah = 30
        length_of_wanted = 8
        output = run_command(full_command,target_word)
        BallX = float(extracted_numbers)
        coord = "Y"
        #Ball Y
        length_of_blah = 40
        length_of_wanted = 8
        output = run_command(full_command,target_word)
        BallY = float(extracted_numbers)
        output = run_command(full_command,target_word)   

        ballPos = [BallX,BallY]
        #print("BallX: ",BallX," , BallY: ",BallY)

        #Angle 0 is facing Computers.
        #Angle 90 is Towards Solder
        #Angle 180 is at door.
        #Angle 270 is at lockers.
        # Calculate the angle of the line connecting the robot and the ball with respect to the x-axis
        angle_to_ball = math.atan2(BallY - RobotY, BallX - RobotX)
        angle_to_ball_deg = math.degrees(angle_to_ball)
        #print(angle_to_ball)
        #print("ANGLE TO BALL DEG = ", angle_to_ball_deg)
        # Adjust the angle based on the orientation of the robot
        angle_from_robot = angle_to_ball_deg - math.degrees(robotAngle) 
        # Ensure the angle is within [0, 360) range
        #angle_from_robot %= 360
        if angle_from_robot <0:
            angle_from_robot += 360
        

       



        


        AngleRobToBall = angle_from_robot
        robotAngle = math.degrees(robotAngle)

    kick = 'http://172.20.10.8/kick'
    rigt = 'http://172.20.10.8/rigt'
    left = 'http://172.20.10.8/left'
    frwd = 'http://172.20.10.8/frwd'
    serl = 'http://172.20.10.8/serl'
    stop = 'http://172.20.10.8/stop'
    bkwd = 'http://172.20.10.8/bkwd'
    

    angle_to_net = math.atan2(netY - RobotY, netX - RobotX)
    angle_to_net_deg = math.degrees(angle_to_net)
    angle_to_net_deg=angle_to_net_deg- math.degrees(robotAngle)

    if angle_to_net_deg <0:
        angle_to_net_deg = angle_to_net_deg+360

    #print("ANGLE TO NET = ", angle_to_net_deg)
    distanceNetToRobot = math.sqrt((int(netX)-int(robotPos[0]))**2+(int(netY)-int(robotPos[1]))**2)
    #print("Distance to Net = : ", distanceNetToRobot)

    distanceBallToRobot = math.sqrt((int(ballPos[0])-int(robotPos[0]))**2+(int(ballPos[1])-int(robotPos[1]))**2)
    #print("DISTANCE BALL TO ROBOT",distanceBallToRobot)
    print("ANGLE TO BALL = ",AngleRobToBall)
    
    ballAngle = robotAngle - AngleRobToBall
    if ballAngle <0:
        ballAngle+=360
    print("Robot Heading: ",robotAngle)
    #print("DIFFERENCE IN ANGLE FROM ROBOT TO BALL",ballAngle)



    if output == (0,0) or (BallX == RobotX and BallY == RobotY):
        response = requests.get(stop)
        print("Stopping Robot")
    elif distanceBallToRobot < 110 and ballAngle < 25:
        robHasBall = True
        print("Robot Has Ball")
        response = requests.get(kick)
        robHasBall = False
        print("KICKED IN NET")
    elif AngleRobToBall < 5 or AngleRobToBall > 355:
        response = requests.get(frwd)
        print("GOING FORWARD")
    elif AngleRobToBall > 180 :
        response = requests.get(rigt)
        print("Sent right command")
    elif AngleRobToBall <= 180 :
        response = requests.get(left)
        print("Sent left command")
    
    
    
    if distanceBallToRobot > 110 or ballAngle > 25:
        robHasBall = False

    
    if robHasBall:
        if angle_to_net_deg < 5 and distanceNetToRobot<800 and distanceNetToRobot>500 and abs(RobotY)<550:
            response = requests.get(kick)
            robHasBall = False
            print("KICKED IN NET")
        elif angle_to_net_deg < 5 and distanceNetToRobot<500:
            response = requests.get(bkwd)
            print("Moving BACKWARD")
        elif angle_to_net_deg < 5:
            response = requests.get(frwd)
            print("Going Forward")
        elif angle_to_net_deg >= 180:
            response = requests.get(rigt)
            print("Spinning Right")
        elif angle_to_net_deg < 180:
            response = requests.get(left)
            print("Spinning Left")
       