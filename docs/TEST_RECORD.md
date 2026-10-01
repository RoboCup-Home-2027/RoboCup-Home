# Test Record

更新时间：2026-10-02

## 环境

- Ubuntu 22.04 虚拟机
- ROS2 Humble：`/opt/ros/humble`
- 未连接或启动真实机器人
- 未修改系统网络

## 已执行命令

```bash
source /opt/ros/humble/setup.bash
colcon list
colcon build --symlink-install
```

## 结果记录

`colcon list` 已识别比赛包及本地 Nav2、SLAM 和 Gazebo ROS 源码包，包括 `aruco`、`aruco_msgs`、`aruco_ros`、`robocup_competition_bringup`、`robocup_simulation`、`tts`、`turn_on_wheeltec_robot`、`wheeltec_nav2`、`slam_toolbox`、`gazebo_ros` 和 `gazebo_plugins`。

`rosdep install --from-paths src --ignore-src -r -y` 未执行成功，原因是当前系统 rosdep 尚未初始化。

使用提供的管理员密码尝试执行 `sudo rosdep init`，但下载默认源列表时网络连接被拒绝；因此没有继续修改系统软件源。

随后补齐 `bond_core`、`diagnostics`、Wheeltec 消息、`slam_toolbox`、`gazebo_ros_pkgs` 及图像公共包，完整构建已成功完成 68 个功能包。

当前工作空间的完整构建命令为：

```bash
rosdep install --from-paths src --ignore-src -r -y
```

APT 缓存中的 `libbondcpp-dev` 是 ROS1 包，未安装；它不能替代 Nav2 所需的 ROS2 `bondcpp`。

## 仿真联调记录

- 未启动真实机器人；仅启动 Gazebo 仿真服务端。
- `ros2 launch robocup_simulation mapping_simulation.launch.py gui:=false rviz:=false` 启动成功。
- 已验证 `/scan`、`/odom`、`/tf`、`/map`、`/imu/data` 和相机话题。
- 发布短时 `/cmd_vel` 后，`/odom` 位姿发生变化，说明底盘插件和运动链路可用。
- 已验证 `slam_mapping.launch.py` 启动 `async_slam_toolbox_node`。
- 已清理重复 Gazebo 实例后验证机器人可控：`/cmd_vel` 有订阅者，低速前进约 5 秒后 `/odom` 位姿发生明显变化；同一实例同时发布 `/scan`、`/odom`、`/map` 和 `/tf`，可在 RViz2 实时建图。
- 已加入 `trajectory_demo.py` 和 `trajectory_demo.launch.py`，可向 `/cmd_vel` 发布约 45 秒的低速矩形轨迹，末尾自动发布零速度停车；同时保留 `teleop_twist_keyboard` 键盘控制方式。
- 真实 Gemini 深度、N10P 驱动、麦克纳姆四轮运动、ArUco 识别和 TTS 硬件仍未现场测试。

## 完整仿真原始数据

2026-10-02 19:28（`ROS_DOMAIN_ID=31`）完成一轮约 49.8 秒的无界面完整仿真，并保存原始 ROS 2 bag：

```text
bags/sim_20261002_192808/
```

记录文件为 `sim_20261002_192808_0.db3`，大小约 2.5 GiB，共 26872 条消息。包含：

- `/camera/rgbd_camera/image_raw`：2919 条原始 RGB 图像
- `/camera/rgbd_camera/camera_info`：2891 条
- `/scan`：1944 条
- `/odom`：16068 条
- `/tf`：2728 条
- `/map`：26 条
- `/cmd_vel`：296 条

该轮记录中 `/imu/data` 消息数为 0，已在场景中补充 IMU `always_on` 和噪声定义；后续录制应重新确认 IMU 计数。bag 文件及目录已加入 `.gitignore`，保留在本机供 `ros2 bag play` 回放。

## 2026-10-03 全程建图运行

清理重复 Gazebo 实例后，启动唯一的 Gazebo、SLAM Toolbox 和 RViz2，执行了两轮自动路线。扩展路线持续约 274.8 秒，记录目录为：

```text
bags/full_map_20261003_094348_extended/
```

该 bag 约 149 MiB，共 320987 条消息，包含 `/scan` 8504 条、`/odom` 74190 条、`/tf` 235779 条、`/map` 137 条和 `/cmd_vel` 2377 条。最终地图已保存为：

```text
maps/competition_home_full.pgm
maps/competition_home_full.yaml
```

地图分辨率为 0.05 m/pixel，尺寸为 178 x 98（约 8.9 m x 4.9 m）。这次运行验证了完整的采集、SLAM 更新和地图保存流程，但由于当前仿真底盘是差速等效模型，长距离扫掠在部分墙体/门洞处发生碰撞，地图仍有未覆盖区域；不能将其视为比赛场地的最终全覆盖地图。真实麦克纳姆运动学接入后应重新执行覆盖路线。

## 图形显示修复

首次图形启动时，虚拟机的 Gazebo/RViz 面板为空，原因是默认相机没有对准场地，且虚拟机 OpenGL 兼容性导致 RViz GLSL 纹理链接报错。已在仿真启动入口中启用软件渲染和 X11 共享内存兼容设置，并在比赛世界中加入场地上方的初始俯视相机。修复后日志显示 Gazebo、`gzclient` 和 RViz2 均正常启动，RViz 使用软件 OpenGL 4.5。

查看记录：

```bash
source /opt/ros/humble/setup.bash
ros2 bag info bags/sim_20261002_192808
ros2 bag play bags/sim_20261002_192808
```

## Git 记录

- 本地提交：`初始化 RoboCup Home ROS2 工作空间`（最终哈希见交付报告）。
- 远程推送：已成功推送到 `origin/main`。
