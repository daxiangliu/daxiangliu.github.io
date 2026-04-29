# 基础镜像：包含运行 Jekyll 所需依赖的 Ruby 环境
FROM ruby:3.2

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    nodejs \
    && rm -rf /var/lib/apt/lists/*


# 创建非 root 用户（UID 1000）
RUN groupadd -g 1000 vscode && \
    useradd -m -u 1000 -g vscode vscode

# 设置工作目录
WORKDIR /usr/src/app

# 设置工作目录权限
RUN chown -R vscode:vscode /usr/src/app

# 切换到非 root 用户
USER vscode

# 复制 Gemfile 到容器（`bundle install` 必需）
COPY Gemfile ./



# 安装 bundler 与依赖
RUN gem install connection_pool:2.5.0
RUN gem install bundler:2.3.26
RUN bundle install

# 启动 Jekyll 站点的默认命令
CMD ["jekyll", "serve", "-H", "0.0.0.0", "-w", "--config", "_config.yml,_config_docker.yml"]
