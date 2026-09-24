# Antigravity Global Engineering Protocol & Skill Lifecycle

This document defines the global development protocol for Antigravity on this machine. Follow these lifecycle stages and activate the corresponding global skills at the appropriate moment:

---

## 1. Ideation & Requirements Phase
* **Trigger:** When starting any new feature, creative component, or significant behavior modification.
* **Skill to activate:** `brainstorming`
  * Clarify user intent, explore architecture, and validate requirements *before* touching code.
* **Autonomous PRD / Spec generation:**
  * For structured requirements: activate `ralph-tui-prd` to generate a PRD with user stories.
  * For loop-driven execution: activate `ralph-tui-create-json` to convert PRDs into `prd.json`.

---

## 2. Planning & Workspace Isolation Phase
* **Trigger:** When moving from requirements to execution.
* **Skills to activate:**
  * `writing-plans`: Generate a step-by-step implementation plan with verifiable checkpoints before editing files.
  * `using-git-worktrees`: Isolate feature development in a separate git worktree or branch so the main branch stays clean and functional.

---

## 3. Implementation & Testing Phase
* **Trigger:** When actively writing code.
* **Skills to activate:**
  * `test-driven-development` (TDD): Write the failing test first, write minimal code to pass, then refactor.
  * `executing-plans`: For sequential single-session execution of plans.
  * `subagent-driven-development` / `dispatching-parallel-agents`: When tasks are independent and can be parallelized across subagents without shared state.
  * `ralph-loop-workflow` / `ralph-wiggum`: When running long-running autonomous iteration loops against specs until all acceptance criteria pass.

---

## 4. Debugging & Web Interaction Phase
* **Trigger:** When encountering bugs, test failures, unexpected behaviors, or web navigation tasks.
* **Skills to activate:**
  * `systematic-debugging`: Mandatorily investigate root cause (reproduce, isolate, hypothesize, verify) before proposing any patch. Never guess or apply speculative fixes.
  * `browser-use` / `agent-browser`: When requiring browser automation, CDP control, web scraping, form submission, or visual web testing.

---

## 5. Verification & Completion Phase
* **Trigger:** When work is believed to be finished, before declaring completion or merging.
* **Skills to activate:**
  * `verification-before-completion`: **MANDATORY RULE:** Never claim a task is complete, fixed, or passing without executing verification commands and verifying actual test output.
  * `requesting-code-review`: Perform rigorous automated code review against requirements before merge.
  * `finishing-a-development-branch`: Clean up git worktrees/branches, determine integration strategy (squash/rebase/merge).

---

## 6. Ecosystem & Meta-Skills
* `find-skills`: When the user asks "how do I do X", "find a skill for X", or requires new capabilities from the skills.sh ecosystem.
* `skill-creator`: When authoring or refining new skills for Antigravity.

---

## 7. Security & Supply Chain Defense (Anti-Malware Gate)
* **Trigger:** When downloading, inspecting, or installing skills, repos, or agent profiles from external sources.
* **Skill to activate:** `skill-security-guard`
* **MANDATORY SECURITY RULE:**
  - Before executing or installing untrusted third-party code from GitHub, audit the repository using the `skill-security-guard` scanner.
  - Immediate Block Triggers: Reverse shells, Base64/IEX obfuscation, credential exfiltration (`.ssh`, `.aws`, `.env`), Windows Defender tampering, or destructive system commands (`rm -rf`, disk wipes).

