from robot import *
import math

class Robot_player(Robot):
    team_name = "ExplorateurGA"

    def __init__(self, x, y, theta, name="n/a", team="n/a"):
        super().__init__(x, y, theta, name=name, team=team)
        self.param = [-2.2464852586750874, 1.441803329394571, 3.0, 2.2033677756121137,
                      -2.241384994128072, 1.3470674521590515, 1.971694301872875, -0.6076243605712588]

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        p = self.param
        translation = math.tanh(
            p[0]
            + p[1] * sensors[sensor_front_left]
            + p[2] * sensors[sensor_front]
            + p[3] * sensors[sensor_front_right]
        )
        rotation = math.tanh(
            p[4]
            + p[5] * sensors[sensor_front_left]
            + p[6] * sensors[sensor_front]
            + p[7] * sensors[sensor_front_right]
        )
        return translation, rotation, False