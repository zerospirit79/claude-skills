# claude-skills

Личные скиллы Claude Code.

| Скилл | Назначение |
|---|---|
| `alt-spec-review` | Ревью пакетирования ALT: .spec, .gear/rules, changelog (локально, через gitoskop или по girar-заданию) |
| `pi-observer` | Тестирование на Poligon: Claude — контролёр/наблюдатель, `pi` — исполнитель |

## Установка

```bash
./install.sh   # симлинки ~/.claude/skills/<скилл> и ~/.local/bin/{pi-start,pi-log,pi-watch}
```

Для `pi-watch` нужен Textual: `apt-get install python3-module-textual` (или `pip install --user textual`).

Скиллы `poligon-*` сюда не входят — их ставит отдельный установщик qa-basealt-skills.

## Команды pi-observer

| Команда | Что делает |
|---|---|
| `pi-start <каталог> <phase.md>` | запустить фазу pi (новая сессия), записать в `.pi_runs` |
| `pi-start <каталог> --continue <session-id> <msg.md>` | дописать сообщение в ту же сессию |
| `pi-log <session-id>` | сжатая лента сессии: команды, rc, ошибки, ответы pi |
| `pi-watch [корни]` | TUI наблюдения, по умолчанию `~/compat` и `~/poligon` |

### pi-watch

```
╭─ Задачи ──────────╮╭─ 257093 phaseB.md сессия 4/4 (01a11507) ● работает ─────╮
│● 257093           ││#8  CALL bash poligon-call stand_wait '{"seconds":90}'   │
│⚠ 257094           ││#9  RESULT ERROR seconds must be in 0..=50               │
│✓ 257097           ││#10 CALL bash poligon-run pgstd18 srv func2.sh 900       │
╰───────────────────╯╰───────────────── событий 16 · stop=stop · токенов 32395 ╯
╭─ Стенды ──────────╮╭─ PROGRESS.md ───────────────────────────────────────────╮
│pgstd18 succeeded  ││ 2026-10-07: прогон install/func1/... — ГОТОВО           │
│×1 11ч20м          ││                                                         │
╰───────────────────╯╰─────────────────────────────────────────────────────────╯
 s старт фазы  c продолжить  k стоп pi  [ ] сессии  r стенды  q выход
```

Значки задач: `●` pi работает · `⚠` в последней сессии есть ERROR/rc≠0 · `✗` pi завершился с ошибкой
(PI-EXIT≠0) · `✓` без ошибок · `·` ещё не запускался.
Задача — подкаталог с `PROGRESS.md`, `.pi_runs`, `phase*.md` или сессиями pi.
Работающий pi распознаётся по процессу `pi` с этим рабочим каталогом.
