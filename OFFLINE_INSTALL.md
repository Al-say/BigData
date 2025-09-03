# Hadoop 离线安装指南

由于网络连接问题，以下是离线或替代安装方法：

## 方法1：手动下载安装

### 1. 安装 Java
- 访问 Oracle 官网：https://www.oracle.com/java/technologies/downloads/
- 或 OpenJDK：https://openjdk.org/install/
- 下载 macOS 版本的 JDK 11 或 8
- 双击 `.dmg` 文件安装

### 2. 手动下载 Homebrew 安装脚本
如果网络问题持续，可以：
- 使用移动热点或其他网络
- 或者从朋友处获取 Homebrew 安装脚本
- 或者直接下载预编译的软件包

### 3. 手动下载 Hadoop
- 访问：https://hadoop.apache.org/releases.html
- 下载最新稳定版（如 hadoop-3.3.6.tar.gz）
- 解压到 `/opt/homebrew/` 或 `/usr/local/` 目录

## 方法2：使用移动热点

如果有移动数据，可以：
1. 开启手机热点
2. 连接热点网络
3. 重新运行安装命令

## 方法3：检查网络配置

```bash
# 检查 DNS 设置
cat /etc/resolv.conf

# 尝试使用不同的 DNS
sudo networksetup -setdnsservers Wi-Fi 8.8.8.8 8.8.4.4

# 测试连接
ping google.com
```

## 当前状态

基于检查结果：
- ✅ SSH 配置已完成
- ✅ 数据目录已创建
- ✅ 配置文件已准备
- ❌ Java 需要安装
- ❌ Homebrew 需要安装  
- ❌ Hadoop 需要安装

## 下一步

1. 解决网络连接问题
2. 安装 Java
3. 安装 Homebrew
4. 通过 Homebrew 安装 Hadoop
5. 运行 `./verify_hadoop.sh` 验证安装
