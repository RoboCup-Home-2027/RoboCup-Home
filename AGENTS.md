# Agent Working Agreement

## Scope

本仓库用于 RoboCup Home 家庭组 ROS2 比赛系统。修改应围绕导航、寻物、语音反馈、底盘驱动、传感器配置和现场启动流程。

## Safety

- 不启动真实机器人，不向 `/cmd_vel` 发布运动指令。
- 不修改系统网络、Docker、主机时间或设备权限，除非用户明确要求。
- 不删除现有源码；不复制虚拟机镜像、构建目录、安装目录、日志目录或大型无关教程资料。
- 任何真实硬件测试前，先确认底盘悬空、急停和低速限制。

## Build and test

使用 ROS2 Humble：

```bash
source /opt/ros/humble/setup.bash
colcon list
colcon build --symlink-install
```

涉及跨机通信时，两端使用 `ROS_DOMAIN_ID=31`，仅通过 `ros2 topic list`、`ros2 topic echo` 和 talker/listener 做无运动验证。

## Change discipline

优先使用现有 Wheeltec launch、参数和消息接口。每次修改记录受影响的包、构建结果、缺失依赖和后续硬件验证事项；不伪造未验证的运行结果。

