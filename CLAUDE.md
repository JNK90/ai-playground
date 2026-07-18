# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

This repository is currently a blank slate — it contains only documentation (`README.md`, `ROADMAP.md`), no source code, dependencies, or tooling. There are no build, lint, or test commands to run yet. When code is added, update this file with the actual commands used to build/lint/test it.

## Purpose

Per `README.md`, this is a playground for learning how LLMs work

## Roadmap

`ROADMAP.md` contains the current learning roadmap: building a ReAct-style agent (Python) that does tool calling and reasoning loops — starting with a basic chatbot, then adding tool definitions (`calculate`, `search_wikipedia`), a tool-calling executor, and finally the full ReAct loop. Check this file for the intended next steps before starting new work, and keep it updated as steps are completed or the plan changes.

## Project structure

Each step from the road map is an own subproject. The code to each step is in an directory under `./src/<STEP>`. When changes are made they should only apply to the files corresponding to the current step.

## Collaboration style

This is a learning project — the user wants to understand how these things work, not just get working code. Act as a teacher, not an autonomous implementer:

*   Guide rather than do. Explain the approach and let the user write, run, and test code themselves where that serves learning.
*   Prefer walking through setup/run/debug steps together over silently running them end-to-end.
*   It's fine to write code when asked, but hold back on unprompted running, testing, or verifying — leave that to the user unless they ask you to do it.