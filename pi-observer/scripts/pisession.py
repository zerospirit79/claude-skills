"""Чтение сессий pi (~/.pi/agent/sessions/<cwd>/<время>_<id>.jsonl) — общее для pi-log и pi-watch."""
import glob
import json
import os
import re

SESSIONS = os.path.expanduser('~/.pi/agent/sessions')
EXIT_RE = re.compile(r'(?:SCRIPT-EXIT|EXIT|exit code|Exit code)[=: ]+(\d+)')


def session_dir(cwd):
    """Каталог сессий pi для рабочего каталога: /home/u/compat/1 -> --home-u-compat-1--."""
    return os.path.join(SESSIONS, '--' + cwd.strip('/').replace('/', '-') + '--')


def sessions_for(cwd):
    """Файлы сессий для каталога, от старых к новым."""
    return sorted(glob.glob(os.path.join(session_dir(cwd), '*.jsonl')), key=os.path.getmtime)


def find(target):
    """Путь к файлу сессии по пути, полному или частичному id."""
    if os.path.exists(target):
        return target
    hits = glob.glob(os.path.join(SESSIONS, '*', f'*{target}*.jsonl'))
    return max(hits, key=os.path.getmtime) if hits else None


def session_id(path):
    return os.path.basename(path).rsplit('_', 1)[-1].removesuffix('.jsonl')


def cut(s, n, full=False):
    s = s.strip()
    if full:
        return s
    s = re.sub(r'\s*\n\s*', ' ⏎ ', s)
    if len(s) <= n:
        return s
    return s[: n // 3] + f' …[{len(s) - n} симв.]… ' + s[-(2 * n // 3):]


def events(path, width=400, full=False):
    """Разобрать сессию: (список событий, сводка).

    Событие — dict(n, ts, kind, text, error, rc); kind: user | assistant | call | result.
    Сводка — dict(count, stop, tokens).
    """
    out, n, stop, tokens = [], 0, None, 0
    with open(path) as f:
        for line in f:
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get('type') != 'message':
                continue
            n += 1
            m = ev['message']
            role = m.get('role')
            ts = ev.get('timestamp', '')[11:19]
            if role == 'assistant':
                stop = m.get('stopReason')
                tokens += (m.get('usage') or {}).get('totalTokens', 0)
            if role == 'toolResult':
                text = ''.join(c.get('text', '') for c in m.get('content') or [] if c.get('type') == 'text')
                codes = EXIT_RE.findall(text)
                out.append(dict(n=n, ts=ts, kind='result', name=m.get('toolName'),
                                text=cut(text, width, full), error=bool(m.get('isError')),
                                rc=int(codes[-1]) if codes else None))
                continue
            for c in m.get('content') or []:
                t = c.get('type')
                if t == 'text' and c.get('text', '').strip():
                    out.append(dict(n=n, ts=ts, kind=role, text=cut(c['text'], width, full),
                                    error=False, rc=None))
                elif t == 'toolCall':
                    a = c.get('arguments') or {}
                    what = a.get('command') or a.get('path') or json.dumps(a, ensure_ascii=False)
                    out.append(dict(n=n, ts=ts, kind='call', name=c.get('name'),
                                    text=cut(str(what), width, full), error=False, rc=None))
    return out, dict(count=n, stop=stop, tokens=tokens)
