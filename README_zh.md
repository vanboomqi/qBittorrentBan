# qBittorrent 屏蔽迅雷客户端

该脚本用于根据预定义规则自动过滤 qBittorrent 中不需要的客户端。

## 特性

- 自动登录 qBittorrent Web UI。
- 获取正在下载/上传的种子列表。
- 查询每个种子的连接客户端。
- 根据用户定义的规则过滤不需要的客户端。
- 更新 qBittorrent 的 IP 过滤器，阻止被过滤的客户端。
- 定期检查状态并执行上述步骤。

## 快速开始

### 先决条件

- Python 3.x
- 需要的 Python 包（通过 `pip install -r requirements.txt` 安装）：
  - `requests`
  - `json`
  - `time`
  - `random`
  - `math`
  - `string`
  - `configparser`
  - `os`

### 配置

1. 将 `config_sample.ini` 重命名为 `config.ini`。
2. 打开 `config.ini` 并配置以下设置：
   - **Credentials：** 设置 qBittorrent Web UI 的用户名和密码。
   - **URLs：** 设置 qBittorrent Web UI 的根 URL。
   - **Paths：** 设置 IP 过滤的文件路径。

### 过滤规则

修改 `config.ini` 中的 `[FilterRules]` 部分以定义您的自定义过滤规则。每个规则应遵循格式 `name,findType`，其中 `findType` 为 `1` 表示包含匹配，`2` 表示前缀匹配。

示例：
```ini
[FilterRules]
# 用于阻止客户端的过滤规则
# 每个规则的格式为：name,findType
# 其中 findType 为 1 表示包含匹配，2 表示前缀匹配
rule_1 = -XL0012,1
rule_2 = -XL0012-,1
rule_3 = Xunlei,1
rule_4 = Xfplay,1
rule_5 = go.torrent,1
rule_6 = QQDownload,1
rule_7 = 7.,2
# FilterRules 结束

