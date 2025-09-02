# Hadoop 安装指南（MacOS）

本指南将帮助你在 MacOS 系统上安装和配置 Hadoop。

## 目录
- [前### 4. 配置环境变量
将以下内容添加到 `~/.zshrc` 文件：

```bash
# Hadoop 环境变量
export HADOOP_HOME=/opt/homebrew/Cellar/hadoop/$(brew list --versions hadoop | awk '{print $2}')
export HADOOP_CONF_DIR=$HADOOP_HOME/libexec/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Java 环境变量（根据实际安装路径调整）
export JAVA_HOME=/opt/homebrew/opt/openjdk@11
# 或者使用系统工具查找：export JAVA_HOME=$(/usr/libexec/java_home -v 11)
```

重新加载配置：
```bash
source ~/.zshrc
```

### 5. 复制配置文件
```bash
# 复制项目中的配置文件到 Hadoop 配置目录
cp hadoop_config/* $HADOOP_CONF_DIR/
```
- [安装步骤](#安装步骤)
- [配置说明](#配置说明)
- [验证安装](#验证安装)
- [常见问题](#常见问题)

## 前置条件

1. Java 环境
   - 确保已安装 Java 8 或更高版本
   - 推荐使用 OpenJDK 11 或 8
   - 可通过以下方式安装：
     ```bash
     # 使用 Homebrew 安装 OpenJDK
     brew install openjdk@11
     # 或者从官网下载安装包：https://openjdk.org/install/
     ```

2. SSH 配置
   - 确保已启用 SSH 服务
   - 配置 SSH 免密登录（本地）
   - 运行 `install_hadoop.sh` 会自动配置

## 快速开始

如果您想快速开始，请按以下步骤操作：

1. **运行环境检查脚本**
   ```bash
   ./install_hadoop.sh
   ```

2. **手动安装 Java 和 Homebrew**（如果脚本检测到未安装）
   - Java: 访问 https://openjdk.org/install/ 下载安装
   - Homebrew: 访问 https://brew.sh/ 获取安装命令

3. **安装 Hadoop**
   ```bash
   brew install hadoop
   ```

4. **配置环境变量**（见下方详细配置）

5. **启动 Hadoop**
   ```bash
   ./start_hadoop.sh
   ```

## 详细安装步骤

### 1. 安装 Homebrew（如果未安装）
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 使用 Homebrew 安装 Hadoop
```bash
brew install hadoop
```

### 3. 配置环境变量
将以下内容添加到 `~/.zshrc` 文件（如果使用 bash，则添加到 `~/.bash_profile`）：

```bash
# Hadoop 环境变量
export HADOOP_HOME=/usr/local/Cellar/hadoop/[版本号]
export HADOOP_CONF_DIR=$HADOOP_HOME/libexec/etc/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
```

### 4. 配置 SSH 免密登录
### 6. 配置 SSH 免密登录
```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

## 配置说明

本项目已经提供了预配置的文件，位于 `hadoop_config/` 目录：

- `core-site.xml` - 核心配置
- `hdfs-site.xml` - HDFS 配置  
- `mapred-site.xml` - MapReduce 配置
- `yarn-site.xml` - YARN 配置
- `hadoop-env.sh` - 环境变量配置

这些文件会在步骤 5 中复制到 Hadoop 配置目录。

## 启动和停止

### 启动 Hadoop
使用提供的脚本：
```bash
./start_hadoop.sh
```

或手动启动：
```bash
# 首次运行需要格式化 NameNode
hdfs namenode -format

# 启动 HDFS
start-dfs.sh

# 启动 YARN
start-yarn.sh
```

### 停止 Hadoop
```bash
./stop_hadoop.sh
```

或手动停止：
```bash
stop-yarn.sh
stop-dfs.sh
```

3. 验证进程
```bash
jps
```
应该看到以下进程：
- NameNode
- DataNode
- SecondaryNameNode
- ResourceManager
- NodeManager

4. 访问 Web 界面
- HDFS 管理界面：http://localhost:9870
- YARN 资源管理器：http://localhost:8088

## 常见问题

1. 如果出现 "Permission denied" 错误
```bash
sudo chown -R $USER:staff /usr/local/hadoop
```

2. 如果端口被占用
```bash
# 查看占用端口的进程
lsof -i:9000
# 终止进程
kill -9 [PID]
```

3. 如果无法启动 HDFS
- 检查日志文件
- 确保已正确设置环境变量
- 验证配置文件的格式

## 下一步

安装完成后，你可以：
1. 运行示例程序
2. 学习 HDFS 命令
3. 开发 MapReduce 程序

## 参考资源
- [Apache Hadoop 官方文档](https://hadoop.apache.org/docs/current/)
- [Hadoop 命令参考](https://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/CommandsManual.html)
