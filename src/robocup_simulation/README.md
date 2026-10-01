# RoboCup Home 仿真场地

场景依据用户提供的原始尺寸图重建：外框约 9.00 m x 13.33 m，图纸内部标注包含 6.60 m、4.50 m、3.50 m、4.00 m 和 3.00 m。模型包含餐厅、卧室、客厅、书房、两侧通道和休息区；墙高 0.6 m，门洞按图纸中的开口关系建模。

当前包提供兼容 Gazebo 11（Ubuntu 22.04 软件源）的场地 SDF、机器人 URDF 占位模型和启动入口。工作空间内已编译 `gazebo_ros_pkgs`，因此场景中的传感器和底盘可直接发布 ROS 2 话题。运行：

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch robocup_simulation competition_world.launch.py
```

推荐使用组合入口同时启动比赛场景、SLAM Toolbox 和 RViz2：

```bash
ros2 launch robocup_simulation mapping_simulation.launch.py
```

启动后可在 RViz2 使用 `2D Pose Estimate` 设置初始位姿、使用 `2D Goal Pose` 发布导航目标；建图过程中通过 `/cmd_vel` 发布速度指令驱动机器人探索场地。

机器人在 Gazebo 中使用蓝色底盘和黑色轮子显示。控制示例：

```bash
ros2 topic pub -r 10 /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.12}, angular: {z: 0.0}}"
```

停止机器人：

```bash
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.0}}"
```

RViz2 会实时显示 `/scan`、`/odom`、`/tf` 和 SLAM Toolbox 发布的 `/map`；用速度指令让机器人沿走廊和房间移动即可实时更新地图。

也可以直接运行内置的矩形轨迹演示（约 45 秒，结束后自动停车）：

```bash
ros2 launch robocup_simulation trajectory_demo.launch.py
```

键盘控制需要另开终端运行：

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r cmd_vel:=/cmd_vel
```

运行键盘控制时保持 Gazebo 仿真窗口和 RViz2 建图窗口开启；退出键盘节点或发布零速度即可停车。

虚拟机图形性能不足时可关闭 Gazebo 和 RViz 界面，仅运行服务端：

```bash
ros2 launch robocup_simulation mapping_simulation.launch.py gui:=false rviz:=false
```

建图时使用 `/scan`、`/odom` 和 `base_link`，SLAM Toolbox 启动入口为：

```bash
ros2 launch robocup_simulation slam_mapping.launch.py
ros2 launch robocup_simulation save_map.launch.py map_file:=maps/competition_home
```

当前仿真话题包括：

- `/scan`：镭神 N10P 的二维激光等效数据（`sensor_msgs/LaserScan`）
- `/odom`、`/tf`：差速运动学等效底盘里程计
- `/camera/rgbd_camera/image_raw`、`/camera/rgbd_camera/camera_info`：Gemini 相机的 RGB 等效数据
- `/imu/data`：IMU 数据

上述插件来自工作空间内的 `gazebo_ros_pkgs`、`camera_info_manager` 和 `camera_calibration_parsers` 源码构建。每次新终端运行前都要先加载：

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

当前模型是用于算法联调的移动底盘等效模型，麦克纳姆四轮运动学和真实 Gemini 深度/点云驱动仍需在拿到实物接口后替换或扩展。
