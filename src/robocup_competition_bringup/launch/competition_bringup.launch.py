"""RoboCup 家庭组现场一键启动入口。

默认启动：底盘 + 雷达 + 相机 + Nav2 定位导航 + AR 标签识别。
TTS 默认关闭，避免启动时重复生成示例音频；确认讯飞离线资源可用后再启用。
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    sensor_dir = get_package_share_directory('turn_on_wheeltec_robot')
    nav_dir = get_package_share_directory('wheeltec_nav2')

    map_file = LaunchConfiguration('map')
    nav_params = LaunchConfiguration('params')
    use_aruco = LaunchConfiguration('enable_aruco')
    use_tts = LaunchConfiguration('enable_tts')
    marker_id = LaunchConfiguration('marker_id')
    marker_size = LaunchConfiguration('marker_size')
    tts_text = LaunchConfiguration('tts_text')

    sensors = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(sensor_dir, 'launch', 'wheeltec_sensors.launch.py')))

    nav_bringup = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav_dir, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'map': map_file,
            'params_file': nav_params,
            'use_sim_time': 'false',
            'slam': 'false',
            'autostart': 'true',
            'use_composition': 'True',
            'use_respawn': 'False',
        }.items())

    aruco = Node(
        condition=IfCondition(use_aruco),
        package='aruco_ros',
        executable='single',
        name='competition_aruco_detector',
        output='screen',
        parameters=[{
            'image_is_rectified': True,
            'marker_size': marker_size,
            'marker_id': marker_id,
            'reference_frame': 'camera_link',
            'camera_frame': 'camera_link',
            'marker_frame': 'aruco_marker_frame',
            'corner_refinement': 'LINES',
        }],
        remappings=[
            ('/camera_info', '/camera/color/camera_info'),
            ('/image', '/camera/color/image_raw'),
        ])

    tts = Node(
        condition=IfCondition(use_tts),
        package='tts',
        executable='tts_node',
        name='competition_tts',
        output='screen',
        parameters=[{'tts_text': tts_text}])

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=os.path.join(nav_dir, 'map', 'WHEELTEC.yaml'),
            description='比赛地图 YAML 文件路径'),
        DeclareLaunchArgument(
            'params',
            default_value=os.path.join(nav_dir, 'param', 'wheeltec_params', 'param_mini_mec.yaml'),
            description='Nav2 参数文件路径；麦克纳姆底盘默认 mini_mec'),
        DeclareLaunchArgument(
            'enable_aruco', default_value='true',
            description='是否启动 AR 标签识别'),
        DeclareLaunchArgument(
            'enable_tts', default_value='false',
            description='是否启动 TTS 节点'),
        DeclareLaunchArgument(
            'marker_id', default_value='582',
            description='比赛标签 ID'),
        DeclareLaunchArgument(
            'marker_size', default_value='0.10',
            description='标签边长，单位米'),
        DeclareLaunchArgument(
            'tts_text', default_value='已进入比赛模式',
            description='TTS 测试文本'),
        sensors,
        nav_bringup,
        aruco,
        tts,
    ])
