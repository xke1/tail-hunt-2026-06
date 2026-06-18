#!/bin/bash
# 启动 OpenBB Workspace 本地数据后端
# 用法: 双击 或 终端跑  bash ~/Downloads/openbb/start_workspace_backend.sh
# 起来后保持这个终端窗口开着;关掉窗口=后端停。

cd "$(dirname "$0")"            # 切到脚本所在目录(~/Downloads/openbb)
source .venv/bin/activate        # 激活虚拟环境
echo "OpenBB 数据后端启动中… 浏览器 Workspace 连这个地址: http://127.0.0.1:6900"
echo "交互式 API 文档(可自己点着玩): http://127.0.0.1:6900/docs"
echo "按 Ctrl+C 停止。"
# 用 uvicorn 直接起 + 4个worker(openbb-api 自带的 --workers 有 bug,会卡慢被 Workspace 判掉线)
uvicorn openbb_platform_api.main:app --host 127.0.0.1 --port 6900 --workers 4
