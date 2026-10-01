# Status

更新时间：2026-10-02

## 已完成

- 已从 `https://github.com/RoboCup-Home-2027/RoboCup-Home.git` 克隆空仓库到 `~/robocup_ws`。
- 已创建 `src/`、`config/`、`launch/`、`maps/`、`docs/`。
- 已复制直接相关的底盘、Nav2、ArUco、TTS 和比赛启动源码。
- 已加入 README、AGENTS、项目背景、交接、测试记录和 `.gitignore`。
- 已执行 `source /opt/ros/humble/setup.bash` 和 `colcon list`。
- 已完成本地 Git 提交，提交信息为“初始化 RoboCup Home ROS2 工作空间”。
- GitHub 浏览器登录已验证为账号 `2545666`；该账号在 `RoboCup-Home-2027` 组织中显示为 Owner，目标仓库确实存在且为空。
- 已使用当前有效的 GitHub 认证将 `main` 推送到远端 `RoboCup-Home-2027/RoboCup-Home`。
- 此前令牌已经在聊天中暴露，应立即在 GitHub 中撤销，不再使用。
- 已纳入本地资料中的 `navigation2-humble` 源码，因为 Nav2 是本项目的直接依赖。
- 已补齐并纳入 ROS 2 依赖源码：`bond_core`、`diagnostics`、`BehaviorTree.CPP v3.8`、Wheeltec `wheeltec_robot_msg` 和 `serial_ros2`。
- 已安装 Ubuntu 22.04 编译依赖：GraphicsMagick C++、Ceres Solver、xtensor/xtl、OMPL。
- 已新增 `robocup_simulation` 仿真包，按规则手册建立约 10 m × 7 m（约 70 m²）的四房间赛场、中央走廊、0.8 m 门洞、入口/出口和基础家具模型。
- 已加入 Gazebo 11 比赛世界和机器人模型；当前仅有一条非阻塞连接警告。
- 已根据用户提供的原始场地图重新建模：外框 9.00 m x 13.33 m，内部尺寸参考 6.60 m、4.50 m、3.50 m、4.00 m 和 3.00 m，场地由横向近似图改为原图的纵向布局。
- 已从 Humble 分支源码编译 `slam_toolbox`，可用节点包括 `async_slam_toolbox_node`、`sync_slam_toolbox_node` 和 `map_and_localization_slam_toolbox_node`。
- 已从 ROS 2 `ros2` 分支源码编译 `gazebo_ros_pkgs`，包含 `gazebo_dev`、`gazebo_msgs`、`gazebo_ros` 和 `gazebo_plugins`；同时补齐 `camera_info_manager` 与 `camera_calibration_parsers`。
- 已将比赛世界切换为 ROS 2 Gazebo 插件。实测可收到 `/scan`、`/odom`、`/tf`、`/imu/data`、`/camera/rgbd_camera/image_raw` 和相机标定话题。
- 已实测 `slam_mapping.launch.py` 能启动 `async_slam_toolbox_node`，并使用工作空间内源码构建的 `slam_toolbox`。

## 构建状态

已执行 `source /opt/ros/humble/setup.bash`、`colcon list` 和 `colcon build --symlink-install --parallel-workers 2 --cmake-args -DBUILD_TESTING=OFF`。当前构建结果为 **68 个功能包成功**，包括 Nav2、Wheeltec 底盘、ArUco、TTS、Gazebo ROS 桥接、SLAM Toolbox、竞赛启动包及其直接依赖。

## 已知依赖风险

当前确认的环境问题：系统 rosdep 尚未初始化；之前尝试初始化时，下载默认源列表因网络连接被拒绝而失败。为完成本次离线构建，已从本地资料和上游 ROS 2 源码补齐直接依赖，并通过 `-DBUILD_TESTING=OFF` 跳过缺少 `test_msgs` 的 Nav2 测试目标。构建中仍有两类非阻塞警告：`serial_ros2` 的符号比较/未使用变量警告，Wheeltec 驱动的变长数组和反斜杠换行警告。导航包依赖 Nav2 发行版组件，TTS 依赖对应架构的科大讯飞离线库；实际主控上还需检查 `/dev` 设备、Gemini 话题、N10P 话题、车型参数和 TTS APPID/离线资源。
仿真限制：当前虚拟机没有真实 RDK X5、STM32 F407、Wheeltec 麦克纳姆底盘、N10P 或 Gemini 硬件；场景使用二维激光、RGB 相机和差速等效底盘完成算法联调。真实设备接入时需要替换传感器驱动、四轮麦克纳姆控制器、串口参数以及 Gemini 深度/点云话题。

已确认的仿真构建依赖：`gazebo11`、`libgazebo-dev`、`gazebo_ros_pkgs`（源码）、`camera_info_manager`（源码）、`camera_calibration_parsers`（源码）和 `slam_toolbox`（源码）。由于 ROS apt 源在当前虚拟机网络环境中不稳定，桥接包采用源码编译，没有伪造占位插件。

```bash
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

不要用未验证的占位代码替代缺失依赖。实际主控上还需检查 `/dev` 设备、Gemini 话题、N10P 话题、车型参数和 TTS APPID/离线资源。
