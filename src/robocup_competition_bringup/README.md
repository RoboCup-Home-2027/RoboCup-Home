# RoboCup 比赛版 ROS2 系统

该功能包提供现场一键启动入口 `competition_bringup.launch.py`，默认启动底盘、雷达、相机、Nav2 定位导航和 AR 标签识别。

## 编译

在 ROS2 Humble 工作空间根目录执行：

```bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select robocup_competition_bringup
source install/setup.bash
```

本资料包中的 `4.ROS2源码` 本身就是工作空间目录，可直接在该目录执行以下命令；也可以把其中的 `src` 复制或软链接到已有工作空间。底层依赖包需要先完成编译。

## 现场启动

```bash
source install/setup.bash
ros2 launch robocup_competition_bringup competition_bringup.launch.py
```

默认参数：

- 地图：`wheeltec_nav2/map/WHEELTEC.yaml`
- Nav2：`param/wheeltec_params/param_mini_mec.yaml`
- AR 标签：ID `582`，边长 `0.10 m`
- TTS：默认关闭

使用自建比赛地图：

```bash
ros2 launch robocup_competition_bringup competition_bringup.launch.py map:=/home/wheeltec/maps/competition.yaml
```

启用 TTS 测试：

```bash
ros2 launch robocup_competition_bringup competition_bringup.launch.py enable_tts:=true tts_text:='已找到目标物品'
```

## 现场检查

```bash
ros2 topic list
ros2 topic echo /scan --once
ros2 topic echo /camera/color/camera_info --once
ros2 run tf2_tools view_frames
ros2 node list
```

如虚拟机与主控跨机通信异常，先统一两端 `ROS_DOMAIN_ID`，并按资料中的 Docker 停止、重启和 talker/listener 流程排查。比赛前需要根据实际车型修改 Nav2 参数文件和底盘模型。

## 工作空间脚本

- `build_robocup.sh`：加载 ROS2 Humble、安装依赖并编译整个工作空间。
- `start_robocup.sh`：加载工作空间并启动比赛版系统，支持把 `map:=`、`params:=` 等参数继续传入。
