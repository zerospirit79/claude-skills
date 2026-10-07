# claude-skills

Личные скиллы Claude Code.

| Скилл | Назначение |
|---|---|
| `alt-spec-review` | Ревью пакетирования ALT: .spec, .gear/rules, changelog (локально, через gitoskop или по girar-заданию) |
| `pi-observer` | Тестирование на Poligon: Claude — контролёр/наблюдатель, `pi` — исполнитель (`scripts/pi-start`, `scripts/pi-log`) |

## Установка

```bash
./install.sh   # симлинки ~/.claude/skills/<скилл> -> этот репозиторий
```

Скиллы `poligon-*` сюда не входят — их ставит отдельный установщик qa-basealt-skills.
