# -*- coding: utf-8 -*-
import csv

rows = [
 dict(
  zh_title="英伟达投资韩国 AI 初创：Point2Tech 等四家入列",
  zh_desc="英伟达在首尔 AI 初创合作论坛上宣布投资韩国 Point2Tech，并计划追加投资 Motif、Realworld、Upstage；Upstage 由此集齐亚马逊、AMD 与英伟达三家投资人。",
  en_title="NVIDIA Invests in Korean AI Startups, Including Point2Tech",
  en_desc="At its AI startup forum in Seoul, NVIDIA said it will invest in Korea's Point2Tech and plans to add Motif, Realworld and Upstage; Upstage now counts Amazon, AMD and NVIDIA as backers.",
  link="https://www.chaincatcher.com/article/2302982", pair="NVDA-USDT", src="ChainCatcher",
  date="11/9/2026 17:32:42", url="https://www.bitrue.com/futures/NVDA"),
 dict(
  zh_title="马斯克：特斯拉可能出租而非出售 Optimus",
  zh_desc="据财联社报道，马斯克表示特斯拉很可能向客户出租其人形机器人而非出售；特斯拉已在弗里蒙特工厂启动 Optimus 早期量产，预计 2027 年底左右开始向外部客户交付。",
  en_title="Musk: Tesla May Rent Out Optimus Rather Than Sell It",
  en_desc="Musk said Tesla will likely rent its humanoid robots to customers rather than sell them; early Optimus production has begun at the Fremont plant, with external deliveries expected around late 2027.",
  link="https://www.chaincatcher.com/article/2302931", pair="TSLA-USDT", src="ChainCatcher",
  date="11/9/2026 14:28:38", url="https://www.bitrue.com/futures/TSLA"),
 dict(
  zh_title="英伟达与 SK 电讯合作推进主权 AI 基础设施",
  zh_desc="英伟达、Rebellions 与 SK 电讯宣布合作，依托英伟达 NVLink Fusion 推进主权 AI 基础设施建设。",
  en_title="NVIDIA Partners with SK Telecom to Advance Sovereign AI Infrastructure",
  en_desc="NVIDIA, Rebellions and SK Telecom announced a partnership to build sovereign AI infrastructure based on NVIDIA's NVLink Fusion.",
  link="https://www.chaincatcher.com/article/2302919", pair="NVDA-USDT", src="ChainCatcher",
  date="11/9/2026 13:01:48", url="https://www.bitrue.com/futures/NVDA"),
 dict(
  zh_title="SpaceX 计划 11 月 13 日进行星舰测试发射",
  zh_desc="SpaceX 称在获监管批准前提下，计划最早于 11 月 13 日发射星舰，窗口 75 分钟，将于美中时间下午 4:45 开启；此次将首次尝试让星舰与超重型助推器双双返回发射场并回收。",
  en_title="SpaceX Plans Starship Test Launch on November 13",
  en_desc="SpaceX said it plans to launch Starship as early as Nov 13, subject to regulatory approval; the 75-minute window opens at 4:45 pm Central, and the flight will for the first time attempt to return and catch both the ship and Super Heavy booster.",
  link="https://www.chaincatcher.com/article/2302764", pair="SPCX-USDT", src="ChainCatcher",
  date="11/8/2026 18:43:37", url="https://www.bitrue.com/futures/SPCX"),
 dict(
  zh_title="Strategy 披露 47.9 亿美元储备，2026 年出售比特币筹资约 4.318 亿美元",
  zh_desc="Strategy 文件披露截至 11 月 1 日其指定美元储备为 47.9 亿美元、另有现金 1.327 亿美元；2026 年截至 10 月已通过出售比特币为股息和回购筹资约 4.318 亿美元。",
  en_title="Strategy Discloses $4.79B Reserve, Raised About $431.8M From Bitcoin Sales in 2026",
  en_desc="Strategy disclosed a $4.79 billion designated dollar reserve and $132.7 million in cash as of Nov 1; through October 2026 it raised about $431.8 million by selling bitcoin to fund dividends and buybacks.",
  link="https://www.chaincatcher.com/article/2302703", pair="MSTR-USDT", src="ChainCatcher",
  date="11/8/2026 09:32:48", url="https://www.bitrue.com/futures/MSTR"),
 dict(
  zh_title="谷歌悄悄买入高通：手机芯片巨头盯上数据中心，目标年入超 150 亿美元",
  zh_desc="Alphabet 三季度末持有高通约 297.7 万股、市值约 5.48 亿美元，二季度尚无持仓；高通正推动数据中心业务，计划 2027 财年实现 50 亿美元、到 2029 财年超 150 亿美元收入。",
  en_title="Google Quietly Bought Qualcomm Stake as Chipmaker Targets Data Centers and $15B+ Annual Revenue",
  en_desc="Alphabet held about 2.977 million Qualcomm shares worth roughly $548 million at end-Q3, a new position; Qualcomm targets $5 billion in data-center revenue by FY2027 and over $15 billion by FY2029.",
  link="https://www.chaincatcher.com/article/2302665", pair="GOOGL-USDT", src="ChainCatcher",
  date="11/7/2026 23:28:52", url="https://www.bitrue.com/futures/GOOGL"),
 dict(
  zh_title="突然跳水！AI 巨头，终止合作",
  zh_desc="11 月 7 日消息，微软在拒绝续签后正逐步关闭从甲骨文租用的人工智能算力，相关硬件搭载上一代英伟达芯片；消息致甲骨文股价盘中跳水约 3%，收盘上演深 V。",
  en_title="Sudden Plunge! AI Giant Ends Partnership",
  en_desc="Microsoft is phasing out AI compute rented from Oracle after declining to renew, as the hardware runs prior-generation NVIDIA chips; Oracle shares fell about 3% intraday before a deep V-shaped recovery.",
  link="https://www.chaincatcher.com/article/2302661", pair="MSFT-USDT", src="ChainCatcher",
  date="11/7/2026 23:03:30", url="https://www.bitrue.com/futures/MSFT"),
 dict(
  zh_title="Coinbase CEO：支持将公司股票代币化，吸纳潜在新股东是明智做法",
  zh_desc="Coinbase CEO Brian Armstrong 发文称，作为上市公司 CEO 他支持将公司股票代币化，希望更多人能持有该股票，不应将潜在新股东群体拒之门外。",
  en_title="Coinbase CEO Backs Tokenizing the Company's Stock to Reach New Shareholders",
  en_desc="Coinbase CEO Brian Armstrong said he supports tokenizing the company's stock to let more people own it, arguing it is unwise to shut out a potential new shareholder base.",
  link="https://www.chaincatcher.com/article/2302615", pair="COIN-USDT", src="ChainCatcher",
  date="11/7/2026 16:31:40", url="https://www.bitrue.com/futures/COIN"),
 dict(
  zh_title="民主党计划调查苹果、Meta 和马斯克，特朗普的硅谷盟友面临“清算”",
  zh_desc="据《华盛顿邮报》11 月 6 日报道，民主党赢得国会两院后正确定调查优先事项，苹果因 ICE 追踪应用、Meta 因地方政府数据中心协议受到关注，SpaceX 股价仍坚挺。",
  en_title="Democrats Plan to Investigate Apple, Meta and Musk as Trump's Silicon Valley Allies Face Reckoning",
  en_desc="After winning both chambers, Democrats are setting investigative priorities, with Apple flagged over an ICE-tracking app and Meta over local data-center deals; SpaceX shares held firm.",
  link="https://www.chaincatcher.com/article/2302551", pair="META-USDT", src="ChainCatcher",
  date="11/7/2026 09:02:59", url="https://www.bitrue.com/futures/META"),
 dict(
  zh_title="亚马逊推出基于文本的购物功能",
  zh_desc="亚马逊通过 Alexa 推出基于文本的购物功能，可帮用户搜索比价、追踪促销与价格变动并代为下单；目前向少量受邀美国用户开放，未来几周将扩大。",
  en_title="Amazon Launches Text-Based Shopping Feature",
  en_desc="Amazon launched a text-based shopping feature via Alexa that helps users search and compare products, track deals and prices, and complete purchases; it is initially open to a small group of invited US users.",
  link="https://www.chaincatcher.com/article/2302482", pair="AMZN-USDT", src="ChainCatcher",
  date="11/6/2026 22:09:42", url="https://www.bitrue.com/futures/AMZN"),
]

zh_header=["标题","描述","链接","相关币对","来源","日期","币对地址"]
en_header=["Title","Description","Link","Pair","Source","Date","Pair URL"]

with open("zh_rows.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    w.writerow(zh_header)
    for r in rows:
        w.writerow([r["zh_title"],r["zh_desc"],r["link"],r["pair"],r["src"],r["date"],r["url"]])

with open("en_rows.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f,quoting=csv.QUOTE_ALL)
    w.writerow(en_header)
    for r in rows:
        w.writerow([r["en_title"],r["en_desc"],r["link"],r["pair"],r["src"],r["date"],r["url"]])

print("rows:",len(rows))
import collections
print("pairs:",collections.Counter(r["pair"] for r in rows))
