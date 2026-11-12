# MacBook + Codex 现场开发交接清单

> 用途：把本文件复制到 MacBook，作为 MacBook 上 Codex 的首要上下文。本文不依赖原聊天记录。
>
> 当前状态：尚未完成实物型号核验，也尚未从车载主控导出实际 ROS2 工作区。先盘点、备份，再修改。

## 1. 项目目标与当前技术路线

项目为 RoboCup@Home 校赛家庭服务机器人，计划实现：

1. 激光 SLAM 建图；
2. Nav2 多房间导航与动态避障；
3. ArUco/数字标签及 YOLO 目标识别；
4. TTS 语音报告；
5. 异常停车、日志记录和比赛流程自动化。

现有方案采用 ROS2 Humble，记录的硬件路线为：

- WHEELTEC R550/R550A 麦克纳姆底盘；
- RDK X5 车载主控；
- C30D STM32 底盘控制板；
- 镭神 N10P 激光雷达；
- RGB 或 RGB-D 相机；
- 机械臂可能为 4 自由度或 6 自由度，尚待实物确认。

以上是方案和厂商资料中的信息，不得当作已经核验的实物事实。第一次现场工作必须拍照确认主控、C30D 版本、雷达、相机、机械臂自由度和编码器类型。

## 2. 当前 Windows 工作区事实

- 原工作区：`E:\RoboCup校赛`
- 当前不是 Git 仓库。
- `RoboCup-Home` 和 `RoboCup-Home-win` 目录当前为空。
- 主要内容是厂商资料、镜像、视频和答辩材料，不是已经整理好的比赛源码。
- `A 移动机器人使用资料` 约 87.53 GB。
- `2026资料` 约 6.77 GB。
- 不要把约 94 GB 的资料目录整体复制到 MacBook，也不要直接初始化成一个大 Git 仓库。
- 真正正在车上运行的 ROS2 工作区预计位于 RDK X5 的 `~/wheeltec_ros2`，需要从实物只读盘点后再导出。

Windows 端最值得保留/选择性复制的资料：

- `RoboCup@Home校赛技术方案.docx`
- `附件1 RoboCup机器人世界杯中国赛家庭组项目校赛暨北京化工大学智能服务机器人大赛规则手册.pdf`
- `A 移动机器人使用资料/4.ROS2系列教程/ROS2-V2.0常用指令.txt`
- `A 移动机器人使用资料/4.ROS2系列教程/6.ROS2补充资料/X3_X5派WHEELTEC_ROS2小车TROS功能补充手册/WHEELTEC R550 FOR X3&X5使用手册20250526.pdf`
- `2026资料/2.WHEELTEC R550-V550 ROS教育机器人运动底盘资料/1.硬件说明与底盘问题排查/2.整车到手自检程序使用说明/C30D主板客户端辅助质检使用手册_2025.01.13_V2.0.pdf`

## 3. 系统与网络信息

厂商手册给出的默认信息如下，现场可能已被修改：

- 小车热点：`wheeltec_sunrise`
- 车载主控默认地址：`192.168.0.100`
- SSH 用户：`wheeltec`
- ROS2 工作区：`/home/wheeltec/wheeltec_ros2`
- TogetherROS 工作区：`/home/wheeltec/wheeltec_tros`

热点和 SSH 凭据不得提交到仓库；从厂商手册、密码管理器或现场负责人处获取。

| 信息 | 当前来源 | 状态 |
|---|---|---|
| Windows 工作区不是 Git 仓库、资料体积约 94 GB | Windows 实测 | 已确认 |
| RDK X5、N10P、ROS2 Humble 技术路线 | 团队技术方案 | 待实物确认 |
| `192.168.0.100`、`wheeltec`、工作区路径 | 厂商手册 | 待现场确认 |
| 机械臂资料主要为 ROS1 Melodic | 本地资料盘点 | 不代表实车当前环境 |
| 上电静置 10 秒进行 IMU 零点标定 | C30D 厂商手册 | 适用性待实物/固件确认 |

ROS2 Humble 与 TogetherROS 不应在同一个 shell 中混合加载。比赛主线优先使用：

```bash
source /opt/ros/humble/setup.bash
source /home/wheeltec/wheeltec_ros2/install/setup.bash
```

不要同时加载 `/opt/tros/...`，除非当前任务明确需要 RDK 的 TogetherROS/NPU 例程，并且已经确认环境隔离方式。

## 4. MacBook 上的准备工作

### 4.1 安装基础工具

先确认架构和系统：

```bash
uname -m
sw_vers
git --version
ssh -V
rsync --version
```

Apple Silicon 应显示 `arm64`。如缺少开发工具：

```bash
xcode-select --install
```

### 4.2 安装 Codex CLI

使用官方安装方式之一：

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
```

或已有 Homebrew 时：

```bash
brew install --cask codex
```

验证并登录：

```bash
codex --version
codex
```

登录凭据只保存在用户环境中。不得把 OpenAI API Key、ChatGPT 令牌、SSH 私钥或密码写入项目仓库。

### 4.3 建立轻量工作区

```bash
mkdir -p ~/Projects/robocup-home/{docs,src,config,scripts,maps,logs,vehicle_snapshot}
cd ~/Projects/robocup-home
git init
```

只把文本源码、配置、脚本、小型文档和地图纳入 Git。默认排除：

- `build/`、`install/`、`log/`；
- rosbag 大文件；
- 虚拟机和系统镜像；
- 视频、压缩包、模型权重；
- 密钥和包含密码的配置文件。

MacBook 当前阶段不要求安装 Ubuntu 虚拟机。Mac 主要承担 SSH、Codex、Git、文件同步、日志查看和浏览器监控。RViz2/ROS2 多机深度调试暂时使用原 Windows 电脑的 Ubuntu 22.04 虚拟机。

## 5. MacBook 第一次连接小车

1. 在有互联网时预先安装并登录 Codex；
2. 连接 `wheeltec_sunrise`；
3. 禁止同时连接会改变路由的 VPN；
4. 小车热点可能不提供互联网。若 Codex 断网，保持当前终端，由人工按本文执行只读命令；也可使用有线网/第二网络接口提供互联网，但必须先检查路由没有改变小车网段；
3. 进行只读连接检查：

```bash
ping -c 4 192.168.0.100
ssh wheeltec@192.168.0.100
```

登录后先运行以下只读盘点，不要马上启动或修改程序：

```bash
hostname
hostname -I
uname -a
cat /etc/os-release
uname -m
echo "$ROS_DISTRO"
free -h
df -h
ls -la /home/wheeltec
ls -la /home/wheeltec/wheeltec_ros2
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
```

确认 ROS2 环境：

```bash
source /opt/ros/humble/setup.bash
source /home/wheeltec/wheeltec_ros2/install/setup.bash
ros2 pkg prefix turn_on_wheeltec_robot
ros2 pkg prefix wheeltec_robot_nav2
ros2 node list
ros2 topic list
```

如果 `echo "$ROS_DISTRO"`、工作区路径或功能包不存在，停止套用厂商命令，先记录实际环境。

## 6. 导出车载工作区快照

在 MacBook 新终端中执行。第一次只做从小车到 Mac 的读取，不要反向覆盖小车。先建立带时间戳的新目录并 dry-run：

```bash
SNAPSHOT_DIR="$HOME/Projects/robocup-home/vehicle_snapshot/$(date +%Y%m%d-%H%M%S)-wheeltec_ros2"
mkdir -p "$SNAPSHOT_DIR"

rsync -av \
  --dry-run \
  --itemize-changes \
  --no-owner \
  --no-group \
  --exclude build \
  --exclude install \
  --exclude log \
  --exclude '*.bag' \
  --exclude '*.db3' \
  wheeltec@192.168.0.100:/home/wheeltec/wheeltec_ros2/ \
  "$SNAPSHOT_DIR/"
```

人工核对 dry-run 只显示从小车读取文件后，删除 `--dry-run` 再执行一次。随后生成清单：

```bash
find "$SNAPSHOT_DIR" -type f -print0 | sort -z | xargs -0 shasum -a 256 > "$SNAPSHOT_DIR.sha256"
chmod -R a-w "$SNAPSHOT_DIR"
```

原始快照只读保存，不直接在其中开发。把需要修改的源码复制到 `src/` 后纳入 Git。

然后由 MacBook 上 Codex：

1. 读取全部源码和配置；
2. 识别底盘、雷达、相机、SLAM、Nav2、视觉和 TTS 功能包；
3. 记录实际 launch 文件和参数文件；
4. 查找已有自定义改动，不能用厂商压缩包覆盖；
5. 在本地 Git 中建立首次基线提交；
6. 输出“现有系统清单”和“待确认问题”，经过人工确认后再修改。

禁止直接把 Windows 中的 `x5_src_250401.zip` 覆盖到车上。车载系统可能包含更新配置和已经调过的参数。

## 7. 已知启动命令，仅作验证候选

这些命令来自厂商资料，必须先用 `ros2 pkg prefix` 和实际 launch 文件验证。**第一阶段只读盘点期间禁止执行本节任何命令。**

底盘：

风险：占用底盘串口，可能允许后续速度指令驱动车轮。

```bash
ros2 launch turn_on_wheeltec_robot turn_on_wheeltec_robot.launch.py
```

雷达：

风险：占用雷达设备；通常不驱动车轮。

```bash
ros2 launch turn_on_wheeltec_robot wheeltec_lidar.launch.py
ros2 topic hz /scan
```

相机：

风险：占用相机和算力；通常不驱动车轮。

```bash
ros2 launch turn_on_wheeltec_robot wheeltec_camera.launch.py
```

键盘控制：

风险：会发布速度指令并驱动车轮，必须架空车轮并由人工监护。

```bash
ros2 run wheeltec_robot_keyboard wheeltec_keyboard
```

SLAM Toolbox：

风险：本身通常不驱动车轮，但常与遥控运动配合使用。

```bash
ros2 launch wheeltec_slam_toolbox online_sync.launch.py
```

保存地图：

风险：会在车载文件系统写入地图文件。

```bash
ros2 launch wheeltec_nav2 save_map.launch.py
```

Nav2：

风险：可能自动发布速度指令并驱动车轮，必须完成底盘、TF、地图和急停验证后才可启动。

```bash
ros2 launch wheeltec_nav2 wheeltec_nav2.launch.py
```

不得在 MacBook 和小车上同时启动两份底盘驱动、雷达驱动或相同的导航系统。MacBook 默认只发 SSH 命令和查看状态，实际节点运行在 RDK X5。

## 8. 实车安全边界

任何可能发布速度、控制机械臂、烧写固件或修改底层参数的操作，都必须人工确认并满足：

- 首次电机测试时四轮完全架空；
- 一人操作，一人守在电机使能开关旁；
- 机械臂运动范围内无人、无遮挡；
- 上电后的前 10 秒保持车体静止，等待 IMU 零点标定；
- 不烧写 STM32，除非已确认 C30D 版本、机械臂自由度、GMR/霍尔编码器和固件文件完全匹配；
- 不修改机械臂舵机零位；
- 不改网络、串口号、Udev 规则或 `/opt/ros`，除非已有备份和回退方案；
- 不运行来源不明的 `sudo`、递归删除或全盘覆盖命令；
- Codex 不得在无人看守时执行实车运动测试。

## 9. 机械臂特别说明

`2026资料` 中机械臂现成功能包主要是 ROS1 Melodic，使用 `roslaunch`；比赛主线是 ROS2 Humble。资料还存在 2024 源码包与 2025 命令说明不完全一致的问题。

在 ROS2 底盘、雷达、建图和导航闭环完成前，不要把机械臂 ROS1 包直接混入 ROS2 工作区。后续应明确选择：

1. ROS1 容器独立控制机械臂；
2. ROS1/ROS2 Bridge；
3. 根据串口协议实现原生 ROS2 机械臂节点。

该决策需要实物和车载代码盘点后再做。

## 10. MacBook 上 Codex 的职责

Codex 应按以下顺序工作：

1. 只读盘点实物、系统、ROS 环境和车载工作区；
2. 建立本地 Git 基线和可回退备份；
3. 整理一条最小启动链：底盘 → 雷达 → SLAM → Nav2；
4. 为每一步给出可验证指标，如 `/odom`、`/scan` 频率、TF 连通和停车响应；
5. 每次只修改一个问题所需的最少文件；
6. 本地审查 diff 后，仅同步明确文件到小车；
7. 实车测试前说明将启动哪些节点、可能产生什么运动；
8. 保留地图、参数、日志、rosbag 和代码版本对应关系；
9. 最终形成一条比赛启动命令，并确保电脑断开后小车仍可独立运行；
10. 出现硬件型号、网络或固件歧义时停止并询问，不得猜测。

任何 Mac → 小车回传都必须先列出明确文件清单、备份远端原文件并 dry-run。禁止使用 `rsync --delete`，禁止整目录覆盖 `~/wheeltec_ros2`。具体回传命令应在确认实际目录和备份位置后再生成，不能提前套模板。

Codex 当前不应做：

- 重装车载系统；
- 替换整个 ROS2 工作区；
- 升级系统 Python、ROS2 或底层驱动；
- 为方便而重构厂商代码；
- 安装与比赛无关的软件；
- 未备份就修改地图、Nav2 参数或设备规则。

## 11. 第一次现场必须补齐的信息

- [ ] 整车正面、侧面照片；
- [ ] RDK X5 主控板和接口照片；
- [ ] C30D 板丝印，确认 1.0/2.0/2.1；
- [ ] 机械臂关节数量；
- [ ] 雷达铭牌，确认是否 N10P；
- [ ] 相机型号，确认 RGB/RGB-D；
- [ ] 编码器类型和减速比；
- [ ] 小车热点、IP、SSH 用户是否仍为默认值；
- [ ] Ubuntu、ROS2、内核版本；
- [ ] 实际工作空间和比赛代码位置；
- [ ] 现有地图、Nav2 参数和自定义 launch；
- [ ] 底盘、雷达、相机、机械臂分别是否能单独运行；
- [ ] 电池续航、充电器、电机使能和急停方式；
- [ ] 现场是否允许自带路由器/手机热点；
- [ ] 比赛时是否能获得外网；
- [ ] 电脑断开后，小车程序是否继续运行。

## 12. 阶段验收标准

第一阶段完成条件：

- MacBook 能稳定 SSH 登录小车；
- 车载工作区已只读备份到 Mac；
- 硬件型号和软件版本已经记录；
- 尚未对小车做不可逆修改。

第二阶段完成条件：

- 底盘低速控制正常，松键及时停车；
- `/odom` 连续更新；
- `/scan` 频率稳定、方向正确；
- TF 树无明显断裂；
- 可以完成小范围建图并保存地图。

第三阶段完成条件：

- Nav2 连续 3 次完成指定路线；
- 关键点到达误差约 0.3 m 以内；
- 识别结果连续 3 帧一致；
- 异常时能清零速度并提示人工接管；
- 比赛程序在 RDK X5 上独立运行，MacBook 只负责监控和救场。

## 13. 给 MacBook 上 Codex 的首条消息

在 MacBook 克隆 `https://github.com/RoboCup-Home-2027/RoboCup-Home.git`，进入仓库后启动 Codex，并发送：

```text
请完整阅读 docs/macbook-handoff/MACBOOK_CODEX_交接清单.md，并同时阅读 docs/PROJECT_CONTEXT.md、docs/HANDOFF.md、docs/STATUS.md。先不要修改任何文件，也不要启动机器人运动。
请按交接清单完成第一阶段：检查 Mac 环境，指导我连接小车，对 RDK X5 和 ROS2 工作区做只读盘点，并把需要确认的信息列成清单。
每次涉及 sudo、网络修改、覆盖文件、启动底盘/机械臂或烧写固件前必须停下说明风险并等我确认。所有改动保持最小化，并先建立可回退基线。
```

