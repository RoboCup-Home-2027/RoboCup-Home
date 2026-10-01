import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, SetEnvironmentVariable
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = PathJoinSubstitution([
        FindPackageShare('robocup_simulation'), 'worlds', 'competition_home.sdf'])
    return LaunchDescription([
        SetEnvironmentVariable('LIBGL_ALWAYS_SOFTWARE', '1'),
        SetEnvironmentVariable('QT_X11_NO_MITSHM', '1'),
        DeclareLaunchArgument('world', default_value=world),
        DeclareLaunchArgument('gui', default_value='true'),
        ExecuteProcess(
            cmd=['gazebo', '--verbose', LaunchConfiguration('world')],
            condition=IfCondition(LaunchConfiguration('gui')),
            output='screen'),
        ExecuteProcess(
            cmd=['gzserver', '--verbose', LaunchConfiguration('world')],
            condition=UnlessCondition(LaunchConfiguration('gui')),
            output='screen'),
    ])
