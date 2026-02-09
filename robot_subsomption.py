
from robot import * 

nb_robots = 0
debug = True

class Robot_player(Robot):

    team_name = "subsomption"
    robot_id = -1
    iteration = 0

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name=name, team=team)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):

        mode = 1 #les differents modes de comportement du robot
        
        sensor_to_wall = []
        sensor_to_robot = []
        for i in range (0,8):
            if  sensor_view[i] == 1:
                sensor_to_wall.append( sensors[i] )
                sensor_to_robot.append(1.0)
            elif  sensor_view[i] == 2:
                sensor_to_wall.append( 1.0 )
                sensor_to_robot.append( sensors[i] )
            else:
                sensor_to_wall.append(1.0)
                sensor_to_robot.append(1.0)

        def go_straight():
            translation = sensors[sensor_front]*0.5
            rotation = 0.0
            return translation, rotation, False
        
        def hateWall():
            translation = 0.6 * (sensor_to_wall[sensor_front] + sensor_to_wall[sensor_front_left] + sensor_to_wall[sensor_front_right]) / 3.0

            left = sensor_to_wall[sensor_front_left]*0.8 + sensor_to_wall[sensor_left]*0.6 + sensor_to_wall[sensor_rear_left]*0.3
            right = sensor_to_wall[sensor_front_right]*0.8 + sensor_to_wall[sensor_right]*0.6 + sensor_to_wall[sensor_rear_right]*0.3
            rotation = left - right
            return translation, rotation, False

        def Avoider():
            sensor_to_wall = []
            sensor_to_robot = []
            for i in range (0,8):
                if sensor_view[i] == 1:
                    sensor_to_wall.append( sensors[i] )
                    sensor_to_robot.append(1.0)
                elif sensor_view[i] == 2:
                    sensor_to_wall.append( 1.0 )
                    sensor_to_robot.append( sensors[i] )
                else:
                    sensor_to_wall.append(1.0)
                    sensor_to_robot.append(1.0)

            translation = (sensors[sensor_front] + sensors[sensor_front_left] + sensors[sensor_front_right]) / 3.0

            left = sensors[sensor_front_left]*0.8 + sensors[sensor_left]*0.6 + sensors[sensor_rear_left]*0.3
            right = sensors[sensor_front_right]*0.8 + sensors[sensor_right]*0.6 + sensors[sensor_rear_right]*0.3
            rotation = left - right

            #self.iteration = self.iteration + 1        
            return translation, rotation, False

        def loveBot():
            detected = False
            for i in range(0,8):
                if sensor_view[i] == 2 and sensor_team[i] != self.team_name :
                    detected = True
                    break

            if not detected:
                return Avoider()

            sensor_to_wall = []
            sensor_to_opps = []
            sensor_to_bros = []
            for i in range(0,8):
                if sensor_view[i] == 1:
                    sensor_to_wall.append(sensors[i])
                    sensor_to_opps.append(1.0)
                    sensor_to_bros.append(1.0)
                elif sensor_view[i] == 2 and sensor_team[i] != self.team_name :
                    sensor_to_wall.append(1.0)
                    sensor_to_opps.append(sensors[i])
                    sensor_to_bros.append(1.0)
                elif sensor_view[i] == 2 and sensor_team[i] == self.team_name :
                    sensor_to_wall.append(1.0)
                    sensor_to_opps.append(1.0)
                    sensor_to_bros.append(sensors[i]) 
                else:
                    sensor_to_wall.append(1.0)
                    sensor_to_opps.append(1.0)
                    sensor_to_bros.append(1.0)

            #distance: 1.0 far, 0.0 very close
            front_attraction = (
                1.5 * (1.0 - sensor_to_opps[sensor_front]) +
                1.0 * (1.0 - sensor_to_opps[sensor_front_left]) +
                1.0 * (1.0 - sensor_to_opps[sensor_front_right]) +
                0.5 * (1.0 - sensor_to_opps[sensor_left]) +
                0.5 * (1.0 - sensor_to_opps[sensor_right])
            ) 
            translation = 0.2 + front_attraction * 0.8


            left = (
                1.0 * (1.0 - sensor_to_opps[sensor_front_left]) + 
                1.0 * (1.0 - sensor_to_opps[sensor_left]) + 
                1.0 * (1.0 - sensor_to_opps[sensor_rear_left])
            )
            right = (
                1.0 * (1.0 - sensor_to_opps[sensor_front_right]) + 
                1.0 * (1.0 - sensor_to_opps[sensor_right]) + 
                1.0 * (1.0 - sensor_to_opps[sensor_rear_right])
            )
            rotation = (left - right)

            return translation, rotation, False
        
        # mur trop proche ?
        wall_danger = max(sensor_to_wall) > 0.7

        # robot adverse visible ?
        enemy_detected = False
        for i in range(8):
            if sensor_view[i] == 2 and sensor_team[i] != self.team_name:
                enemy_detected = True
                break
        
        if wall_danger:
            mode = 3      # hateWall (prio max)
        elif enemy_detected:
            mode = 2      # loveBot
        else:
            mode = 1      # go_straight

        if mode == 1:
            translation, rotation, _ = go_straight()
        elif mode == 2:
            translation, rotation, _ = loveBot()
        elif mode == 3:
            translation, rotation, _ = hateWall()

        if debug == True:
            if self.iteration % 100 == 0:
                print ("Robot",self.robot_id," (team "+str(self.team_name)+")","at step",self.iteration,":")
                print ("\tsensors (distance, max is 1.0)  =",sensors)
                print ("\t\tsensors to wall  =",sensor_to_wall)
                print ("\t\tsensors to robot =",sensor_to_robot)
                print ("\ttype (0:empty, 1:wall, 2:robot) =",sensor_view)
                print ("\trobot's name (if relevant)      =",sensor_robot)
                print ("\trobot's team (if relevant)      =",sensor_team)
                print(f"MODE ACTIF = {mode}")

        self.iteration = self.iteration + 1        
        return translation, rotation, False
