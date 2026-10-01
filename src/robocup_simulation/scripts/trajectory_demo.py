#!/usr/bin/env python3
"""Publish a slow, repeatable trajectory for Gazebo simulation checks."""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class TrajectoryDemo(Node):
    def __init__(self):
        super().__init__('trajectory_demo')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.started = self.get_clock().now()
        self.timer = self.create_timer(0.05, self.tick)
        self.segments = [
            (8.0, 0.12, 0.0),
            (4.0, 0.0, 0.35),
            (8.0, 0.12, 0.0),
            (4.0, 0.0, 0.35),
            (8.0, 0.12, 0.0),
            (4.0, 0.0, 0.35),
            (8.0, 0.12, 0.0),
            (4.0, 0.0, 0.35),
            (1.0, 0.0, 0.0),
        ]

    def tick(self):
        elapsed = (self.get_clock().now() - self.started).nanoseconds / 1e9
        offset = 0.0
        command = (0.0, 0.0)
        finished = True
        for duration, linear_x, angular_z in self.segments:
            if elapsed < offset + duration:
                command = (linear_x, angular_z)
                finished = False
                break
            offset += duration

        msg = Twist()
        msg.linear.x, msg.angular.z = command
        self.publisher.publish(msg)
        if finished:
            self.get_logger().info('Trajectory complete; robot stopped.')
            self.timer.cancel()
            self.destroy_node()
            rclpy.shutdown()


def main():
    rclpy.init()
    node = TrajectoryDemo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()
