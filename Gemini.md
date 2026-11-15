# Gemini.md - Multi-System Workspace & Mutual Lock Specification

[![WikiLife Core CI](https://github.com/userfn-git/wiki-live-core/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/userfn-git/wiki-live-core/actions/workflows/ci.yml)

> **[MUTUAL-LOCK: Gemini.md <-> README.md | TRUNK: main | OWNER: userfn-git]**

## 1. Mutual Locking Governance
Positioned above WikiLife Core in strict mutual lock with [README.md](./README.md) on branch main.

## 2. Multi-System Specs (Windows / Bash / Linux / WSL / Ubuntu)
| System Layer | Environment | Specification & Role |
|---|---|---|
| Host OS | Windows 11 Pro 64-bit | Primary path D:\projects\wiki-live-core, PowerShell |
| POSIX Shell | MSYS2 Bash (UCRT64) | C++20, Python 3.12, Git ED25519 SSH |
| Linux Subsystem | WSL2 & Ubuntu LTS | Linux kernel runtime, container & Homelab bridge |
| Startup Logging | Shell on Startup | Automated terminal diagnostic & telemetry audit |

## 3. Virtual Tree Hierarchy
```text
[FN-HOMELAB-ROOT]
 +-- Windows-11-Pro (D:\projects\wiki-live-core)
 +-- MSYS2-Bash-UCRT64 (POSIX / SSH)
 +-- WSL2-Ubuntu-Linux (Linux Runtime)
 +-- Shell-on-Startup (Telemetry & Session Audit)
 +-- WikiLife-Core (4 Paths / 12 Branches / Yusra Trunk)
```
