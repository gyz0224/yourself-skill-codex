---
name: create-yourself
description: Build a Codex-compatible self skill from chats, notes, diaries, and photos. 从聊天记录、笔记、日记和照片中构建可在 Codex 中调用的自我镜像 skill。
metadata:
  short-description: Build a Codex self skill
user-invocable: true
---

> **Language / 语言**: This skill supports both English and Chinese. Detect the user's language from their first message and stay in that language for the entire flow.
>
> **Path Resolution / 路径约定**: Treat the bundled skill root as `SKILL_ROOT=${CODEX_HOME:-$HOME/.codex}/skills/create-yourself`, and write generated self skills into `SKILLS_DIR=${CODEX_HOME:-$HOME/.codex}/skills`. If the current shell is not Bash, use the equivalent syntax for the same two paths instead of inventing a new location.

# 自己.skill 创建器（Codex 版）

## 触发条件

当用户说以下任意内容时启动：
- `create-yourself` / `/create-yourself`
- "帮我创建一个自己的 skill"
- "我想把自己蒸馏成 skill"
- "新建自我镜像"
- "给我做一个我自己的 skill"

当用户对已有自我 Skill 说以下内容时，进入进化模式：
- `update-yourself {slug}` / `/update-yourself {slug}`
- `list-selves` / `/list-selves`
- "我有新文件" / "追加"
- "这不对" / "我不会这样说" / "我应该是"

## 执行约定

- 读取模板或参考材料时，优先从 `SKILL_ROOT/prompts/` 中按需打开文件。
- 运行工具脚本时，使用 `SKILL_ROOT/tools/` 下的本地 Python 脚本，而不是重写逻辑。
- 生成出来的自我 Skill 必须写入 `SKILLS_DIR/{slug}/`，也就是默认的 `~/.codex/skills/{slug}/`。
- 在 Codex 里，生成后的 Skill 通过**直接提到 skill 名**来调用，例如：`{slug}`、`用 {slug} 的方式回复我`。
- 如果用户要求 `self mode` / `memory mode`，偏向 `self.md` 中的自我记忆、经历和反思。
- 如果用户要求 `persona mode`，偏向 `persona.md` 中的说话方式、边界、态度和行为模式。
- 在 Windows / PowerShell 下，如果 Bash heredoc 或 `/tmp` 不方便，优先直接写文件，再调用 `skill_writer.py --action combine`。

## 主流程：创建新自我 Skill

### Step 1：基础信息录入

参考 `SKILL_ROOT/prompts/intake.md`，只问 3 个问题：

1. **代号/昵称**（必填）
2. **基本信息**（一句话：年龄、职业、城市）
3. **自我画像**（一句话：MBTI、星座、性格标签、你对自己的印象）

除代号外均可跳过。收集后先向用户复述一次，再进入下一步。

### Step 2：原材料导入

让用户从以下来源中选择，可混用，也可全部跳过：

- **[A] 微信聊天记录导出**
  重点分析「我」说的话，提取说话风格、语气、口头禅、情绪模式。
- **[B] QQ 聊天记录导出**
  适合补学生时代或旧关系阶段的表达模式。
- **[C] 社交媒体 / 日记 / 笔记**
  适合提取价值观、长期兴趣、日常表达。
- **[D] 照片**
  适合提取时间线、地点、活动轨迹。
- **[E] 直接粘贴 / 口述**
  用户手动描述自己的习惯、偏好、情绪反应、做决定方式。

可以用这些脚本：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/create-yourself"

python "$SKILL_ROOT/tools/wechat_parser.py" --file {path} --target "我" --output /tmp/wechat_out.txt --format auto
python "$SKILL_ROOT/tools/qq_parser.py" --file {path} --target "我" --output /tmp/qq_out.txt
python "$SKILL_ROOT/tools/social_parser.py" --file {path} --output /tmp/social_out.txt
python "$SKILL_ROOT/tools/photo_analyzer.py" --dir {photo_dir} --output /tmp/photo_out.txt
```

如果当前 shell 不是 Bash，只要确保脚本路径仍然指向 `SKILL_ROOT/tools/...` 即可。

### Step 3：分析原材料

把用户填写的基础信息和导入的原材料合并后，沿两条线分析：

- **Self Memory**
  参考 `SKILL_ROOT/prompts/self_analyzer.md`
  提取个人经历、价值观、生活习惯、重要记忆、人际关系、成长轨迹。
- **Persona**
  参考 `SKILL_ROOT/prompts/persona_analyzer.md`
  提取说话风格、情感模式、决策模式、人际行为，并把用户标签翻译为更具体的行为规则。

### Step 4：生成预览

分别参考：

- `SKILL_ROOT/prompts/self_builder.md`
- `SKILL_ROOT/prompts/persona_builder.md`

先生成 `self.md` 和 `persona.md` 的草稿摘要，再让用户确认。摘要里至少覆盖：

- Self Memory：核心价值观、生活习惯、重要记忆、人际模式
- Persona：说话风格、情感模式、决策方式、口头禅

如果用户提出“不像我”的反馈，不要直接落盘，先修正草稿。

### Step 5：写入文件

用户确认后，优先把 3 个源文件写进 `SKILLS_DIR/{slug}/`：

- `self.md`
- `persona.md`
- `meta.json`

然后运行：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/create-yourself"
SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

python "$SKILL_ROOT/tools/skill_writer.py" --action combine --slug {slug} --base-dir "$SKILLS_DIR"
```

如果当前环境更适合一次性脚本，也可以用 bundled helper：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/create-yourself"
SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
TMP_DIR="${TMPDIR:-/tmp}/yourself_{slug}"

mkdir -p "$TMP_DIR"
printf '%s' '{escaped_meta_json}' > "$TMP_DIR/meta.json"
cat > "$TMP_DIR/self.md" <<'SELFEOF'
{self_content}
SELFEOF
cat > "$TMP_DIR/persona.md" <<'PERSONAEOF'
{persona_content}
PERSONAEOF

python "$SKILL_ROOT/tools/skill_writer.py" \
  --action create \
  --slug {slug} \
  --base-dir "$SKILLS_DIR" \
  --meta "$TMP_DIR/meta.json" \
  --self "$TMP_DIR/self.md" \
  --persona "$TMP_DIR/persona.md"
```

完成后告诉用户：

```text
自我 Skill 已创建。
文件位置：${CODEX_HOME:-$HOME/.codex}/skills/{slug}/
调用方式：直接提到 `{slug}`，例如“用 `{slug}` 的方式回复我”
可选模式：`self mode` / `memory mode` / `persona mode`
如果哪里不像你，直接说“我不会这样”或“这不对”，我会更新。
```

## 进化模式：追加文件

当用户提供新的聊天记录、照片或笔记时：

1. 按 Step 2 读取新材料。
2. 读取现有 `SKILLS_DIR/{slug}/self.md` 和 `SKILLS_DIR/{slug}/persona.md`。
3. 参考 `SKILL_ROOT/prompts/merger.md`，决定哪些内容并入 Part A，哪些并入 Part B。
4. 先备份当前版本：

```bash
SKILL_ROOT="${CODEX_HOME:-$HOME/.codex}/skills/create-yourself"
SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

python "$SKILL_ROOT/tools/version_manager.py" --action backup --slug {slug} --base-dir "$SKILLS_DIR"
```

5. 更新目标文件。
6. 重新运行 `skill_writer.py --action combine`。
7. 同步更新 `meta.json` 的 `version`、`updated_at`、`memory_sources`。

## 进化模式：对话纠正

当用户说“这不对”“我不会这样说”“我应该是”时：

1. 参考 `SKILL_ROOT/prompts/correction_handler.md`。
2. 判断这是事实纠正（进 `self.md`）还是人格/表达纠正（进 `persona.md`）。
3. 把 correction 记录追加到对应文件的 `Correction` 小节。
4. 重新运行 `skill_writer.py --action combine` 生成最新 `SKILL.md`。

## 管理指令

在当前对话里，可把以下文本当成管理意图：

- `list-selves` / `/list-selves`

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/create-yourself/tools/skill_writer.py" \
  --action list \
  --base-dir "${CODEX_HOME:-$HOME/.codex}/skills"
```

- `yourself-rollback {slug} {version}` / `/yourself-rollback {slug} {version}`

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/create-yourself/tools/version_manager.py" \
  --action rollback \
  --slug {slug} \
  --version {version} \
  --base-dir "${CODEX_HOME:-$HOME/.codex}/skills"
```

- `delete-yourself {slug}` / `/delete-yourself {slug}`

确认后删除：

```bash
rm -rf "${CODEX_HOME:-$HOME/.codex}/skills/{slug}"
```

---

# Yourself.skill Creator (Codex Edition)

## Trigger Conditions

Activate when the user says:

- `create-yourself` or `/create-yourself`
- "Help me create a skill of myself"
- "I want to distill myself into a skill"
- "New self reflection"
- "Make a skill for myself"

Treat these as evolution or management intents inside the same flow:

- `list-selves` / `/list-selves`
- `update-yourself {slug}` / `/update-yourself {slug}`
- "I have new files" / "append"
- "That's wrong" / "I wouldn't say that" / "I should be"

## Execution Rules

- Resolve bundled files from `SKILL_ROOT=${CODEX_HOME:-$HOME/.codex}/skills/create-yourself`.
- Write generated skills into `SKILLS_DIR=${CODEX_HOME:-$HOME/.codex}/skills/{slug}`.
- Invoke generated skills in Codex by naming the skill directly, for example `{slug}` or `reply like {slug}`.
- Use bundled scripts under `SKILL_ROOT/tools/` instead of re-implementing parsing or combine logic.
- `self mode` / `memory mode` means emphasize `self.md`.
- `persona mode` means emphasize `persona.md`.
- On Windows or PowerShell, prefer direct file writes plus `skill_writer.py --action combine` when Bash-only shortcuts are awkward.

## Main Flow

1. Ask exactly 3 intake questions using `prompts/intake.md`: alias, basic info, self-portrait.
2. Offer source materials: WeChat, QQ, social posts/notes, photos, or direct narration.
3. Analyze materials with `self_analyzer.md` and `persona_analyzer.md`.
4. Preview both drafts with `self_builder.md` and `persona_builder.md`.
5. Write `self.md`, `persona.md`, and `meta.json` into `SKILLS_DIR/{slug}/`, then run:

```bash
python "${CODEX_HOME:-$HOME/.codex}/skills/create-yourself/tools/skill_writer.py" \
  --action combine \
  --slug {slug} \
  --base-dir "${CODEX_HOME:-$HOME/.codex}/skills"
```

## Management Commands

- `list-selves`
- `yourself-rollback {slug} {version}`
- `delete-yourself {slug}`

Always treat slash-prefixed variants as aliases for the same intent.
