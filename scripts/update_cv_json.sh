#!/bin/bash

# 将 Markdown 简历转换并更新为 CV JSON 的脚本
# 作者：Yuan Chen

# 设置仓库根目录
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 定义文件路径
CV_MARKDOWN="$BASE_DIR/_pages/cv.md"
CV_JSON="$BASE_DIR/_data/cv.json"
CONFIG_FILE="$BASE_DIR/_config.yml"

# 检查 Python 脚本是否存在
PYTHON_SCRIPT="$BASE_DIR/scripts/cv_markdown_to_json.py"
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script not found at $PYTHON_SCRIPT"
  exit 1
fi

# 检查 Markdown 简历文件是否存在
if [ ! -f "$CV_MARKDOWN" ]; then
  echo "Error: Markdown CV not found at $CV_MARKDOWN"
  exit 1
fi

# 执行 Python 脚本进行转换
echo "Converting markdown CV to JSON..."
python3 "$PYTHON_SCRIPT" --input "$CV_MARKDOWN" --output "$CV_JSON" --config "$CONFIG_FILE"

# 检查转换是否成功
if [ $? -eq 0 ]; then
  echo "Successfully updated CV JSON file at $CV_JSON"
  
  # 可选：构建 Jekyll 站点以预览变更
  echo "Would you like to build the Jekyll site to see the changes? (y/n)"
  read -r answer
  if [[ "$answer" =~ ^[Yy]$ ]]; then
    echo "Building Jekyll site..."
    cd "$BASE_DIR" && bundle exec jekyll serve
  fi
else
  echo "Error: Failed to update CV JSON file"
  exit 1
fi

exit 0
