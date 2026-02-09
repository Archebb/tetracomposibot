# Projet "robotique" IA&Jeux 2025
#
# Binome:
# Prénom Nom No_étudiant/e : Arthur Bonnault 21313394
# Prénom Nom No_étudiant/e : Idrys Sylla 21311738
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 
import math

nb_robots = 0

class Robot_player(Robot):

    team_name = "BOSY" # vous pouvez modifier le nom de votre équipe
    robot_id = -1 # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0 # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        #print(self.robot_id)

        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        translation = sensors[sensor_front]
        rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1

        def wanderer():
            translation = sensors[sensor_front]*0.8
            rotation = 1.0 * sensors[sensor_front_left] - 1.0 * sensors[sensor_front_right] + (random.random()-0.5)*0.1
            return translation, rotation, False

        """        
        def loveWall():
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

            translation = 0.6 * (sensor_to_wall[sensor_front] + sensor_to_wall[sensor_front_left] + sensor_to_wall[sensor_front_right]) / 3.0
            rotation = 0.8 * (sensor_to_wall[sensor_front_left] - sensor_to_wall[sensor_front_right]) + 0.6 * (sensor_to_wall[sensor_left] - sensor_to_wall[sensor_right]) + 0.3 * (sensor_to_wall[sensor_rear_left] - sensor_to_wall[sensor_rear_right])
            return translation, rotation, False
        """
        
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
        
        def hateBot():
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

            translation = 0.6 * (
                sensor_to_bros[sensor_front] +
                sensor_to_bros[sensor_front_left] +
                sensor_to_bros[sensor_front_right]
            ) / 3.0

            left = (
                sensor_to_bros[sensor_front_left]*0.8 +
                sensor_to_bros[sensor_left]*0.6 +
                sensor_to_bros[sensor_rear_left]*0.3
            )
            right = (
                sensor_to_bros[sensor_front_right]*0.8 +
                sensor_to_bros[sensor_right]*0.6 +
                sensor_to_bros[sensor_rear_right]*0.3
            )
            rotation = left - right

            # --- ROOOMBA-LIKE UNSTUCK ---
            front_bro_too_close = (
                sensor_to_bros[sensor_front] < 0.2 or
                sensor_to_bros[sensor_front_left] < 0.2 or
                sensor_to_bros[sensor_front_right] < 0.2
            )

            if front_bro_too_close and translation < 0.1:
                translation = -0.2   # recule
                rotation = 0.4       # tourne légèrement

            return translation, rotation, False
        
        def hateWall():
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
            translation = 0.6 * (sensor_to_wall[sensor_front] + sensor_to_wall[sensor_front_left] + sensor_to_wall[sensor_front_right]) / 3.0

            left = sensor_to_wall[sensor_front_left]*0.8 + sensor_to_wall[sensor_left]*0.6 + sensor_to_wall[sensor_rear_left]*0.3
            right = sensor_to_wall[sensor_front_right]*0.8 + sensor_to_wall[sensor_right]*0.6 + sensor_to_wall[sensor_rear_right]*0.3
            rotation = left - right
            return translation, rotation, False
        
        def dora():
            p = [-2.2464852586750874, 1.441803329394571, 3.0, 2.2033677756121137,
                      -2.241384994128072, 1.3470674521590515, 1.971694301872875, -0.6076243605712588]
            translation = math.tanh(
                p[0]
                + p[1] * sensors[sensor_front_left]
                + p[2] * sensors[sensor_front]
                + p[3] * sensors[sensor_front_right] )
            rotation = math.tanh(
                p[4]
                + p[5] * sensors[sensor_front_left]
                + p[6] * sensors[sensor_front]
                + p[7] * sensors[sensor_front_right] )
            return translation, rotation, False
        
        def subsomption():
            mode = 4 #les differents modes de comportement du robot
        
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
                """
                redefinition juste pour la subsomption
                """
                sensor_to_wall = []
                for i in range(8):
                    if sensor_view[i] == 1:
                        sensor_to_wall.append(sensors[i])
                    else:
                        sensor_to_wall.append(1.0)

                # --- normal Braitenberg wall avoidance ---
                translation = 0.6 * (
                    sensor_to_wall[sensor_front] +
                    sensor_to_wall[sensor_front_left] +
                    sensor_to_wall[sensor_front_right]
                ) / 3.0

                left = (
                    sensor_to_wall[sensor_front_left]*0.8 +
                    sensor_to_wall[sensor_left]*0.6 +
                    sensor_to_wall[sensor_rear_left]*0.3
                )
                right = (
                    sensor_to_wall[sensor_front_right]*0.8 +
                    sensor_to_wall[sensor_right]*0.6 +
                    sensor_to_wall[sensor_rear_right]*0.3
                )
                rotation = left - right

                # --- CRITICAL UNSTUCK FIX ---
                front_wall_close = (
                    sensor_to_wall[sensor_front] < 0.25 and
                    sensor_to_wall[sensor_front_left] < 0.25 and
                    sensor_to_wall[sensor_front_right] < 0.25
                )

                if front_wall_close:
                    translation = -0.2   # recule
                    rotation = 0.5       # tourne fort

                return translation, rotation, False

            # mur trop proche ?
            wall_danger = min(sensor_to_wall) < 0.3

            # robot adverse visible ?
            enemy_detected = False
            for i in range(8):
                if sensor_view[i] == 2 and sensor_team[i] != self.team_name:
                    enemy_detected = True
                    break
            
            # robot allie visible ?
            friend_detected = False
            for i in range(8):
                if sensor_view[i] == 2 and sensor_team[i] == self.team_name:
                    friend_detected = True
                    break
            
            if wall_danger:
                mode = 1      #
            elif friend_detected:
                mode = 2      #
            elif enemy_detected:
                mode = 3      #
            else:
                mode = 4      #

            if mode == 1:
                translation, rotation, _ = hateWall()
            elif mode == 2:
                translation, rotation, _ = hateBot()
            elif mode == 3:
                translation, rotation, _ = loveBot()
            elif mode == 4:
                translation, rotation, _ = wanderer()

            #print("mode : ", mode)
            return translation, rotation, False
        
        if self.robot_id == 0 :
            return hateBot()
        elif self.robot_id == 1:
            return loveBot()
        elif self.robot_id == 2:
            return dora()
        elif self.robot_id == 3:
            return subsomption()
        else:
            return subsomption()
        
        #return subsomption()