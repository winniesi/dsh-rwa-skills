---
name: rwa-daily-news
description: >-
  Bitrue「RWA & TradFi」每日资讯「采集 + 上架 Bitrue 后台」的流水线。先采集与 20 个 RWA 代币化美股币对相关的最新资讯，**直接在对话里用英文 7 列表格列出（不写飞书文档）**，再从确认后的表格组装 payload 发布到 Bitrue 后台（RWA 资讯管理，https://newsd.bitapple.com），最后回查校验。
  当用户提到「RWA 资讯」「每日资讯」「采集新闻」「资讯上架」「更新后台」「Bitrue 后台」等时使用。
  执行前必须先向用户强调两件事：①拿到【最新的登录 cookie】；②连接【公司 VPN】。
---

# Bitrue RWA 每日资讯：采集 →（对话中列出）→ 上架 Bitrue 后台

本 skill 合并两条链路：
- **Phase 1（获取内容）**：按规则采集最新资讯，**直接在对话里输出一张英文 7 列表格**（详见 `references/collect.md`）。**不再写入飞书表格。**
- **Phase 2（上架 Bitrue 后台）**：以对话里已确认的英文表为输入 → 组 payload → POST 到 Bitrue 后台 `news/edit` → 回查校验（详见 `references/publish-api.md`）。

> 命名/结构约定（用户口径）：每次运行产出**一张英文表**，7 列 `Title/Description/Link/Pair/Source/Date/Pair URL`，只保留英文。

## 0. 前置提醒（每次执行前必须向用户强调）

1. **必须使用【最新的登录 cookie】**：Bitrue 后台登录态会过期，旧的会被 401/419 或跳登录。每次执行前提示用户用 **Chrome 的 Cookie-Editor 扩展**重新获取：
   - 打开后台页面并登录（referer 页：`https://newsd.bitapple.com/assets-transactions/contract-manange/rwa-management/rwa-information-management`）；
   - 点 Cookie-Editor 扩展 → **Copy** → 选 **Header string**；或 Export → Header String；
   - 把整段 Cookie 粘到对话里给 agent（至少包含 `login-status`、`XSRF-TOKEN`、`laravel_session`）；
   - `X-XSRF-TOKEN` 请求头 = Cookie 里的 `XSRF-TOKEN` 值（Laravel 双提交校验）。
   - **cookie 是敏感且会过期的凭证：不要写死进本 skill 文件，也不要在回复里明文回显。** Cookie **只在本次对话里使用**：直接把 Cookie 字符串拼进 curl（`-b "名字=值; ..."`），**不要写入文件、不要用 cookie jar、不要交给其他工具**。
2. **必须连接【公司 VPN】**：`newsd.bitapple.com` 与部分资讯源（ChainCatcher / TechFlow / PANews / Odaily 等）需要公司网络 / VPN 才能稳定访问。
   - 连接测试：`curl -sS --noproxy '*' --max-time 8 -o /dev/null -w '%{http_code}' https://newsd.bitapple.com/`；能返回 HTTP 状态码即表示已连内网，否则提示用户检查 VPN。
3. **代理坑**：若本机开了全局代理（如 `127.0.0.1:7897`），curl 访问 `newsd.bitapple.com` 会 TLS 握手失败。用 curl 时加 `--noproxy '*'` 走直连（在 VPN 生效的前提下）。
4. **写操作需确认**：上架属于线上写操作。默认先投 1 条让用户在后台核对，确认后再批量；或先跟用户确认本次要投几条。
5. **输出载体：对话**。本期**不再写飞书表格**；采集结果直接在对话里用英文 7 列表格列出，用户确认后再上架后台。

## 1. 关键对象速查

| 项 | 值 |
|---|---|
| 输出载体 | **对话内的英文 7 列表格**（不写飞书；如需可临时存 `/tmp/en_rows.csv`） |
| Bitrue 后台基址 | `https://newsd.bitapple.com` |
| 新建/编辑资讯 | `POST /api/v1/rwa/news/edit`（不带 `id`=新建；带 `id`=编辑） |
| 资讯列表 | `POST /api/v1/rwa/news/list`，body `{"page":1,"page_size":50}` |
| 资讯详情 | `GET /api/v1/rwa/news/detail?id=<id>`（列表返回的 `content_pc/h5` 为 null，正文只在详情里） |
| 固定分类 | `topic_ids:[1]`（topic id 1 = "AI"，现有全部记录都用它） |
| 配图（三选一） | 资产解析/交易行情/数据洞察=`1794215718818.png`；新闻快讯/机构动态=`1794215755704.png`；人物观点=`1794215770406.png`（前缀 `https://static.bitrue.com/futures_trade_race/`） |

## 2. Phase 1 — 获取内容并在对话中列出

完整规则见 **`references/collect.md`**（含 20 个币对清单、来源优先级、时间核验、7 列表头、查重）。要点：
- 用 Bitrue `POST /api/v1/rwa/news/list` 拉取后台现有记录做查重（不重复同一篇文章链接/同一标题）；
- 选 10 条近 24h（不足放宽 72h）**事件性**资讯，尽量覆盖不同币对；
- 逐篇打开原文核实标题 / 核心事实 / 精确发布时间，**不要**只信搜索摘要的相对时间；
- **只写英文一张表**（7 列），标题/描述用英文；
- **标题用一句英文简短概括**（不要太长，建议 ≤90 字符），具体细节放 Description；
- **来源尽量多样化，不要只用一个资讯源**（10 条尽量覆盖 ≥3 个来源）；
- 输出方式：**在对话里输出 Markdown 表格（含表头 A1 起 7 列）**，等用户确认。

> 若用户已有确认好的表格内容、只想上架，可直接跳到 Phase 2。

## 3. Phase 2 — 上架到 Bitrue 后台

完整接口/字段/示例见 **`references/publish-api.md`**。执行步骤：

1. 以**对话里已确认的英文 7 列表**为输入（必要时把内容落到临时 CSV/JSON 便于脚本处理）。
2. 逐行组 payload（见下「字段口径」），写入临时 JSON 文件（用 Python 生成，避免转义问题）。
3. 用 curl（带最新 cookie、`--noproxy '*'`）逐条 `POST /api/v1/rwa/news/edit`。
4. 回查：`POST /list` 看总数是否 +N、状态是否上线；对新增 id 用 `GET /detail?id=` 抽查 `title.en_US`、`content_pc/h5`、`source`、`show_time`、`icon`、`topics`。

### 字段口径（务必遵守）
- `name`：**≤50 字符**（超了接口报 `name 的最大长度为 50 字符`）。约定用「日期MMDD + 英文短标题」。
- `title`：`{"en_US": 英文标题}`（**英文标题用一句简短概括，不要太长，建议 ≤90 字符**；细节写进 Description；后端会自动生成多语言，无需手填其它语种）。
- `content_pc` 与 `content_h5`：内容完全相同，HTML 模板：
  ```html
  <p><span style="color: rgb(255, 255, 255); font-size: 13px;">{描述}</span></p>
  <p><a href="{币对地址}" target="_blank"><span style="color: rgb(255, 255, 255); font-size: 13px;">{XXX/USDT}</span></a></p>
  ```
  （`{XXX/USDT}` 由 Pair `XXX-USDT` 把 `-` 换成 `/`；币对地址取表格「Pair URL」列。）
- `topic_ids`：`[1]`。
- `icon`：按新闻类型三选一（见速查表）；拿不准时：数据/行情/财报类→资产解析，快讯/公司机构动作→新闻快讯，人物表态/观点→人物观点。
- `source`：取表格「来源/Source」列（如 ChainCatcher / TechFlow）。
- `show_time`：`YYYY-MM-DD HH:MM:SS`（由表格 Date `M/D/YYYY HH:MM:SS` 转成补零格式）。
- `online_status`：`1`。

## 4. 选条规则（用户口径，Phase 2 若需从候选中挑选时使用）
- **排除竞品**：Coinbase / COIN-USDT 等竞品交易所相关的不写。
- **尽量往币对上靠**：优先「新闻主体 = 该币对标的、且有明确事件催化（合作/发布/人事/监管/财报/大额链上）」，少用纯行情播报/价格预测。
- 选「最合适」的若干条时**尽量覆盖不同币对**（同一币对最多取 2 条不同事件）。
- **来源多样化**：不要只用单一资讯源；10 条尽量覆盖 ≥3 个不同来源，避免全部来自同一站。
- **标题简短**：Title 用一句英文概括（建议 ≤90 字符），不要堆砌细节。
- 每次投递后用表格映射清楚：哪条 → 哪个币对 → 哪个配图 → 哪条 id，方便用户核对与替换。

## 5. 验收清单（每次结束前）
- [ ] 对话中的英文 7 列表格已由用户确认；
- [ ] 接口逐条 `{"code":200,"msg":"成功"}`；
- [ ] `POST /list` 总数按预期增加，`online_status=1`；
- [ ] `GET /detail?id=` 抽查：`title.en_US` 与表一致、`content_pc==content_h5` 且含描述+币对链接、`source`/`show_time`/`icon`/`topics` 正确；
- [ ] 报告里列出 id、币对、配图、来源、发布时间，并说明排除/未选原因。

## 参考文件与本地资源
- `references/collect.md` — Phase 1 采集规则与 7 列格式（输出到对话）。
- `references/publish-api.md` — Phase 2 Bitrue 后台接口、payload、curl 示例与核验。
- `assets/` — 三类配图的本地副本（`新闻快讯、机构动态.png`、`资产解析、交易行情、数据洞察.png`、`人物观点.png`），仅作参考；正式 payload 用第 1 节速查表里的远端 URL。
- `examples/` — 一次真实采集的示例：`build_rows.py`（生成 CSV 的脚本）、`en_rows.csv`（英文 7 列成品样板）。

## 目录约定
本 skill 随 DSH 插件 `@local/rwa-skills` 打包，位于插件包内 `skills/rwa-daily-news/`；`resourceBase` 指向该目录，正文中的相对路径（`references/`、`assets/`、`examples/`）据此解析。
