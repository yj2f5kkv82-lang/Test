#!/usr/bin/env python3
"""
learn.py - Interactive CLI tutorial: Claude Code subagents, cutting-edge style.
"""

import argparse
import sys

from fun import ascii_banner

# ── ANSI colours ──────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[32m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
RED    = "\033[31m"

def bold(s):    return f"{BOLD}{s}{RESET}"
def green(s):   return f"{GREEN}{s}{RESET}"
def cyan(s):    return f"{CYAN}{s}{RESET}"
def yellow(s):  return f"{YELLOW}{s}{RESET}"
def magenta(s): return f"{MAGENTA}{s}{RESET}"
def dim(s):     return f"{DIM}{s}{RESET}"
def red(s):     return f"{RED}{s}{RESET}"

# ── UI helpers ─────────────────────────────────────────────────────────────────

def hr(char="─", width=60, color=DIM):
    print(f"{color}{char * width}{RESET}")

def pause(prompt="  Press Enter to continue..."):
    try:
        input(dim(prompt))
    except (EOFError, KeyboardInterrupt):
        print()
        sys.exit(0)

def section(title, lesson_num, total=5):
    print()
    hr("═")
    tag = f"  Lesson {lesson_num}/{total}"
    print(f"{YELLOW}{BOLD}{tag}{RESET}  {BOLD}{title}{RESET}")
    hr("═")
    print()

def bullet(items, indent=4):
    for item in items:
        print(" " * indent + green("▸") + "  " + item)

def code_block(code, label=None):
    hr("─", 60, DIM)
    if label:
        print(dim(f"  {label}"))
    for line in code.strip().splitlines():
        print("  " + cyan(line))
    hr("─", 60, DIM)
    print()

def quiz(question, options, correct_index):
    """Single-choice quiz. Returns True if user got it right."""
    print()
    print(bold("  Quiz: ") + question)
    print()
    for i, opt in enumerate(options, 1):
        print(f"    {BOLD}{i}{RESET}. {opt}")
    print()
    while True:
        try:
            raw = input(dim("  Your answer (number): ")).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            sys.exit(0)
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            choice = int(raw)
            break
        print(red("  Please enter a valid number."))
    if choice == correct_index:
        print(green("  ✓ Correct!"))
        return True
    else:
        print(red(f"  ✗ Not quite. The answer is {correct_index}: {options[correct_index - 1]}"))
        return False

# ── Lessons ────────────────────────────────────────────────────────────────────

def lesson_1():
    section("What Are Subagents?", 1)

    print("  Imagine you're running a company.")
    print("  You don't do every task yourself — you delegate to specialists.")
    print()
    print("  " + bold("Claude Code works the same way."))
    print()
    print("  When you give Claude a big task, it can spin up")
    print("  smaller, focused agents — " + bold("subagents") + " — to handle")
    print("  specific parts of the work in parallel.")
    print()
    bullet([
        "The main Claude = the " + bold("manager"),
        "Subagents = the " + bold("specialists"),
        "Each subagent has its own context, tools, and goal",
    ])
    print()
    pause()

    print()
    print("  " + bold("Why does this matter?"))
    print()
    bullet([
        "Subagents run " + bold("in parallel") + " — faster results",
        "Each has a " + bold("fresh context") + " — no clutter from other tasks",
        "You can " + bold("restrict their tools") + " — safer, more focused",
        "You can use " + bold("different models") + " per agent — cost control",
    ])
    print()
    pause()

    print()
    print("  " + bold("A concrete example:"))
    print()
    print("  You ask Claude to review a codebase for bugs.")
    print("  Instead of doing it all serially, Claude might spawn:")
    print()
    bullet([
        "Agent A: scan auth module for security issues",
        "Agent B: check database queries for SQL injection",
        "Agent C: look for performance bottlenecks in API layer",
    ])
    print()
    print("  All three run " + bold("simultaneously") + ".")
    print("  The manager aggregates the results. Done in 1/3 the time.")
    print()
    pause()

    quiz(
        "What is the main benefit of running subagents in parallel?",
        [
            "They use less memory",
            "They complete independent tasks simultaneously, saving time",
            "They share the same context window",
            "They always use a cheaper model",
        ],
        correct_index=2,
    )
    print()
    pause("  Press Enter for the next lesson...")


def lesson_2():
    section("Built-in Agent Types", 2)

    print("  Claude Code ships with three built-in agent types.")
    print("  Claude picks the right one automatically based on your task.")
    print()

    agents = [
        ("Explore",         "haiku (fast)",  "Read, Grep, Glob",          "Quick codebase searching / analysis"),
        ("Plan",            "inherits",      "Read-only",                 "Planning + gathering context before acting"),
        ("general-purpose", "inherits",      "All tools",                 "Complex tasks needing exploration AND edits"),
    ]

    col_widths = [16, 16, 22, 38]
    header = ["Agent", "Model", "Tools", "Best for"]
    header_line = "  " + "  ".join(h.ljust(w) for h, w in zip(header, col_widths))
    print(bold(header_line))
    hr("─", 60)
    for row in agents:
        line = "  " + "  ".join(str(v).ljust(w) for v, w in zip(row, col_widths))
        print(green("  ▸") + line[2:])
    print()
    pause()

    print()
    print("  " + bold("Explore agent") + " — the workhorse of code analysis")
    print()
    print("  It uses Claude Haiku (fast + cheap) and has " + bold("read-only") + " tools.")
    print("  Perfect for: searching, understanding, summarising.")
    print("  It never touches your files.")
    print()
    pause()

    print()
    print("  " + bold("Plan agent") + " — the architect")
    print()
    print("  Activated when you enter Claude Code's " + bold("plan mode") + " (Shift+Tab).")
    print("  Gathers context, outlines steps, shows you the plan")
    print("  before any code is written. You approve before it acts.")
    print()
    pause()

    print()
    print("  " + bold("general-purpose agent") + " — the full-stack worker")
    print()
    print("  Has access to all tools: Read, Write, Edit, Bash, Grep…")
    print("  Used for complex multi-step work that needs to both")
    print("  explore and make changes.")
    print()
    pause()

    quiz(
        "Which built-in agent is fastest and cheapest to run?",
        [
            "general-purpose (it has all the tools)",
            "Plan (it just thinks, never writes)",
            "Explore (it uses Claude Haiku and is read-only)",
            "They all cost the same",
        ],
        correct_index=3,
    )
    print()
    pause("  Press Enter for the next lesson...")


def lesson_3():
    section("Writing Your Own Agent", 3)

    print("  Built-in agents are great, but the real power comes from")
    print("  defining " + bold("custom agents") + " tuned to your project.")
    print()
    print("  Drop a Markdown file in " + cyan(".claude/agents/") + " and you're done.")
    print()
    pause()

    print()
    print("  Here's a real example — a " + bold("security-reviewer") + " agent:")
    print()

    code_block("""\
---
name: security-reviewer
description: >
  Expert security code reviewer. Use when asked to check for
  vulnerabilities, audit authentication, or review API endpoints.
tools: Read, Grep, Glob
model: opus
maxTurns: 15
---

You are a senior security engineer with deep expertise in:
- OWASP Top 10 vulnerabilities
- Authentication and session management
- SQL injection, XSS, CSRF

When invoked, you:
1. Read the relevant files
2. List every vulnerability found (severity: LOW / MED / HIGH / CRIT)
3. Suggest a concrete fix for each issue""",
        label=".claude/agents/security-reviewer.md",
    )

    pause()

    print("  Let's break down the frontmatter fields:")
    print()
    fields = [
        ("name",        "Unique identifier. Must be lowercase, no spaces."),
        ("description", "The most important field. Claude reads this to decide"),
        ("",            "  when to automatically invoke the agent."),
        ("tools",       "Comma-separated list of tools the agent is allowed."),
        ("",            "  Omit to inherit all tools from the parent."),
        ("model",       "haiku | sonnet | opus. Default: inherits parent model."),
        ("maxTurns",    "Max number of back-and-forth turns before stopping."),
    ]
    for name, desc in fields:
        if name:
            print(f"  {CYAN}{BOLD}{name:<14}{RESET}  {desc}")
        else:
            print(f"  {'':14}  {desc}")
    print()
    pause()

    print()
    print("  " + bold("Where do agent files live?"))
    print()
    bullet([
        cyan(".claude/agents/")    + "  — project-level (checked into git, shared with team)",
        cyan("~/.claude/agents/")  + "  — user-level (applies to all your projects)",
    ])
    print()
    print("  Project-level agents take priority over user-level.")
    print()
    pause()

    print()
    print("  " + bold("How to invoke your custom agent:"))
    print()
    bullet([
        bold("Automatic: ") + "Claude reads the description and delegates on its own",
        bold("Explicit:  ") + 'Say "Use the security-reviewer agent to check auth.py"',
    ])
    print()
    pause()

    quiz(
        "Which field tells Claude WHEN to automatically use your custom agent?",
        [
            "name — it matches on the agent's name",
            "description — Claude reads it to decide when to delegate",
            "model — the model choice triggers delegation",
            "tools — agents with fewer tools are preferred",
        ],
        correct_index=2,
    )
    print()
    pause("  Press Enter for the next lesson...")


def lesson_4():
    section("Model Routing: Right Model for the Job", 4)

    print("  Not every task needs the smartest (and most expensive) model.")
    print("  Routing different agents to different models is a")
    print("  " + bold("cost and speed superpower") + ".")
    print()

    models = [
        ("haiku",   "Fastest. Cheapest.",          "Search, grep, summarise, quick Q&A"),
        ("sonnet",  "Balanced. Default choice.",   "General coding, explanations, reviews"),
        ("opus",    "Most capable. Slowest.",       "Complex reasoning, security audits, architecture"),
    ]

    print(f"  {BOLD}{'Model':<10}  {'Speed/Cost':<26}  Best for{RESET}")
    hr("─", 60)
    for model, cost, use in models:
        print(f"  {GREEN}▸{RESET} {CYAN}{model:<10}{RESET}  {cost:<26}  {use}")
    print()
    pause()

    print()
    print("  " + bold("In a custom agent file, set the model in frontmatter:"))
    print()

    code_block("""\
---
name: fast-searcher
description: Quick keyword searches across the codebase
tools: Read, Grep, Glob
model: haiku          # fast + cheap — perfect here
---

Search the codebase and return matching snippets only.""",
        label=".claude/agents/fast-searcher.md",
    )

    code_block("""\
---
name: deep-architect
description: High-level architectural design decisions and trade-offs
tools: Read, Glob, Grep
model: opus           # complex reasoning — worth the cost
---

You think deeply about system design before suggesting changes.""",
        label=".claude/agents/deep-architect.md",
    )

    pause()

    print()
    print("  " + bold("Rule of thumb for model selection:"))
    print()
    bullet([
        bold("Haiku")  + "  → any agent that just reads and searches",
        bold("Sonnet") + "  → most writing, coding, and analysis tasks",
        bold("Opus")   + "  → security audits, complex refactors, design work",
    ])
    print()
    print("  Mixing models across agents in a workflow can cut your")
    print("  API costs by " + bold("50–80%") + " with no quality loss on simple tasks.")
    print()
    pause()

    quiz(
        "You need an agent that scans 200 files for TODO comments. Which model?",
        [
            "Opus — it will be more thorough",
            "Sonnet — always safest default",
            "Haiku — it's a simple search task, save money and time",
            "The model doesn't matter for file scanning",
        ],
        correct_index=3,
    )
    print()
    pause("  Press Enter for the final lesson...")


def lesson_5():
    section("Parallel Agents: The Killer Feature", 5)

    print("  This is where Claude Code becomes genuinely " + bold("superhuman") + ".")
    print()
    print("  By default, tools run one at a time.")
    print("  With multiple subagents, work runs " + bold("simultaneously") + ".")
    print()
    pause()

    print()
    print("  " + bold("Scenario: review a large PR"))
    print()
    print("  Serial approach (one agent):")
    bullet([
        "Read auth changes          (8 s)",
        "Check database queries     (6 s)",
        "Scan API endpoints         (7 s)",
        "Review tests               (5 s)",
    ])
    print()
    print("  " + bold("Total: ~26 seconds"))
    print()
    pause()

    print()
    print("  Parallel approach (4 agents):")
    bullet([
        "Agent A: auth changes   ┐",
        "Agent B: DB queries     ├── all running at the same time",
        "Agent C: API endpoints  │",
        "Agent D: tests          ┘",
    ])
    print()
    print("  " + bold("Total: ~8 seconds") + "  (bottlenecked by the slowest agent only)")
    print()
    pause()

    print()
    print("  " + bold("How to trigger parallel agents:"))
    print()
    print("  Just write a prompt that has " + bold("independent parallel tasks") + ".")
    print("  Claude figures out the parallelism automatically.")
    print()

    code_block("""\
Analyse the authentication, database, and API modules in parallel.
Use a separate subagent for each area.
Each agent should:
  1. Read the relevant files
  2. List security concerns
  3. Suggest improvements

Summarise all three findings at the end.""",
        label="Example prompt that triggers parallel agents",
    )

    pause()

    print()
    print("  " + bold("Context isolation — why it matters:"))
    print()
    print("  Each subagent starts with a " + bold("fresh context window") + ".")
    print("  The main conversation stays clean and focused.")
    print("  An Explore agent can read 50 files; none of that")
    print("  noise bleeds back into the parent agent.")
    print()
    bullet([
        "Agents do NOT share context with each other",
        "The ONLY link is: prompt in → result out",
        "Include all needed context explicitly in the prompt",
    ])
    print()
    pause()

    print()
    print("  " + bold("Advanced: worktree isolation"))
    print()
    print("  For agents that write files, add " + cyan("isolation: worktree") + "")
    print("  to the frontmatter. The agent gets a separate git")
    print("  branch to work in — no risk of clobbering your work.")
    print()

    code_block("""\
---
name: auto-refactor
description: Refactor code for readability and performance
tools: Read, Edit, Write, Grep, Glob
model: sonnet
isolation: worktree   # works in a temp branch — safe!
---

Refactor the code without changing public API surfaces.""",
        label=".claude/agents/auto-refactor.md",
    )

    pause()

    quiz(
        "What is the main technical reason subagents speed things up?",
        [
            "They skip permission checks so they run faster",
            "They run simultaneously on independent tasks",
            "They use smaller models which respond quicker",
            "They cache results from previous runs",
        ],
        correct_index=2,
    )

    print()
    hr("═")
    print()
    print("  " + bold(green("You've completed all 5 lessons!")))
    print()
    print("  " + bold("What to do next:"))
    print()
    bullet([
        "Create " + cyan(".claude/agents/") + " in your project",
        "Write one custom agent with a clear description",
        "Try a prompt that asks Claude to use it",
        "Experiment with " + cyan("model: haiku") + " on search-only agents",
        "Use " + cyan("isolation: worktree") + " for agents that modify files",
    ])
    print()
    print("  " + dim("Resources:"))
    print("  " + dim("  https://docs.anthropic.com/en/docs/claude-code/sub-agents"))
    print("  " + dim("  https://docs.anthropic.com/en/docs/claude-code/sdk"))
    print()
    hr("═")
    print()


# ── Lesson registry ───────────────────────────────────────────────────────────

LESSONS = [
    ("What Are Subagents?",                   lesson_1),
    ("Built-in Agent Types",                  lesson_2),
    ("Writing Your Own Agent",                lesson_3),
    ("Model Routing: Right Model for the Job",lesson_4),
    ("Parallel Agents: The Killer Feature",   lesson_5),
]

# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Interactive Claude Code subagents tutorial.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Run with no arguments to start from lesson 1.",
    )
    parser.add_argument(
        "--lesson",
        metavar="N",
        type=int,
        help="Jump to lesson N (1–5)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all lesson titles and exit",
    )
    args = parser.parse_args()

    if args.list:
        print()
        for i, (title, _) in enumerate(LESSONS, 1):
            print(f"  {GREEN}{i}{RESET}. {title}")
        print()
        return

    # Validate --lesson
    if args.lesson is not None:
        if not (1 <= args.lesson <= len(LESSONS)):
            print(red(f"  Error: --lesson must be between 1 and {len(LESSONS)}."))
            sys.exit(1)
        start = args.lesson - 1
    else:
        start = 0

    # Banner
    print()
    print(cyan(ascii_banner("LEARN")))
    print()
    print("  " + bold("Claude Code: Subagents") + "  " + dim("— an interactive tutorial"))
    if start > 0:
        print("  " + dim(f"Jumping to lesson {args.lesson}…"))
    print()
    pause("  Press Enter to begin...")

    for fn in [fn for _, fn in LESSONS[start:]]:
        fn()

    if start == 0:
        print("  " + dim("Run `python learn.py --list` to see all lessons."))
        print("  " + dim("Run `python learn.py --lesson 3` to jump to a specific lesson."))
        print()


if __name__ == "__main__":
    main()
