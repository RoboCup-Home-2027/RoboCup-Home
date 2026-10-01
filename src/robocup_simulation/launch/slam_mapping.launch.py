from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    params = PathJoinSubstitution([
        FindPackageShare('robocup_simulation'), 'config', 'slam_params.yaml'])
    slam_launch = PathJoinSubstitution([
        FindPackageShare('slam_toolbox'), 'launch', 'online_async_launch.py'])
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                slam_launch),
            launch_arguments={
                'slam_params_file': params,
                'use_sim_time': LaunchConfiguration('use_sim_time'),
            }.items()),
    ])
