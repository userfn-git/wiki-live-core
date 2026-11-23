# SNAP-20261123: FN Physics Engine, Official Epic Games Two-Way API, Adaptive Curve Tuner & State-Driven WikiLife-Yusra Architecture

- **Date:** 2026-11-23
- **Tree Path & Branch:** `PATH-02: Knowledge Management` -> `BR05: Gemini Session Tree Snapshots`
- **Target Repositories:** `D:\projects\fn_physics_engine` & `D:\projects\wiki-live-core`
- **Workstation Profile:** `FN-WORKSTATION` (Windows 11 Pro, MSYS2 UCRT64 GCC 16.2.0, Python 3.12 `D:\envs\rl_py_env`, GTX 1660 Ti 6GB VRAM, 32GB RAM, Strict `D:\` Isolation)

---

## 1. Executive Summary
Completed the end-to-end, zero-mock, State-Driven closed-loop physics optimization and telemetry ecosystem across `fn_physics_engine` and `wiki-live-core`. All Epic Games replay (`DemosEpic`) and configuration (`Config`) directories are isolated onto Drive `D:` via NTFS Junctions, paired with the official 120Hz `MatchStatsExporter_TA` two-way socket bridge, an adaptive Custom Map / Replay mathematical curve tuner (`rl tune`), an interactive Replay Director inside `src/yusra_agent.py`, and self-healing Lua macro promotion.

---

## 2. Verified Architectural Milestones

### A. Strict Drive D: Isolation (`DemosEpic` & `Config` NTFS Junctions)
- **Replay Storage Isolation:** Enforced directory `Junction` links for `D:\Games\RocketLeague\TAGame\DemosEpic`, `D:\Games\RocketLeague_Config\TAGame\DemosEpic`, and `Documents\My Games\Rocket League\TAGame\DemosEpic` pointing exclusively to `D:\Games\RocketLeague_Replays`.
- **Configuration Isolation:** Enforced directory `Junction` linking `Documents\My Games\Rocket League\TAGame\Config` directly to `D:\Games\RocketLeague_Config\TAGame\Config`, eliminating all Unreal Engine 3 write footprint on Drive `C:` while preserving `0.05` deadzone and KBM bindings.
- **Zero-Bloat Replay Vault Harvester (`rl auto`):** Moves saved `.replay` files immediately upon lock release from `D:\Games\RocketLeague_Replays` into `D:\projects\wiki-live-core\data\replays_vault`, keeping active game replay folders 100% empty.

### B. Official Epic Games `MatchStatsExporter_TA` Integration (Forms 1–4)
- **Authoritative Schema Reference:** Archived complete field definitions, visibility flags (`CONDITIONAL`, `SPECTATOR`, `TEAM`, `REPLAY`), 15 match/replay lifecycle events, and 6 two-way socket commands in `D:\projects\wiki-live-core\docs\reference\EPIC_STATS_API_SCHEMA.md` (`PATH02-BR04`).
- **120Hz Two-Way Stream Engine (`tools/official_stats_api_bridge.py` / `rl stats` & `rl cmd`):**
  - Configured `D:\Games\RocketLeague\TAGame\Config\TAStatsAPI.ini` (`PacketSendRate=120`, `Port=49123`, `WebPort=49124`).
  - Streams and segregates live telemetry into 5 structured CSV logs (`official_stats_telemetry.csv`, `official_ball_hits.csv`, `official_boost_pickups.csv`, `official_goals_crossbars.csv`, `official_statfeed_events.csv`) while isolating goal replay frames (`GoalReplayStart` to `GoalReplayEnd`).
  - Supports outbound JSON client control (`rl cmd`) for `LoadReplay`, `SeekReplay`, `SetGameSpeed`, `ChangePOV`, `SetHUDVisibility`, and `SetMatchPaused`.

### C. Adaptive Math Curve Tuner (`rl tune`) & Self-Healing Lua Promotion
- **Custom Map & Replay Drag Analyzer (`tools/yusra_curve_math_tuner.py`):** Evaluates `turning_drag_ratio` (`avg_powerslide_speed / avg_speed`) and `supersonic_ratio` from official 120Hz telemetry, recalibrates shaping exponents (`curve_alpha`, `Pace`, `double_w_ms`, `triple_w_ms`), synthesizes Pure-ASCII `<250`-line candidates (`FN_PRO_CURVE_TUNED_*.lua`), and renders 200-DPI Before-vs-After comparison curves in Google Chrome.
- **Time-Bound Anti-Stagnation Bot Arena (`rl train [2h|120m]`):** Enforces signature novelty (`seen` set + adaptive neighborhood expansion) grounded in official 120Hz telemetry and halts immediately when `RocketLeague.exe` launches.
- **State-Driven Self-Healing Promotion:** Uses explicit `Test-Path` / `Get-ChildItem` state checks (compatible with silent error handling in `master_profile.ps1`) to archive `D:\Lua\FN_PRO_v9.4.0_FINAL.lua` into `lua/archive/`, promote verified candidates, and sync the Windows Clipboard via `rl lua`.

### D. Interactive Replay Director in Local Terminal Agent (`src/yusra_agent.py`)
- Armed `wikilife-yusra` (`rl agent`) with `control_rocket_league_client` validated against official Epic Games schema constraints (`Focus` `"Ball"` or digit shortcut, 6 approved `Perspective` modes, `Speed >= 0`), enabling natural-language replay direction over TCP `127.0.0.1:49123`.

---

## 3. Unified 13-Action `rl` CLI (`D:\terminals\config\master_profile.ps1`)
- `rl agent [--auto]` | `rl train [2h|120m]` | `rl auto [--watch]` | `rl stats [Player]` | `rl cmd <Name> <Json>` | `rl tune` | `rl live` | `rl play` | `rl yusra` | `rl replay` | `rl plot` | `rl lua` | `rl status` | `rl stop`.

---

## 4. Repository Synchronization State
- **`D:\projects\fn_physics_engine` (`origin/main`):** Synchronized with official 120Hz two-way bridge, `DemosEpic` harvester, anti-stagnation time trainer, `yusra_curve_math_tuner.py`, and promoted Pure-ASCII `<250`-line Lua macro.
- **`D:\projects\wiki-live-core` (`origin/main`):** Synchronized with `EPIC_STATS_API_SCHEMA.md`, `src/yusra_agent.py` Replay Director, and finalized `SNAP-20261123-FN-PHYSICS-240HZ-SHM.md`.
---

## Finalized Session Milestone: FN PRO v9.6.0 & WikiLife Cut-and-Purge Pipeline

- **Lua Macro Finalized ($lineCount lines, Pure ASCII):** D:\Lua\FN_PRO_v9.4.0_FINAL.lua (v9.6.0 G502 X Q/E-Context Edition).
  - **Engine Toggle:** MB3 (Middle Mouse Click) with deterministic 1ms PrecisionSleep and ClearAllInputs() failsafe.
  - **Context Speedflips:** A + MB4 (Q) for Left Speedflip, D + MB5 (E) for Right Speedflip (leaves aerial Q/E unintercepted when A/D are released).
  - **Ergonomic Half-Flip:** S + Left Shift with automatic Q/E roll direction detection and 480ms forward cancel.
  - **Aerial & Dash Controls:** MB7 (Fast Aerial), MB8 (Hold-to-Loop ChainDash), G6 Sniper button excluded.
- **Replay Harvester & Telemetry:** Windows Shell MyDocuments (D:\Documents\My Games\Rocket League\TAGame) unified via NTFS Junctions with icacls Full Control; yusra_autoplan_daemon.py cuts & purges replays directly to D:\projects\wiki-live-core\data\replays_vault and generates rrocket.exe analytics debriefs.
- **In-Game Curve HUD:** Replaced external Chrome plotting with yusra_ingame_curve_hud.py (127.0.0.1:49125 frameless overlay).
