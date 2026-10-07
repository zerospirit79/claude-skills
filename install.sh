#!/bin/bash
# Симлинки скиллов этого репозитория в ~/.claude/skills (существующие каталоги не трогает).
set -eu
src=$(cd "$(dirname "$0")" && pwd)
dst=${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}
mkdir -p "$dst"
for d in "$src"/*/; do
	name=$(basename "$d")
	[ -f "$d/SKILL.md" ] || continue
	if [ -L "$dst/$name" ]; then
		ln -sfn "${d%/}" "$dst/$name"
	elif [ -e "$dst/$name" ]; then
		echo "пропущен $name: $dst/$name уже существует и это не симлинк" >&2
		continue
	else
		ln -s "${d%/}" "$dst/$name"
	fi
	echo "$name -> ${d%/}"
done

# Команды pi-observer в ~/.local/bin (pi-start, pi-log, pi-watch)
bin=${BIN_DIR:-$HOME/.local/bin}
mkdir -p "$bin"
for f in pi-start pi-log pi-watch; do
	ln -sfn "$src/pi-observer/scripts/$f" "$bin/$f"
	echo "$bin/$f -> $src/pi-observer/scripts/$f"
done
python3 -c 'import textual' 2>/dev/null ||
	echo "для pi-watch нужен Textual: apt-get install python3-module-textual (или pip install --user textual)" >&2
