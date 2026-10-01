# Handoff

## 当前入口

```bash
cd ~/robocup_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 launch robocup_competition_bringup competition_bringup.launch.py
```

默认地图来自 `wheeltec_nav2/map/WHEELTEC.yaml`，默认参数为麦克纳姆底盘 `param_mini_mec.yaml`。比赛前应将实地保存的地图复制到 `maps/`，并通过 `map:=...` 指定。

## 启动前检查

1. 确认机器人不在可运动状态，真实硬件测试由现场负责人执行。
2. 确认主控和调试机使用 ROS2 Humble，必要时两端设置 `ROS_DOMAIN_ID=31`。
3. 检查底盘型号参数、激光雷达话题、Gemini 图像/相机信息话题和 TF。
4. 检查 ArUco 标签 ID/尺寸与比赛物品标签一致。
5. 语音启用前确认 CPU 架构、`libmsc.so`、离线资源和 APPID。

## 现场回退

如果统一入口失败，按模块启动底盘/传感器、Nav2 和 ArUco；通过 `ros2 node list`、`ros2 topic list`、`ros2 topic echo /scan --once` 和相机信息话题定位问题。任何未确认的依赖或参数变更都应记录在 `docs/STATUS.md`。

