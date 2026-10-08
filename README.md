# claude-skills

Личные скиллы Claude Code.

| Скилл | Назначение |
|---|---|
| `alt-spec-review` | Ревью пакетирования ALT: .spec, .gear/rules, changelog (локально, через gitoskop или по girar-заданию) |
| `pi-observer` | Тестирование на Poligon: Claude — контролёр/наблюдатель, `pi` — исполнитель |

## Установка

```bash
./install.sh   # симлинки ~/.claude/skills/<скилл> и ~/.local/bin/{pi-start,pi-log,pi-check,pi-wait,pi-stop,pi-watch,pi-archive}
```

Для `pi-watch` нужен Textual: `apt-get install python3-module-textual` (или `pip install --user textual`).

Скиллы `poligon-*` сюда не входят — их ставит отдельный установщик qa-basealt-skills.

## Команды pi-observer

| Команда | Что делает |
|---|---|
| `pi-start [--bg] <каталог> <phase.md>` | запустить фазу pi (новая сессия), записать в `.pi_runs`; `--bg` — отвязать и вернуться сразу |
| `pi-start [--bg] <каталог> --continue <session-id> <msg.md>` | дописать сообщение в ту же сессию |
| `pi-check <каталог> [session-id]` | приёмка фазы за 5–15 строк: ошибки, «ГОТОВО» поверх ошибок, циклы, опасные действия, Poligon в черновиках, утечки секретов |
| `pi-wait <каталог> [сек]` | молча дождаться конца pi (или цикла) и выдать вердикт pi-check |
| `pi-stop <каталог>` | остановить pi в каталоге |
| `pi-archive [-n] <каталог>` | после `task_close` и `stand_destroy`: удалить скачанные ISO, упаковать каталог (с копией сессий pi) в `<родитель>/<имя>.tar.gz`, удалить каталог |
| `pi-log <session-id> [--brief\|--full --from N]` | лента сессии; секреты из `creds*.sh` маскируются |
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

## Другие агенты (opencode и др.)

opencode читает скиллы из `~/.claude/skills/`, так что `pi-observer` и `alt-spec-review` видны ему без
настройки (`opencode debug skill`). Тексты скиллов нейтральны к агенту: MCP названы по смыслу
(rdb / gitoskop / bugzilla), а для агентов без фоновых задач описан режим `pi-start --bg` + `pi-wait`.
Для неинтерактивного `opencode run` нужен `</dev/null`, иначе он ждёт ввода из stdin.
