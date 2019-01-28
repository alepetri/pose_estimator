"""Module contains a position estimator for tricylce robot

Imports Used:
numpy
Classes:
PoseEstimator -- Estimates position and heading given sensory data
Module Constants:
STEERING_WHEEL_RADIUS -- radius of steering wheel
ENCODER_RESOLUTION -- ticks/revolution of encoder traction wheel
TURNING_RADIUS -- distance from steering wheel to back axel
"""

import numpy as np

STEERING_WHEEL_RADIUS = 0.2
ENCODER_RESOLUTION = 512
TURNING_RADIUS = 1


class PoseEstimator(object):
    """Objects perform coordinate and heading estimation.

    Methods:
    estimate -- estimate position and heading given sensory data
    Instance variables:
    sensor_weight -- (float) ranges from 1 (trust encoder) to 0 (trust imu)
    last_pose -- (list) [x,y,heading] data for latest position
    last_time -- (int) time data for latest position
    last_tick -- (int) encoder tick data for latsest position
    """

    def __init__(self, sensor_weight=0.5):
        """Initialize PoseEstimator object and instance variables.

        Keyword arguements:
        sensor_weight -- (default=0.5) ranges from 1 (trust encoder)
                          to 0 (trust imu)
        """
        self.sensor_weight = sensor_weight
        self.last_pose = [0, 0, 0]
        self.last_time = 0
        self.last_tick = 0

    def estimate(self, time, steering_angle, encoder_ticks,
                 angular_velocity_imu):
        """Estimate and return [x (m), y (m), heading (rad)]
        given data point [time (s), steering angle (rad), encoder ticks (tick),
                          angular velocity (rad/s)]

        Keyword arguements:
        time -- time of current reading
        steering_angle -- steering_angle of current reading
                          (relative to the robot body)
        encoder_ticks -- encoder_ticks of current reading
                         (relative to starting value)
        angular_velocity_imu -- imu value of current reading
        """
        delta_t = time - self.last_time
        delta_ticks = encoder_ticks - self.last_tick
        v_steering_encoder = (2 * np.pi * STEERING_WHEEL_RADIUS * delta_ticks
                              / ENCODER_RESOLUTION / delta_t)
        angular_velocity_encoder = v_steering_encoder * np.sin(steering_angle)
        if (steering_angle != 0):
            v_steering_imu = (angular_velocity_imu * TURNING_RADIUS
                              / np.sin(steering_angle))
            v_steering = self.sensor_fusion(v_steering_encoder, v_steering_imu)
            angular_velocity = self.sensor_fusion(angular_velocity_encoder,
                                                  angular_velocity_imu
                                                  )
        else:
            v_steering = v_steering_encoder
            angular_velocity = angular_velocity_encoder
        delta_heading = angular_velocity * delta_t
        delta_x = (v_steering * np.cos(steering_angle)
                   * np.cos(self.last_pose[2]) * delta_t)
        delta_y = (v_steering * np.cos(steering_angle)
                   * np.sin(self.last_pose[2]) * delta_t)
        self.last_time = time
        self.last_tick = encoder_ticks
        self.last_pose = np.add(self.last_pose,
                                [delta_x, delta_y, delta_heading]
                                )
        self.last_pose[2] = self.last_pose[2]%(2*np.pi)
        return self.last_pose

    def sensor_fusion(self, encoder_value, imu_value):
        """Do basic sensor fusion through confidence value"""
        return (encoder_value * (self.sensor_weight)
                + imu_value * (1-self.sensor_weight))
