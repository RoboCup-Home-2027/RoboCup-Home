from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robocup_simulation',
            executable='trajectory_demo.py',
            name='trajectory_demo',
            output='screen'),
    ])
