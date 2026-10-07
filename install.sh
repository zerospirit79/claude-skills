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
