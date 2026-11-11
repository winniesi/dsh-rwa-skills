#!/usr/bin/env python3
"""金十财经日历 · 免登录抓取器

rili.jin10.com 的日数据来自一个公开的 JSON 接口，只需带上网页面板用到的
x-app-id / x-version 请求头即可，完全不需要登录、不需要 cookie、不需要浏览器。

接口（主机 https://e0430d16720e4211b5e072c26205c890.z3c.jin10.com）：
  /get/data?date=YYYY-MM-DD&category=cj     宏观数据（时间/指标/前值/预测值/公布值/星级/单位）
  /get/event?date=YYYY-MM-DD&category=cj    财经事件（央行决议、讲话、会议等）
  /get/holiday?date=YYYY-MM-DD&category=cj  交易所休市（含前后约两个月）

用法：
  python3 scripts/jin10_fetch.py --start 2026-11-11 --end 2026-11-18
  python3 scripts/jin10_fetch.py --start 2026-11-11 --end 2026-11-18 --top3 --json-out /tmp/out.json

注意：接口返回的 pub_time 就是北京时间，字段 previous/consensus/actual 已解析好，
比原技能里靠 DOM 抓 .jin-table-row 稳定得多。
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

BASE = "https://e0430d16720e4211b5e072c26205c890.z3c.jin10.com"
HEADERS = {
    "x-app-id": "rU6QIu7JHe2gOUeR",
    "x-version": "1.0.0",
    "Referer": "https://rili.jin10.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}
TIMEOUT = 25


def _get(path: str, day: str) -> dict:
    url = f"{BASE}{path}?" + urllib.parse.urlencode({"date": day, "category": "cj"})
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if payload.get("status") != 200:
        raise RuntimeError(f"{path} {day}: status={payload.get('status')!r} "
                           f"message={payload.get('message')!r}")
    return payload


# 技能里的人工重要度顺序：越靠前越重要
HIGH = ("CPI", "GDP", "PPI", "非农", "失业率", "零售", "利率决议", "利率决定", "议息")
MED = ("PMI", "ZEW", "库存", "钻井", "工业产出", "贸易帐", "经常帐", "消费者信心",
       "耐用品", "房屋", "营建", "初请", "ADP", "薪资", "通胀", "货币供应", "社融", "贷款")


def _rank(item: dict) -> tuple:
    """启发式排序：星级 > 关键词 > 是否有预测值（仅供 Top3 参考，人工可覆盖）。"""
    name = str(item.get("indicator_name") or "")
    star = int(item.get("star") or 0)
    kw = 2 if any(k in name for k in HIGH) else 1 if any(k in name for k in MED) else 0
    has_consensus = 1 if item.get("consensus") not in (None, "", "--") else 0
    return (star, kw, has_consensus)


def fetch_day(day: str) -> dict:
    macro = _get("/get/data", day).get("data") or []
    events = _get("/get/event", day).get("data") or []
    return {"date": day, "macro": macro, "events": events}


def compact_macro(item: dict) -> dict:
    return {
        "time": item.get("pub_time", ""),
        "name": item.get("indicator_name", ""),
        "country": item.get("country", ""),
        "star": item.get("star"),
        "previous": item.get("previous"),
        "revised": item.get("revised"),
        "consensus": item.get("consensus"),
        "actual": item.get("actual"),
        "unit": item.get("unit", ""),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="金十财经日历免登录抓取")
    ap.add_argument("--start", required=True, help="起始日期 YYYY-MM-DD（含）")
    ap.add_argument("--end", required=True, help="结束日期 YYYY-MM-DD（含）")
    ap.add_argument("--top3", action="store_true", help="每天按启发式挑出最重要的 3 条宏观数据")
    ap.add_argument("--json-out", help="把结果写到该 JSON 文件")
    ap.add_argument("--include-events", action="store_true", help="同时输出财经事件")
    args = ap.parse_args()

    d0 = date.fromisoformat(args.start)
    d1 = date.fromisoformat(args.end)
    if d1 < d0:
        ap.error("--end 不能早于 --start")

    result = []
    cur = d0
    while cur <= d1:
        ds = cur.isoformat()
        day = fetch_day(ds)
        macro = [compact_macro(x) for x in day["macro"]]
        entry = {"date": ds, "macro_count": len(macro),
                 "events_count": len(day["events"])}
        if args.top3:
            ranked = sorted(macro, key=_rank, reverse=True)
            entry["top3"] = ranked[:3]
        else:
            entry["macro"] = macro
        if args.include_events:
            entry["events"] = [
                {"time": e.get("event_time"), "country": e.get("country"),
                 "star": e.get("star"), "time_status": e.get("time_status"),
                 "content": e.get("event_content")}
                for e in day["events"]
            ]
        result.append(entry)
        if entry["macro_count"] == 0 and entry["events_count"] == 0:
            entry["note"] = "当日无宏观数据与事件（金十可能显示暂无数据）"
        cur += timedelta(days=1)

    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"已写入 {args.json_out}", file=sys.stderr)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
