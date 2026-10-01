from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'map_file', default_value='maps/competition_home'),
        Node(
            package='nav2_map_server',
            executable='map_saver_cli',
            name='competition_map_saver',
            arguments=['-f', LaunchConfiguration('map_file')],
            parameters=[{'use_sim_time': True}],
            output='screen'),
    ])
