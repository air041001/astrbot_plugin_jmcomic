# 🚀 AstrBot JMComic PDF 下传插件

本插件为 [AstrBot](https://github.com/Soulter/AstrBot) V4 框架设计，旨在实现 JMComic 漫画的自动化爬取、PDF 无缝缝合及云端直发。

针对 Linux 环境（尤其是 Docker/Snap 沙盒）中 QQ/微信 客户端无法读取非标准路径文件、权限受限等痛点，本插件采用“本地合成 + 云端中转”的降维打击方案，通过返回临时直链，彻底规避 OneBot 平台常见的 `retcode=1200`（路径不存在/无法访问）报错，确保 100% 的发送成功率。

## ✨ 核心特性

* **☁️ 云端数据流传输**：通过 `tmpfiles.org` 接口将生成的 PDF 转化为完全匿名的临时直链。直接发送 URL 给客户端，无视一切本地阻挡。
* **🧹 磁盘零占用**：采用“战前清场”与“阅后即焚”逻辑。任务开始前自动清理旧数据，任务结束后彻底销毁本地存根，绝不占用宝贵的 VPS/本地 硬盘空间。
* **🛡️ 严格访问控制**：内置 `WHITELIST` 机制，支持针对特定 QQ UID 开启权限。非白名单用户触发指令时机器人直接“装死”无视，从源头降低风控和被举报风险。

## 📦 安装指南

1. **安装环境依赖**
   确保你的运行环境已安装以下 Python 库：
   ```bash
   pip install jmcomic Pillow requests
   ```

2. **部署插件**
   进入 AstrBot 插件目录（通常为 `data/plugins/`），克隆本仓库：
   ```bash
   cd data/plugins/
   git clone [https://github.com/air041001/astrbot_plugin_jmcomic.git](https://github.com/air041001/astrbot_plugin_jmcomic.git)
   ```

3. **配置权限（⚠️必看）**
   用文本编辑器打开 `main.py`，找到 `WHITELIST` 列表，加入允许使用该指令的 QQ 号：
   ```python
   # main.py
   WHITELIST = ["XXXXXXXXX"] # 替换或添加你自己的 QQ 号
   ```
   *注：如果不配置白名单，连部署者本人也无法触发指令。*

4. **重启生效**
   进入 AstrBot 的 WebUI 仪表盘，点击 **【重载】** 插件，或直接重启机器人进程。

## 🎮 使用方法

在私聊或允许的群聊中发送：

```text
/jm [车牌号]
```
*示例：`/jm 1127428`*

机器人将依次反馈进度，并在处理完成后下发专属的高速下载直链。

## 🤝 致谢

* 本插件核心下载逻辑基于强大的 [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) 驱动。向原作者在爬虫领域的硬核贡献表示敬意。

## ⚠️ 免责声明

* 本项目仅供 Python 编程学习及网络协议研究使用，请勿用于任何商业用途或大范围公开传播。
* 请勿利用本插件爬取或传播任何非法内容。
* 使用本插件产生的任何版权纠纷、网络风控或账号安全风险，均由使用者自行承担。
```
作者的话：
	本项目ai含量高达99%，仅是我一时好奇才想出来的东西，介意ai者慎用。






