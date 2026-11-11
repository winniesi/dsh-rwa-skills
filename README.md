# DSH RWA Skills 插件

一个 DeepSeek Harness（DSH）插件包：把两个业务 Skill 打包成随插件分发的**全局技能**，并在左侧栏提供一个「RWA 工具箱」入口。

## 功能

- 左侧栏新增「RWA 工具箱」图标，位置夹在「插件」与「日程」之间。
- 面板里两张技能卡：
  - **RWA 每日资讯**：采集 20 个 RWA 代币化美股币对的最新英文资讯，在对话中列出英文表格，确认后上架 Bitrue 后台并回查。
  - **金十日历同步**：抓取金十财经日历，按天挑 Top3 英文数据，在对话中列出，确认后同步到 Bitrue 事件日历。
- 点卡片上的「开始」→ **新建一个对话并自动发送引导语**，无需手动再点发送。引导顺序：连接公司 VPN → 用 Cookie-Editor 复制 Cookie → 测试能否访问 `https://newsd.bitapple.com/` → 再执行对应技能。
- 两个 Skill 由 Host 端通过 `ctx.skills.register()` 注册为全局技能，换工作区 / 换机器都能用，不依赖某个 `skills/` 目录。

## 前置条件

- 公司 VPN（访问 `https://newsd.bitapple.com` 需要公司内网）。
- Chrome 的 **Cookie-Editor** 扩展（用于复制 Bitrue 后台 Cookie 的 Header string）。
- 本机 `curl`、`python3`（金十抓取脚本已随包，纯标准库）。

## 目录结构

```
.
├── package.json            # dsh.bundle.patch + dsh.client 声明
├── cordis.patch.yml        # 插入 Host 插件行
├── index.js                # Host 半：注册两个技能
├── client.js               # Client 半：左侧图标 + 面板 + 自动发送
├── locale/{zh,en}.json     # 插件在「插件」页的标题/描述
├── icon.svg
└── skills/
    ├── rwa-daily-news/     # SKILL.md + references + examples + assets
    └── jin10-calendar-sync/# SKILL.md + scripts/jin10_fetch.py
```

## 安装

在 DSH 中把本目录作为本地 bundle 安装（例如通过插件管理器的 `install_bundle`，target 指向本包目录），安装后刷新页面即可看到左侧「RWA 工具箱」入口。

## 说明与注意

- 两个技能**不再写入飞书表格**：采集结果直接在对话里以英文 7 列表格列出，用户确认后再上架 Bitrue 后台。
- **Cookie 只在本次对话中使用**：不写入文件、不使用 cookie jar、不上传到任何第三方；每次运行前用 Cookie-Editor 重新复制最新 Cookie。
- 本插件面向 Bitrue 内部后台（`newsd.bitapple.com`），请仅在你有权限的环境使用。
- `skills/rwa-daily-news/assets/` 中的图片为 Bitrue 平台素材，仅作参考，版权归原方。

## License

MIT（不含第三方素材）。
