# Phase 2 — 上架到 Bitrue 后台（RWA 资讯管理后台）

> Bitrue 后台 = `https://newsd.bitapple.com`（RWA 资讯管理页 `.../rwa-management/rwa-information-management` 对应的后端）。

## 前置（必须）
- **最新登录 cookie**：每次用 **Chrome 的 Cookie-Editor 扩展**重新获取（后台页 → Cookie-Editor → Copy → Header string），粘到对话给 agent。至少含 `login-status`、`XSRF-TOKEN`、`laravel_session`。
  - `X-XSRF-TOKEN` 请求头 = Cookie 里的 `XSRF-TOKEN` 值（Laravel 双提交）。
  - 敏感且会过期：不要写死，不要明文回显。Cookie **只在本次对话里使用**，直接拼进 curl 的 `-b "名字=值; ..."`，不要写入文件、不要用 cookie jar。
- **公司 VPN 已连接**：`newsd.bitapple.com` 需公司网络 / VPN 才能稳定访问。
  - 连接测试：`curl -sS --noproxy '*' --max-time 8 -o /dev/null -w '%{http_code}' https://newsd.bitapple.com/`，返回 HTTP 状态码即通过。
- 若本机有全局代理（`127.0.0.1:7897` 等），curl 会 TLS 失败；加 `--noproxy '*'` 直连。

## 接口一览
| 用途 | 方法 | 路径 | 说明 |
|---|---|---|---|
| 新建 / 编辑资讯 | POST | `/api/v1/rwa/news/edit` | **不带 `id` = 新建记录；带 `id` = 编辑该记录** |
| 列表 | POST | `/api/v1/rwa/news/list` | body `{"page":1,"page_size":50}` → `data.list[]` / `data.total` |
| 详情 | GET | `/api/v1/rwa/news/detail?id=<id>` | 返回 `content_pc/content_h5`（列表里这两个字段为 null） |

## 请求头（新建示例）
```
accept: application/json, text/plain, */*
content-type: application/json
x-new-client: 2
x-xsrf-token: <XSRF-TOKEN 的值>
origin: https://newsd.bitapple.com
referer: https://newsd.bitapple.com/assets-transactions/contract-manange/rwa-management/rwa-information-management
```

## payload 字段（JSON）
| 字段 | 说明 |
|---|---|
| `name` | 内部标签，**≤50 字符**（超长报 `name 的最大长度为 50 字符`）。建议「日期MMDD + 英文短标题」。 |
| `title` | `{"en_US": "<英文标题>"}`，**标题用一句简短概括、不要太长（建议 ≤90 字符）**，细节放正文；后端自动生成多语言 |
| `content_pc` | 正文 HTML（PC） |
| `content_h5` | 正文 HTML（H5），与 `content_pc` **完全相同** |
| `topic_ids` | `[1]`（固定；topic id 1 = "AI"，现有记录全部用它） |
| `icon` | 配图 URL，三选一（见下） |
| `source` | 来源名，取表格「来源/Source」列（如 `ChainCatcher` / `TechFlow`）；也可留空 |
| `show_time` | `YYYY-MM-DD HH:MM:SS` |
| `online_status` | `1`（上线）；`0`（下架） |

### 正文 HTML 模板
```html
<p><span style="color: rgb(255, 255, 255); font-size: 13px;">{描述}</span></p><p><a href="{币对地址}" target="_blank"><span style="color: rgb(255, 255, 255); font-size: 13px;">{XXX/USDT}</span></a></p>
```
- `{描述}`：表格 Description。
- `{XXX/USDT}`：由 Pair（`XXX-USDT`）把 `-` 换成 `/`。
- `{币对地址}`：表格「Pair URL」列。

### 配图三选一（前缀 `https://static.bitrue.com/futures_trade_race/`）
| 分类 | 文件名 |
|---|---|
| 资产解析、交易行情、数据洞察 | `1794215718818.png` |
| 新闻快讯、机构动态 | `1794215755704.png` |
| 人物观点 | `1794215770406.png` |

## 完整 curl 示例（新建一条）
```bash
COOKIE='login-status=1; XSRF-TOKEN=<...>; laravel_session=<...>'
XSRF='<与 Cookie 中 XSRF-TOKEN 相同的值>'

curl -sS --noproxy '*' --max-time 40 \
  -b "$COOKIE" \
  -H 'accept: application/json, text/plain, */*' -H 'accept-language: zh-CN,zh;q=0.9' \
  -H 'content-type: application/json' -H 'cache-control: no-cache' \
  -H 'x-new-client: 2' -H "x-xsrf-token: $XSRF" \
  -H 'origin: https://newsd.bitapple.com' \
  -H 'referer: https://newsd.bitapple.com/assets-transactions/contract-manange/rwa-management/rwa-information-management' \
  --data-binary @payload.json \
  "https://newsd.bitapple.com/api/v1/rwa/news/edit"
```

成功返回：`{"code":200,"msg":"成功","data":[]}`。

## 组装 payload 的建议流程（Python，避免转义）
1. 使用**对话里已确认的英文 7 列表**作为输入；如需脚本处理，先落到临时文件（如 `/tmp/en_rows.csv` 或 `/tmp/rows.json`）。
2. 对每行：`datetime.strptime(Date, "%m/%d/%Y %H:%M:%S")` → `name=MMDD+短标题`(≤50)、`show_time=YYYY-MM-DD HH:MM:SS`；按模板拼 `content_pc/h5`。
3. 逐条写入 `payload_*.json` 后用上面的 curl 投递；串行投递，避免并发冲突。

## 校验
```bash
# 列表：看总数是否 +N、各条 online_status
curl -sS --noproxy '*' -b "$COOKIE" -H 'content-type: application/json' -H 'x-new-client: 2' \
  -H "x-xsrf-token: $XSRF" -H 'origin: https://newsd.bitapple.com' \
  --data-raw '{"page":1,"page_size":50}' \
  "https://newsd.bitapple.com/api/v1/rwa/news/list"

# 详情：核对 title.en_US / content_pc==content_h5 / source / show_time / icon / topics
curl -sS --noproxy '*' -b "$COOKIE" -H 'x-new-client: 2' \
  "https://newsd.bitapple.com/api/v1/rwa/news/detail?id=<id>"
```
逐条断言：`title.en_US` 与表一致、`content_pc==content_h5` 且包含描述与币对链接、`source/show_time/icon/topics` 正确、`online_status=1`。

## 选条口径（从候选中挑「最合适」时）
- 排除竞品（Coinbase / COIN 等）。
- 尽量往币对上靠：新闻主体 = 该币对标的、且有明确事件催化；少用纯行情/预测。
- 尽量覆盖不同币对；同一币对最多 2 条不同事件。
- 每条都记录：id ↔ 币对 ↔ 配图 ↔ 来源 ↔ 时间，便于用户核对与替换。
