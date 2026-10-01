from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package_share = FindPackageShare('robocup_simulation')
    world_launch = PathJoinSubstitution([
        package_share, 'launch', 'competition_world.launch.py'])
    slam_launch = PathJoinSubstitution([
        package_share, 'launch', 'slam_mapping.launch.py'])
    rviz_config = PathJoinSubstitution([
        package_share, 'rviz', 'mapping.rviz'])

    return LaunchDescription([
        SetEnvironmentVariable('LIBGL_ALWAYS_SOFTWARE', '1'),
        SetEnvironmentVariable('QT_X11_NO_MITSHM', '1'),
        DeclareLaunchArgument('gui', default_value='true'),
        DeclareLaunchArgument('rviz', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(world_launch),
            launch_arguments={'gui': LaunchConfiguration('gui')}.items()),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(slam_launch),
            launch_arguments={'use_sim_time': 'true'}.items()),
        Node(
            package='rviz2',
            executable='rviz2',
            name='mapping_rviz',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            additional_env={'LIBGL_ALWAYS_SOFTWARE': '1', 'QT_X11_NO_MITSHM': '1'},
            condition=IfCondition(LaunchConfiguration('rviz')),
            output='screen'),
    ])
