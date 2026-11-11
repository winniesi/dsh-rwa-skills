# Phase 1 — 采集内容并在对话中输出英文表

> 来源：Bitrue「RWA & TradFi Assets」每日资讯整理任务。每日为资讯上架收集 10 条与页面上线币对相关的最新资讯，**直接在对话里以英文 7 列表格输出，不再写飞书表格**。

## 输出载体
- **对话内 Markdown 表格**：A1 起 7 列 `Title / Description / Link / Pair / Source / Date / Pair URL`，只写英文。
- 如需脚本处理，可临时落到 `/tmp/en_rows.csv`（含表头），不写入任何飞书文档。

## 币对范围与币对地址（只能用以下 20 个；币对地址直接从下表复制，不要自行拼接）

| 相关币对 | 币对地址 |
|---|---|
| NVDA-USDT | https://www.bitrue.com/futures/NVDA |
| AMD-USDT | https://www.bitrue.com/futures/AMD |
| AVGO-USDT | https://www.bitrue.com/futures/AVGO |
| INTC-USDT | https://www.bitrue.com/futures/INTC |
| MU-USDT | https://www.bitrue.com/futures/MU |
| SKHYNIX-USDT | https://www.bitrue.com/futures/SKHYNIX |
| MSFT-USDT | https://www.bitrue.com/futures/MSFT |
| GOOGL-USDT | https://www.bitrue.com/futures/GOOGL |
| AMZN-USDT | https://www.bitrue.com/futures/AMZN |
| META-USDT | https://www.bitrue.com/futures/META |
| TSLA-USDT | https://www.bitrue.com/futures/TSLA |
| COIN-USDT | https://www.bitrue.com/futures/COIN |
| HOOD-USDT | https://www.bitrue.com/futures/HOOD |
| MSTR-USDT | https://www.bitrue.com/futures/MSTR |
| CRCL-USDT | https://www.bitrue.com/futures/CRCL |
| DELL-USDT | https://www.bitrue.com/futures/DELL |
| NBIS-USDT | https://www.bitrue.com/futures/NBIS |
| PLTR-USDT | https://www.bitrue.com/futures/PLTR |
| ORCLX-USDT | https://www.bitrue.com/futures/ORCLX |
| SPCX-USDT | https://www.bitrue.com/futures/SPCX |

> 注：上架到 Bitrue 后台时，用户口径要求**排除竞品**（如 COIN/Coinbase）。采集阶段可按需保留，但「上架」阶段要过滤。

## 第一步：查重基线（读 Bitrue 后台现有记录）
用最新 cookie 调 `POST /api/v1/rwa/news/list` 拉取后台现有记录，记录已有标题/链接，用于查重（不重复之前已上线的**同一篇文章链接/同一标题**）。

```bash
curl -sS --noproxy '*' -b "$COOKIE" -H 'content-type: application/json' -H 'x-new-client: 2' \
  -H "x-xsrf-token: $XSRF" -H 'origin: https://newsd.bitapple.com' \
  --data-raw '{"page":1,"page_size":200}' \
  "https://newsd.bitapple.com/api/v1/rwa/news/list"
```

## 第二步：搜集资讯
1. 选 10 条新资讯，优先近 24 小时；不足 10 条可放宽到 72 小时并按时间倒序补足；仍不足时如实说明，**不要**用纯行情播报、价格预测页凑数。
2. 优先**事件性新闻**：产品发布、合作、人事、监管、大额链上动作、财报、重大涨跌事件。
3. 尽量覆盖 10 个不同币对；某币对确实无新资讯时，可给同一币对选 2 条不同事件。
4. **来源多样化（不要只用单一来源）**：10 条应尽量来自 **≥3 个不同来源**，单一来源不超过约一半。可选来源：
   - 中文：ChainCatcher(chaincatcher.com)、TechFlow(techflowpost.com)、PANews(panewslab.com)、Odaily；
   - 英文：Cryptonews、CoinDesk、Cointelegraph、The Block、Decrypt、Business Wire、项目/公司官方 X 帖。
5. 逐一打开文章页核实：标题、核心事实、精确发布时间。不要只信搜索摘要里的相对时间。
6. **标题规范**：Title 用**一句英文简短概括**（建议 **≤90 字符**），突出「主体 + 事件」，具体数字/细节放 Description。

## 时间核验规则（最易错，必须严格执行）
- 日期列统一**北京时间(UTC+8)**，格式 `M/D/YYYY HH:MM:SS`，必须到秒；原文无秒补 `:00`。
- 站点已知规则：
  - **ChainCatcher**：读页面 `og:published_time` meta，该值即**北京时间**。
  - **TechFlow**：读 `article:published_time` meta，该值为 **UTC**，需 +8 换算。
  - **X 帖**：用 Snowflake ID 推算或页面显示时间。
  - **其他站点**：先确认时区再换算为北京时间。
- 防张冠李戴：确认新闻主体与币对真实对应（例：render.com 云公司 ≠ RENDER 币；智谱 GLM 大模型 ≠ Golem 的 GLM 币）。

## 表格列格式（英文单表，共 7 列）
| 列 | 表头 | 说明 |
|---|---|---|
| A | Title | 英文标题：一句简短概括（建议 ≤90 字符），细节放 Description |
| B | Description | 1-2 句英文核心事实 |
| C | Link | 文章原始链接 |
| D | Pair | `XXX-USDT`，必须在上面的币对清单内 |
| E | Source | 如 ChainCatcher / TechFlow / 官方X |
| F | Date | `M/D/YYYY HH:MM:SS` 北京时间（补零到秒） |
| G | Pair URL | 直接从上面「币对范围与币对地址」表中复制对应链接 |

## 第三步：在对话中输出并等确认
- 在回复里输出上面 7 列的 Markdown 表格（含表头）。
- 附一张映射：每条 → 币对 → 建议配图 → 来源，方便用户核对。
- **等用户确认后**再进入 Phase 2 上架。
