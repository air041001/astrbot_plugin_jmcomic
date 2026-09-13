# astrbot_plugin_jmcomic

一个给 AstrBot 使用的 JMComic PDF 下载插件。

插件注册了 `/jm` 命令。输入漫画 ID 后，它会下载对应画册的图片，使用 Pillow 合成为 PDF，上传到 `tmpfiles.org`，最后返回一个下载地址。生成过程中使用的临时目录会在发送完成后删除。

## 安装

在 AstrBot 的插件目录执行：

```bash
cd data/plugins/
git clone https://github.com/air041001/astrbot_plugin_jmcomic.git
```

安装依赖：

```bash
pip install -r astrbot_plugin_jmcomic/requirements.txt
```

然后在 AstrBot 中重载插件，或重启 AstrBot。

依赖包括：

- `jmcomic`
- `Pillow`
- `requests`

## 配置白名单

白名单写在 `main.py` 的 `WHITELIST` 变量中。把示例值替换成允许使用命令的 QQ 号，例如：

```python
WHITELIST = ["123456789", "987654321"]
```

不在白名单中的消息不会得到回复。当前代码使用字符串包含匹配来判断发送者 ID，因此填写时应确认它与 AstrBot 实际提供的 `sender_id` 格式相符。

## 使用

在 AstrBot 能接收命令的会话中发送：

```text
/jm 1127428
```

ID 必须是纯数字。插件会依次完成下载、图片转换和 PDF 生成；处理成功后会返回下载地址。

由于代码会把返回地址中的英文句号替换成中文句号，复制地址后需要把 `。` 改回 `.` 才能打开。

## 文件和临时目录

默认临时目录是：

```text
/AstrBot/data/jm_tmp/<漫画ID>/
```

插件会在启动时创建这个目录。正常完成上传后，对应的漫画目录会被删除；如果中途异常退出，临时目录可能需要手动清理。PDF 的文件名为 `<漫画ID>.pdf`。如果部署环境没有这个路径，需要在 `main.py` 中调整 `base_mount_dir`。

## 常见情况

- 没有任何回复：先检查发送者是否在 `WHITELIST` 中。
- 提示 ID 必须是纯数字：命令参数中不要带前缀、空格或其他字符。
- 云端中转失败：检查 AstrBot 运行环境能否访问 `tmpfiles.org`。
- 下载后没有 PDF：查看 AstrBot 日志，确认图片下载和 Pillow 转换过程是否报错。

## 说明

这个插件依赖 [JMComic-Crawler-Python](https://github.com/hect0x7/JMComic-Crawler-Python) 完成画册下载。插件本身只负责命令处理、图片转 PDF 和临时文件上传，不提供漫画内容。

请遵守所在地区的法律法规、网站条款和版权要求，只处理你有权访问或保存的内容。
