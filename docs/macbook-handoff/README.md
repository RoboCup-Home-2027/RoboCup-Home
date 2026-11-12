# MacBook / Codex 交接入口

MacBook 上的新 Codex 请按以下顺序阅读：

1. `MACBOOK_CODEX_交接清单.md`：Mac 环境、SSH、只读盘点、快照和实车安全边界；
2. `../PROJECT_CONTEXT.md`：仓库原有项目背景与目标硬件；
3. `../HANDOFF.md`：仓库原有启动入口；
4. `../STATUS.md`：仓库原有构建状态与未解决依赖；
5. `RoboCup@Home校赛技术方案.md`：团队总体技术路线；
6. `ROS2-V2.0常用指令.txt`：厂商候选命令，仅可在核对实际功能包后使用；
7. `references/`：X5、C30D、树莓派和比赛规则原始资料。

## 重要限制

- 仓库源码不一定等于实车当前工作区；首次现场必须先只读盘点和备份。
- 仓库不保存 Wi-Fi、SSH、OpenAI、GitHub 或其他凭据。
- 第一阶段禁止启动底盘、Nav2、键盘控制和机械臂。
- 不要用厂商压缩包或本仓库整目录覆盖车载 `~/wheeltec_ros2`。
- `src/tts_make_ros2/audio/2000-01-01_08:56:03.wav` 的文件名包含冒号，Windows 无法完整 checkout；Mac/Linux 可以正常克隆。

## MacBook 首次开始

```bash
git clone https://github.com/RoboCup-Home-2027/RoboCup-Home.git
cd RoboCup-Home
codex
```

随后向 Codex 发送 `MACBOOK_CODEX_交接清单.md` 最后一节提供的首条消息。

