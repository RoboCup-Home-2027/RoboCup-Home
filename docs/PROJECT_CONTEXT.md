# Project Context

## 目标

构建一套可在 RoboCup Home 家庭组比赛现场部署的 ROS2 Humble 机器人系统，覆盖建图、定位、导航、寻物和语音报告。

## 目标平台

| 项目 | 目标 |
|---|---|
| 主控 | RDK X5 |
| 下位机 | STM32 F407 |
| 底盘 | Wheeltec 麦克纳姆轮 |
| 激光雷达 | 镭神 N10P |
| 深度相机 | Gemini |
| 中间件 | ROS2 Humble |
| 通信域 | `ROS_DOMAIN_ID=31` |

## 软件路线

SLAM Toolbox 用于二维建图，Nav2 用于定位、全局/局部规划和恢复行为，ArUco/二维码用于寻物基线识别，TTS 用于物品位置播报。统一入口 `robocup_competition_bringup` 默认启动底盘、雷达、相机、Nav2 和 ArUco；TTS 通过 launch 参数选择性启用。

## 当前源码

- `src/turn_on_wheeltec_robot`：底盘、雷达、相机、TF 和机器人模型。
- `src/wheeltec_robot_nav2`：地图、Nav2 参数和导航 launch。
- `src/aruco_ros-humble-devel`：ArUco 及消息包。
- `src/tts_make_ros2`：科大讯飞 TTS 包及离线资源。
- `src/robocup_competition_bringup`：比赛现场统一启动入口。

