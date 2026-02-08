# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Arthur Bonnault 21313394
#  Prénom Nom No_étudiant/e : Idrys Sylla 21311738
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import * 

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

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

        def Avoider():
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

            translation =  (sensors[sensor_front] + sensors[sensor_front_left] + sensors[sensor_front_right]) / 3.0

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

        """if self.robot_id == 0 :
            return Avoider()
        elif self.robot_id == 1:
            return HitNRun()
        else:
            return wanderer()"""

        return loveBot()
    

