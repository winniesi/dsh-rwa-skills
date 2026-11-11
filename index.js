import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

/** Host half: register the two bundled skills into the global skill layer. */
export const inject = ['skills'];

const SKILLS = [
  {
    dir: 'rwa-daily-news',
    name: 'rwa-daily-news',
    description:
      'Bitrue RWA 每日资讯：采集最新英文资讯并在对话中列出英文表，确认后上架 Bitrue 后台并回查。',
    whenToUse:
      '用户提到 RWA 资讯、每日资讯、采集新闻、资讯上架、更新 Bitrue 后台时使用。',
  },
  {
    dir: 'jin10-calendar-sync',
    name: 'jin10-calendar-sync',
    description:
      '金十财经日历：抓取指定日期范围的宏观数据，每天挑 3 条在对话中列出英文表，确认后同步到 Bitrue 事件日历。',
    whenToUse:
      '用户要求同步/抓取财经日历、更新 RWA event calendar、或提到金十日历→Bitrue 流程时使用。',
  },
];

/** Drop the leading YAML front matter; the registry stores name/description separately. */
function stripFrontmatter(text) {
  if (text.charCodeAt(0) === 0xfeff) text = text.slice(1);
  if (text.startsWith('---')) {
    const end = text.indexOf('\n---', 3);
    if (end !== -1) {
      let body = text.slice(end + 4);
      if (body.startsWith('\n')) body = body.slice(1);
      return body;
    }
  }
  return text;
}

export function apply(ctx) {
  const here = path.dirname(fileURLToPath(import.meta.url));

  for (const skill of SKILLS) {
    const dir = path.join(here, 'skills', skill.dir);
    let content;
    try {
      content = stripFrontmatter(readFileSync(path.join(dir, 'SKILL.md'), 'utf8'));
    } catch (err) {
      console.error('[rwa-skills] failed to read skill', skill.dir, err);
      continue;
    }

    ctx.effect(() =>
      ctx.skills.register({
        name: skill.name,
        description: skill.description,
        whenToUse: skill.whenToUse,
        content,
        source: 'bundled',
        resourceBase: { kind: 'directory', path: dir },
      }),
    );
  }
}
