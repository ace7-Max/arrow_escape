# 箭头消除 · 方向突围

一个基于 Python + Pygame 的休闲益智小游戏。

## 游戏简介

棋盘上分布着上、下、左、右四个方向的箭头。点击箭头后：

- 前方无阻挡 → 箭头飞出棋盘并消失；
- 前方有阻挡 → 箭头撞到阻挡物后弹回，消耗一次失误。

失误 3 次本关失败；清空全部箭头通关。

## 开发环境

- 操作系统：Windows 11
- Python 版本：3.13.9
- Pygame 版本：2.6.1
- 开发工具：PyCharm 2024.2

## 安装和运行方法

1. 安装 Python 3.8+，安装时勾选 "Add Python to PATH"
2. 安装 Pygame：

   ```bash
   pip install pygame
   ```

3. 下载本项目：

   ```bash
   git clone https://github.com/ace7-Max/arrow_escape.git
   cd arrow_escape
   ```

4. 运行游戏：

   ```bash
   python main.py
   ```

## 游戏操作说明

| 操作 | 效果 |
|------|------|
| 鼠标左键点击箭头 | 尝试飞出，被阻挡则扣一次失误 |
| R 键 | 重新开始当前关卡 |
| ESC 键 | 返回开始界面 |

界面按钮：

- 开始界面：开始游戏 / 选择关卡 / 退出游戏
- 游戏界面：重新开始 (R) / 返回首页
- 通关界面：下一关 / 返回首页
- 失败界面：重玩本关 / 返回首页

## 游戏截图

### 开始界面
<img width="649" height="904" alt="屏幕截图 2026-09-19 153905" src="https://github.com/user-attachments/assets/ee553adf-4f5b-42f5-a5ad-bba115eba8ab" />


### 游戏界面
<img width="802" height="926" alt="动画" src="https://github.com/user-attachments/assets/9dacfbc7-bdbb-4f9d-b78f-c59e9a186b64" />



### 通关界面
<img width="650" height="912" alt="动画3" src="https://github.com/user-attachments/assets/19852407-1cfd-48a8-b90c-276caff1a2f7" />


### 失败界面
<img width="651" height="914" alt="动画2" src="https://github.com/user-attachments/assets/6b7e0139-1c4a-4e4a-b9e7-7507464035f7" />



## 项目结构

```
arrow_escape/
├── main.py              # 入口
├── config.py            # 常量配置
├── model/               # 数据与规则
│   ├── board.py
│   └── rules.py
├── controller/          # 游戏状态机
│   └── game.py
├── view/                # 渲染与动画
│   ├── renderer.py
│   └── effects.py
└── screenshots/         # 截图
```
