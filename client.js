window.__ModuleLoader__.load({
  id: '@local/rwa-skills',
  factory(require) {
    const React = require('react');
    const h = React.createElement;
    const NS = 'rwa-skills';

    const DICT = {
      'zh-CN': {
        'entry.title': 'RWA 工具箱',
        'panel.title': 'RWA 工具箱',
        'panel.subtitle':
          '点「开始」会直接新建一个对话并自动发送引导，无需再手动点发送。',
        'card.start': '开始',
        'tag.vpn': '需 VPN',
        'tag.cookie': '需 Cookie',
        'card.news.title': 'RWA 每日资讯',
        'card.news.desc':
          '采集 20 个币对的最新英文资讯，直接在对话里列出英文表格，确认后上架 Bitrue 后台并回查校验。',
        'card.calendar.title': '金十日历同步',
        'card.calendar.desc':
          '抓取金十财经日历，按天挑选 Top3 英文数据，在对话里列出，确认后同步到 Bitrue 事件日历。',
      },
      'en-US': {
        'entry.title': 'RWA Toolbox',
        'panel.title': 'RWA Toolbox',
        'panel.subtitle':
          'Clicking Start opens a new chat and sends the guidance automatically.',
        'card.start': 'Start',
        'tag.vpn': 'VPN',
        'tag.cookie': 'Cookie',
        'card.news.title': 'RWA daily news',
        'card.news.desc':
          'Collect the latest English news for 20 pairs, list them in chat as an English table, then publish to the Bitrue backend and verify.',
        'card.calendar.title': 'Jin10 calendar sync',
        'card.calendar.desc':
          'Fetch the Jin10 economic calendar, pick a Top3 per day in English, list them in chat, then sync to the Bitrue event calendar.',
      },
    };

    const PROMPTS = {
      news: [
        '我要运行「RWA 每日资讯」流程（请加载并使用技能 rwa-daily-news）。请严格按下面顺序引导我，不要跳步：',
        '',
        '1. 先让我确认已连接公司 VPN。',
        '2. 提示我用 Chrome 的 Cookie-Editor 扩展获取 Bitrue 后台 Cookie：',
        '   - 打开 https://newsd.bitapple.com 并登录后台；',
        '   - 点 Cookie-Editor 扩展 → Copy → 选 Header string；',
        '   - 把整段 Cookie 粘到对话里发给你（每次运行都要重新复制，因为会过期）。',
        '3. 拿到 Cookie 后先做连接测试：',
        "   curl -sS --noproxy '*' --max-time 8 -o /dev/null -w '%{http_code}' https://newsd.bitapple.com/",
        '   能返回 HTTP 状态码（200/302/401 等）就表示已连内网；连不上就提醒我检查 VPN、并关闭全局代理（7897）。',
        '4. 连接通过后，按 rwa-daily-news 技能执行：采集 10 条最新资讯，**直接在对话里用英文 7 列表格列出（不要再写飞书表格）**，等我确认后再上架 Bitrue 后台并回查校验。',
        '',
        'Cookie 只在本次对话里使用：直接在 curl 里用 -b "名字=值; ..." 带上即可，不要在回复里明文回显，也不要写入文件或交给其他工具。',
      ].join('\n'),
      calendar: [
        '我要运行「金十日历同步」流程（请加载并使用技能 jin10-calendar-sync）。请严格按下面顺序引导我，不要跳步：',
        '',
        '1. 先让我确认已连接公司 VPN。',
        '2. 提示我用 Chrome 的 Cookie-Editor 扩展获取 Bitrue 后台 Cookie：',
        '   - 打开 https://newsd.bitapple.com 并登录后台；',
        '   - 点 Cookie-Editor 扩展 → Copy → 选 Header string；',
        '   - 把整段 Cookie 粘到对话里发给你（每次运行都要重新复制，因为会过期）。',
        '3. 先做连接测试：',
        "   curl -sS --noproxy '*' --max-time 8 -o /dev/null -w '%{http_code}' https://newsd.bitapple.com/",
        '   能返回 HTTP 状态码就表示已连内网；连不上就提醒我检查 VPN、并关闭全局代理（7897）。',
        '4. 连接通过后，先问我抓取的日期范围（含两端），再按 jin10-calendar-sync 技能执行：抓取金十日历、每天挑 3 条重点，**直接在对话里用英文表格列出（不要再写飞书表格）**，等我确认后再推送到 Bitrue 事件日历并回查。',
        '',
        'Cookie 只在本次对话里使用，不要在回复里明文回显，也不要写入文件或交给其他工具。',
      ].join('\n'),
    };

    const COLORS = {
      base: 'var(--dsw-alias-bg-base)',
      layer1: 'var(--dsw-alias-bg-layer-1)',
      layer2: 'var(--dsw-alias-bg-layer-2)',
      border1: 'var(--dsw-alias-border-l1)',
      border2: 'var(--dsw-alias-border-l2)',
      primary: 'var(--dsw-alias-label-primary)',
      secondary: 'var(--dsw-alias-label-secondary)',
      brand: 'var(--dsw-alias-brand-primary)',
    };

    const pageStyle = {
      minHeight: '100%',
      background: COLORS.base,
      color: COLORS.primary,
      overflowY: 'auto',
    };
    const wrapStyle = { maxWidth: 720, margin: '0 auto', padding: '28px 24px' };
    const titleStyle = { fontSize: 20, fontWeight: 700, margin: '0 0 6px' };
    const subtitleStyle = { color: COLORS.secondary, fontSize: 13, margin: '0 0 22px', lineHeight: 1.6 };
    const cardsStyle = { display: 'flex', flexDirection: 'column', gap: 16 };
    const cardStyle = {
      border: '1px solid ' + COLORS.border1,
      background: COLORS.layer1,
      borderRadius: 12,
      padding: '18px 20px',
    };
    const tagRowStyle = { display: 'flex', gap: 6, marginTop: 8 };
    const tagStyle = {
      fontSize: 11,
      padding: '1px 8px',
      borderRadius: 999,
      border: '1px solid ' + COLORS.border2,
      color: COLORS.secondary,
      background: COLORS.layer2,
    };
    const descStyle = {
      color: COLORS.secondary,
      fontSize: 13,
      lineHeight: 1.65,
      margin: '10px 0 16px',
    };
    const btnRowStyle = { display: 'flex', justifyContent: 'flex-end' };
    const btnStyle = {
      padding: '7px 18px',
      borderRadius: 8,
      border: '1px solid ' + COLORS.brand,
      background: COLORS.brand,
      color: '#ffffff',
      fontSize: 13,
      fontWeight: 600,
      cursor: 'pointer',
    };

    function RwaIcon(props) {
      const size = (props && props.size) || 24;
      return h(
        'svg',
        {
          width: size,
          height: size,
          viewBox: '0 0 24 24',
          fill: 'none',
          stroke: 'currentColor',
          strokeWidth: 1.8,
          strokeLinecap: 'round',
          strokeLinejoin: 'round',
          'aria-hidden': true,
          focusable: 'false',
          style: { display: 'block' },
        },
        h('rect', { x: 3.5, y: 4.5, width: 17, height: 15, rx: 2.5 }),
        h('path', { d: 'M7 9h6M7 12.5h10M7 16h8' }),
      );
    }

    return {
      inject: ['slots'],
      apply(ctx) {
        let t = (key, fallback) => fallback;
        try {
          if (ctx.locale) {
            ctx.effect(() => ctx.locale.register(NS, DICT));
            const tr = ctx.locale.bind(NS);
            t = (key, fallback) => {
              try {
                const v = tr(key);
                return v || fallback;
              } catch (_) {
                return fallback;
              }
            };
          }
        } catch (_) {
          t = (key, fallback) => fallback;
        }

        function getService(name) {
          try {
            return typeof ctx.get === 'function' ? ctx.get(name) : ctx[name];
          } catch (_) {
            return undefined;
          }
        }

        function recentWorkspaceId(items, byId) {
          let selected;
          let selectedTime = -Infinity;
          for (const w of items) {
            let latest = -Infinity;
            for (const id of w.sessionIds || []) {
              const s = byId[id];
              if (s !== undefined && typeof s.updatedAt === 'number') latest = Math.max(latest, s.updatedAt);
            }
            if (latest === -Infinity) {
              const created = Date.parse(w.createdAt);
              if (!Number.isNaN(created)) latest = created;
            }
            if (selected === undefined || latest > selectedTime) {
              selected = w.workspaceId;
              selectedTime = latest;
            }
          }
          return selected;
        }

        async function start(kind) {
          const ui = getService('uiWorkspace');
          const workspaces = getService('workspaces');
          const sessions = getService('sessions');
          const conversation = getService('conversation');
          const text = PROMPTS[kind];
          if (!ui || typeof ui.startSession !== 'function') {
            console.error('[rwa-skills] uiWorkspace service is unavailable');
            return;
          }
          try {
            let target;
            try {
              if (workspaces && workspaces.list && sessions && sessions.list) {
                target = recentWorkspaceId(
                  workspaces.list.getSnapshot().items || [],
                  sessions.list.getSnapshot().byId || {},
                );
              }
            } catch (_) {
              target = undefined;
            }
            if (target === undefined || typeof ui.connectWorkspace !== 'function' || !sessions) {
              // No resolvable workspace: leave an unsent draft instead of doing nothing.
              ui.startSession(undefined, { prompt: text, whenDraftExists: 'replace' });
              return;
            }
            const sessionId = await ui.connectWorkspace(target, {});
            if (typeof ui.openSession === 'function') ui.openSession(sessionId);
            const ref = sessions.retain(sessionId, { source: 'controllerOperation' });
            try {
              const binding = await ref.ready;
              if (conversation && typeof conversation.sendSession === 'function') {
                await conversation.sendSession(binding.session, text, [], 'queue');
              } else {
                await binding.session.prompt([{ type: 'text', text }], 'queue');
              }
            } finally {
              ref.release();
            }
          } catch (err) {
            console.error('[rwa-skills] failed to auto-send prompt', err);
            try {
              ui.startSession(undefined, { prompt: text, whenDraftExists: 'replace' });
            } catch (_) {
              /* ignore */
            }
          }
        }

        function renderCard(kind) {
          return h(
            'div',
            { style: cardStyle, key: kind },
            h('div', { style: { fontSize: 15, fontWeight: 600 } }, t('card.' + kind + '.title', kind)),
            h(
              'div',
              { style: tagRowStyle },
              h('span', { style: tagStyle }, t('tag.vpn', '需 VPN')),
              h('span', { style: tagStyle }, t('tag.cookie', '需 Cookie')),
            ),
            h('div', { style: descStyle }, t('card.' + kind + '.desc', '')),
            h(
              'div',
              { style: btnRowStyle },
              h(
                'button',
                {
                  type: 'button',
                  style: btnStyle,
                  onClick: () => start(kind),
                },
                t('card.start', '开始'),
              ),
            ),
          );
        }

        function Panel() {
          return h(
            'div',
            { style: pageStyle },
            h(
              'div',
              { style: wrapStyle },
              h('h1', { style: titleStyle }, t('panel.title', 'RWA 工具箱')),
              h('p', { style: subtitleStyle }, t('panel.subtitle', '')),
              h('div', { style: cardsStyle }, renderCard('news'), renderCard('calendar')),
            ),
          );
        }

        ctx.slots.inject('sidebar.panellist', () =>
          ctx.slots.register(
            {
              name: 'sidebar.panellist',
              id: 'rwa-skills',
              order: 5,
              label: () => t('entry.title', 'RWA 工具箱'),
            },
            RwaIcon,
          ),
        );

        ctx.slots.inject('main', () =>
          ctx.slots.register({ name: 'main', key: 'rwa-skills' }, Panel),
        );
      },
    };
  },
});
