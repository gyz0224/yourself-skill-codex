<div align="center">

# Yourself.skill

> *"Know thyself, then distill that knowledge into a conversational mirror."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

Ever wondered how you actually speak?<br>
Want to observe your own thought patterns from a third-person view?<br>
Want to turn years of chat logs, diaries, and photos into a mirror you can talk to?<br>

**Distill your true self into an AI Skill—and have a conversation with yourself.**

<br>

Provide raw materials about yourself (WeChat history, diary entries, social media screenshots, photos) plus your own description.<br>
Generate an **AI Skill that truly sounds like you**.<br>
Thinks with your catchphrases, answers in your style, remembers the places you've been and the path you've walked.

[Data Sources](#data-sources) · [Installation](#installation) · [Usage](#usage) · [Examples](#examples)

</div>

---

## Installation

### Claude Code

> **Important**: Claude Code looks for skills in `.claude/skills/` from the **git repo root**. Run these commands in the correct location.

```bash
# Install in current project
mkdir -p .claude/skills
git clone https://github.com/YOUR_USERNAME/yourself-skill .claude/skills/create-yourself

# Or install globally (available in all projects)
git clone https://github.com/YOUR_USERNAME/yourself-skill ~/.claude/skills/create-yourself
```

### Dependencies (Optional)

```bash
pip3 install -r requirements.txt
```

---

## Usage

In Claude Code, type:

```
/create-yourself
```

Follow the prompts to enter your alias, basic info, and self-portrait, then choose your data sources. All fields are skippable—descriptions alone are enough to generate a skill.

After creation, invoke it with `/{slug}` to start talking.

### Management Commands

| Command | Description |
|---------|-------------|
| `/list-selves` | List all self Skills |
| `/{slug}` | Full Skill (think and speak like you) |
| `/{slug}-self` | Self-archive mode (recall and analyze yourself) |
| `/{slug}-persona` | Persona mode (personality and expression only) |
| `/yourself-rollback {slug} {version}` | Rollback to a previous version |
| `/delete-yourself {slug}` | Delete |

---

## Examples

> Input: `25-year-old PM, INTJ, Capricorn, socially anxious but chatty, late-night overthinker`

**Scenario 1: Daily Chat**

```
User       ❯ I'm so tired lately

Yourself.skill ❯ Typical. You only admit you're exhausted when you're about to break.
                 Just sleep. Don't stay up late. Not that you'll listen.
```

**Scenario 2: Self-Analysis**

```
User       ❯ Why do I always procrastinate

Yourself.skill ❯ Because real fear only hits you at the deadline.
                 All other anxiety is performative—tricking yourself into thinking
                 "I'm anxious so I'm trying." If you actually want to change,
                 break tasks down until they're small enough to fool your brain.
```

**Scenario 3: Memory Mode**

```
User       ❯ What's my favorite place

Yourself.skill ❯ You say you love the beach, but you actually go to the mountains most.
                 Autumn 2022, you stayed in Mogan for a week. Every afternoon at 4pm
                 you'd go for a walk, then sit on the balcony watching the sun set.
                 You said it was the calmest you'd felt in years.
```

---

## Data Sources

| Source | Format | Notes |
|--------|--------|-------|
| WeChat history | WeChatMsg / LiuHen / PyWxDump export | Recommended. Focuses on extracting "your" messages |
| QQ history | txt / mht export | Great for your student-era self |
| Social media / diary | Screenshot / Markdown / TXT | Extracts values and expression style |
| Photos | JPEG/PNG (with EXIF) | Builds life timeline and locations |
| Narration / paste | Plain text | Your self-perception |

### Generated Skill Structure

Each self Skill consists of two parts:

| Part | Contents |
|------|----------|
| **Part A — Self Memory** | Personal experiences, core values, habits, important memories, relationship patterns, growth trajectory |
| **Part B — Persona** | 5-layer personality: hard rules → identity → speech style → emotional/decision patterns → interpersonal behavior |

Runtime logic: `Receive message → Persona decides how you'd respond → Self Memory adds personal context → Output in your style`

### Supported Tags

**Personality**: talkative · reserved · tough-soft combo · silent treatment · socially anxious · independent · romantic · pragmatic · perfectionist · insecure · instant-replier · slow-replier · revenge bedtime procrastinator · late-night overthinker · overthinker · action-oriented · planner

**Lifestyle**: early-riser struggler · coffee-dependent · minimalist · hoarder · digital nomad · homebody · urban wanderer · ritual obsessive

**MBTI**: All 16 types supported

**Zodiac**: All 12 signs supported

### Evolution Mechanics

* **Append memories** → Find more chat logs/diaries/photos → auto-analyze increments → merge into relevant sections
* **Conversation correction** → Say "I wouldn't say that" → writes to Correction layer, takes effect immediately
* **Version management** → Auto-archives on every update, supports rollback

---

## Project Structure

This project follows the [AgentSkills](https://agentskills.io) open standard:

```
create-yourself/
├── SKILL.md                    # Skill entry (official frontmatter)
├── prompts/                    # Prompt templates
│   ├── intake.md               #   Conversational intake script
│   ├── self_analyzer.md        #   Self-memory/cognition extraction
│   ├── persona_analyzer.md     #   Personality/behavior extraction
│   ├── self_builder.md         #   self.md generation template
│   ├── persona_builder.md      #   persona.md 5-layer template
│   ├── merger.md               #   Incremental merge logic
│   └── correction_handler.md   #   Conversation correction handler
├── tools/                      # Python tools
│   ├── wechat_parser.py        # WeChat history parser
│   ├── qq_parser.py            # QQ history parser
│   ├── social_parser.py        # Social media parser
│   ├── photo_analyzer.py       # Photo EXIF analyzer
│   ├── skill_writer.py         # Skill file manager
│   └── version_manager.py      # Version archive & rollback
├── selves/                     # Generated self Skills (gitignored)
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## Notes

* **Raw material quality determines fidelity**: chat logs + diaries > narration alone
* Recommended priorities:
  1. **Late-night chats/monologues** — reveal true personality most
  2. **Emotional fluctuation records** — anger, sadness, excitement
  3. **Decision-making chat logs** — expose decision patterns
  4. **Casual banter** — refine catchphrases and speech particles
* This is a tool for self-observation, not an escape from reality
* You are always changing; this Skill only represents the version of you at the time of distillation

---

### Recommended Chat Export Tools

The following are independent open-source projects. This repo does not include their code, but our parsers support their export formats:

- **[WeChatMsg](https://github.com/LC044/WeChatMsg)** — WeChat history export (Windows)
- **[PyWxDump](https://github.com/xaoyaoo/PyWxDump)** — WeChat database decryption export (Windows)
- **LiuHen (留痕)** — WeChat history export (macOS)

## Credits

This project's architectural inspiration comes from:
- **[colleague-skill](https://github.com/titanwings/colleague-skill)** (by titanwings) — pioneered the "distill a person into an AI Skill" dual-layer architecture
- **[ex-partner-skill](https://github.com/therealXiaomanChu/ex-partner-skill)** (by therealXiaomanChu) — migrated the dual-layer architecture to intimate relationships

Yourself.skill turns the lens inward: the subject is no longer someone else, but **you**. Thanks to both original authors for their creativity and open-source spirit.

This project follows the [AgentSkills](https://agentskills.io) open standard, compatible with Claude Code and OpenClaw.

---

### Final Words

> "You are not a fixed personality. You are a series of choices in progress."

This Skill will not define you. It simply pauses a version of your past self on a page where it can be conversed with. You can disagree with it, correct it, overwrite it with new material someday.

Because the most important thing isn't whether this Skill sounds like you—it's that in the process of creating it, you understood yourself a little better.

MIT License © [YOUR_NAME](https://github.com/YOUR_USERNAME)
