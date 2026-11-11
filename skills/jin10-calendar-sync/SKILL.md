---
name: jin10-calendar-sync
description: 从金十财经日历（rili.jin10.com）抓取指定日期范围的宏观数据，每天摘选最重要的 3 条，**直接在对话里用英文表格列出（不写飞书文档）**，用户确认后同步到 Bitrue 后台（newsd.bitapple.com RWA 事件日历）。数据抓取走免登录的公开 JSON 接口，无需登录、无需 cookie、无需浏览器。当用户要求同步/抓取财经日历、更新 RWA event calendar、或提到金十日历→Bitrue 流程时使用。
---

# 金十日历 →（对话中列出）→ Bitrue 后台 同步流程

按顺序执行以下阶段，不要跳步。全程用中文与用户沟通，但**抓取到的数据内容保持英文**（如 Title、Remark）。

> **抓取改为免登录直连**：金十日历是 Nuxt 单页应用，日页面数据来自公开 CDN JSON 接口，网页上的「请登录后查看」只是前端遮罩。带上页面自带请求头即可直接取数，**不需要登录、不需要 cookie、不需要浏览器**。
> **输出载体：对话**。本期**不再写飞书表格**；每天的 Top3 直接在对话里用英文表格列出，用户确认后再推送到 Bitrue 后台。

## 启动前：一次问清参数

1. **抓取的日期范围**（如：11.11 到 11.18，含两端）。
2. **最新的 Bitrue cookie**：提示用户用 **Chrome 的 Cookie-Editor 扩展**获取——打开 `https://newsd.bitapple.com` 登录后，点 Cookie-Editor → **Copy** → 选 **Header string**，把整段 Cookie 粘到对话里给 agent（至少含 `XSRF-TOKEN` 和 `laravel_session`）。cookie 会过期，若推送报 419/401 就重新要一次。
3. **提醒用户挂上公司 VPN**（`newsd.bitapple.com` 需要公司网络才能访问）。连接测试：`curl -sS --noproxy '*' --max-time 8 -o /dev/null -w '%{http_code}' https://newsd.bitapple.com/`，返回 HTTP 状态码即通过。

## 阶段 1：免登录抓取金十日历数据（API）

**接口主机**：`https://e0430d16720e4211b5e072c26205c890.z3c.jin10.com`

**请求头（三个接口都要，缺了会返回 502）**：
- `x-app-id: rU6QIu7JHe2gOUeR`
- `x-version: 1.0.0`
- `Referer: https://rili.jin10.com/`
- `User-Agent: Mozilla/5.0`

**接口（`category=cj` 必带）**：
- `GET /get/data?date=YYYY-MM-DD&category=cj` → 宏观数据
- `GET /get/event?date=YYYY-MM-DD&category=cj` → 财经事件（央行决议 / 讲话 / 会议等）
- `GET /get/holiday?date=YYYY-MM-DD&category=cj` → 交易所休市（返回该日期起前后约两个月）

返回结构 `{"status":200,"message":"OK","data":[...]}`。宏观数据每条字段：

| 返回字段 | 含义 |
|---|---|
| `pub_time` | `YYYY-MM-DD HH:MM`，**已是北京时间**，不用转换 |
| `indicator_name` | 指标名 |
| `star` | 重要性星级（1~5） |
| `previous` | 前值 |
| `revised` | 修正值（有则以它为准作前值） |
| `consensus` | 预测值 |
| `actual` | 公布值（未来日期为空） |
| `unit` | 单位 |
| `country` | 国家/地区 |
| `data_id` / `indicator_id` | 稳定 ID |

事件每条字段：`event_time`、`event_content`、`country`、`star`、`time_status`（值为「待定」表示公布时间未定）。

**推荐直接用本 skill 自带脚本（纯标准库无依赖）**：

```bash
python3 scripts/jin10_fetch.py --start YYYY-MM-DD --end YYYY-MM-DD --top3 --include-events
```

- 脚本位于本 skill 目录 `scripts/jin10_fetch.py`（相对 `resourceBase`）；如不确定当前目录，用该 skill 目录的绝对路径调用。
- `--top3`：每日按「星级 → 关键词 → 有无预测值」给出候选 3 条（仅供挑选参考，最终人工定稿）。
- `--json-out <file>`：另存 JSON 便于后续处理。
- 不加 `--top3` 时输出当日全部宏观数据。

等价的手写方式（自检/调试用）：

```bash
curl -s --noproxy '*' \
 "https://e0430d16720e4211b5e072c26205c890.z3c.jin10.com/get/data?date=2026-11-11&category=cj" \
 -H 'x-app-id: rU6QIu7JHe2gOUeR' -H 'x-version: 1.0.0' \
 -H 'Referer: https://rili.jin10.com/' -H 'User-Agent: Mozilla/5.0'
```

**要点与坑**：
- 返回的 `pub_time` 就是北京时间，字段已解析好，比旧的 DOM 抓 `.jin-table-row` 稳定得多。
- 未来日期只有预测值（`actual` 为空）；历史日期有公布值。
- **周日可能全天空**（宏观数据和事件都返回空）——该日 0 条，如实告知用户，不要编造。
- `x-app-id` 可能轮换。若接口开始返回 **502**，去 `rili.jin10.com` 的浏览器 XHR 里抄一份新的换上（当前有效：`rU6QIu7JHe2gOUeR` / `1.0.0`）。
- 若走本地代理遇到 TLS 重置，让 python/curl 不走代理（`--noproxy '*'`，或 python 用 `urllib.request.ProxyHandler({})`）。
- 侧边栏的「本周焦点」周历与日页面数据可能不一致，一律以 **/get/data 当天返回**为准。

## 阶段 2：挑选 Top3 并整理字段

- 重要性星级直接用接口的 `star`；**按宏观重要度人工挑选 Top3**：CPI / GDP / PPI / 非农就业 / 失业率 / 零售 / 利率决议 > PMI / ZEW / 库存 / 钻井数等；同分优先有预测值的。
- 时间就是接口返回的北京时间；`待定` 时间的数据尽量不要选。
- 名称里去掉后缀「 数据回顾」「 视频解析」「 查看数据库 XXX」。
- 每个日期共 3 条（不足 3 条如实说明）。整理成下面需要的行。

数据行格式（用户确认过）：

- **Name**：`YYYYMMDD-N`，N 是当日重要性序号（1 = 最重要），如 `20261111-1`。
- **Title**：英文，如 `Germany October CPI YoY (Final)`；控制在 53 字符内（前端展示上限，规则见阶段 4），超长按缩写手段处理。
- **Remark**：全部英文。未发生：`Previous:2.80% Forecast:2.8%`；已发生：`Previous:X Actual:Y`；缺失值写 `--`。
- **Date**：`YYYYMMDD HH:MM`，如 `20261111 15:00`。
- 表头：`Name | Title | Remark | Date`。

## 阶段 3：在对话中列出 Top3 并等确认

- 在回复里输出 Markdown 表格（`Name / Title / Remark / Date`），按日期分组列出；英文内容。
- 说明每日选取理由（星级、是否有预测值）。
- **等用户确认后**再进入阶段 4 推送（不再写飞书表格）。

## 阶段 4：推送到 Bitrue 后台

**推送前再次确认用户已挂公司 VPN。**

关键经验（本机实测）：
- 本地代理（127.0.0.1:7897）会对 newsd.bitapple.com 的 TLS 握手重置，**所有 curl 必须加 `--noproxy '*'` 直连**，靠 VPN 出去。
- 接口（Laravel）：
  - 列表（只读）：`POST https://newsd.bitapple.com/api/v1/rwa/calendar/list`，body `{"page":1,"page_size":100}`
  - 创建/编辑：`POST https://newsd.bitapple.com/api/v1/rwa/calendar/edit`，**body 不带 `id` = 新建，带 `id` = 编辑**
  - GET 会 405；不存在的路径 404 `{"message":""}`
- **name 规则（用户已确认）**：`YYYYMMDD-N` + 空格 + 英文标题，如 `20261118-3 US Oct Building Permits (Annualized)`。后端校验 name 最大 50 字符；超长按缩写手段处理。
- **title 长度规则（用户已确认）**：前端最多能完整展示约 53 字符，title 超过 53 字符必须缩短后再 edit：去掉括号里的单位/条数说明（如 `(10k barrels)`、`, 10k units`）、Seasonally-Adjusted→SA 等。
- 缩写手段（name/title 通用）：月份 October→Oct / September→Sep、Seasonally-Adjusted→SA、Annualized→Ann.、(Week of Nov 13)→(w/e Nov 13)、去掉括号里的单位说明；优先丢单位/序号说明，不丢指标本身（如 MoM/YoY/Preliminary）。
- 创建 payload 模板（title/remark 是 `{"en_US": "..."}` 对象）：

```json
{"name":"20261111-1 Germany October CPI YoY (Final)","title":{"en_US":"Germany October CPI YoY (Final)"},"remark":{"en_US":"Previous:2.80% Forecast:2.8%"},"image_url":"","event_time":"2026-11-11 15:00:00","time_pending":0,"online_status":1}
```

  注意 `event_time` 格式是 `YYYY-MM-DD HH:MM:00`（表格 Date 是 `YYYYMMDD HH:MM`，要转换）。
- **编辑已有记录**：payload 带上 `id`，并把列表返回的 `ctime`、`mtime` 原样回传，其余字段也原样带回，只改要改的字段。批量改名前先 `POST list` 拉全量，用 python 从返回拼 payload 最稳。

安全规则：
- cookie 是敏感信息，不要在回复里原样展示，直接写进命令即可。
- Cookie **只在本次对话里使用**：直接从 Cookie 字符串里取 `XSRF-TOKEN`（URL 解码后）放进 `x-xsrf-token` 头，把整段 Cookie 用 `-b "$COOKIE"` 带上；不要写入文件、不要用 cookie jar、不要交给其他工具。
- 响应成功标志：HTTP 200 且 body `code == 200`。

**先只发一条**，回读列表给用户确认（name 格式、字段映射），用户确认后再批量发剩余的（每条间隔 0.6s，失败重试一次）：

```bash
# COOKIE 就是用户粘到对话里的整段 Cookie（login-status=...; XSRF-TOKEN=...; laravel_session=...）
xsrf=$(printf '%s' "$COOKIE" | python3 -c "import sys,urllib.parse,re;s=sys.stdin.read();m=re.search(r'XSRF-TOKEN=([^;]+)',s);print(urllib.parse.unquote(m.group(1)) if m else '')")
curl -s --noproxy '*' -X POST 'https://newsd.bitapple.com/api/v1/rwa/calendar/edit' \
  -H 'accept: application/json, text/plain, */*' -H 'content-type: application/json' \
  -b "$COOKIE" \
  -H 'origin: https://newsd.bitapple.com' \
  -H 'referer: https://newsd.bitapple.com/assets-transactions/contract-manange/rwa-management/rwa-event-calendar' \
  -H 'user-agent: Mozilla/5.0 (Linux; Android 16; Pixel 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Mobile Safari/537.36' \
  -H 'x-new-client: 2' -H "x-xsrf-token: $xsrf" \
  --data-raw "$payload"
```

推送完成后：`POST list` 拉全量，核对条数（本次目标数）和每条字段，输出核对表给用户。

## 收尾提醒

- 金十抓取全程免登录，不需要保留任何浏览器标签页。
- 后台若有用户的 test 脏数据，提醒用户可手动删除（删除接口未验证过，不要乱试写接口）。

## 目录约定
本 skill 随 DSH 插件 `@local/rwa-skills` 打包，位于插件包内 `skills/jin10-calendar-sync/`；抓取脚本在 `scripts/jin10_fetch.py`（相对 `resourceBase`）。
