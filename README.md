# RoboCup Home ROS2 Workspace

这是 RoboCup Home 家庭组比赛的 ROS2 Humble 工作空间，面向 RDK X5 主控、STM32 F407 下位机和 Wheeltec 麦克纳姆底盘。当前工作空间包含底盘驱动、激光雷达与相机启动、Nav2 导航、ArUco 标签识别、TTS 语音包和比赛版统一启动入口。

## 环境目标

- ROS2 Humble
- RDK X5
- STM32 F407
- Wheeltec 麦克纳姆底盘
- 镭神 N10P 激光雷达
- Gemini 深度相机
- SLAM Toolbox
- Nav2
- ArUco/二维码识别
- TTS 语音播报
- `ROS_DOMAIN_ID=31`

## 构建

```bash
source /opt/ros/humble/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon list
colcon build --symlink-install
source install/setup.bash
```

## 比赛版启动

```bash
ros2 launch robocup_competition_bringup competition_bringup.launch.py
```

启动前请根据实际比赛地图替换 `maps/` 中的地图，并根据实际车型检查 `config/param_mini_mec.yaml`。本仓库只提供软件工作空间，不启动真实机器人、不修改网络配置。

详细背景、当前状态、交接事项和测试结果见 `docs/`。

