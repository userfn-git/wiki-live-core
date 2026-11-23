# SNAP-20261123: FN Physics Engine, Epic Games DemosEpic Auto-Harvester & WikiLife-Yusra Closed-Loop System

- **Date:** 2026-11-23
- **Tree Path & Branch:** `PATH-02: Knowledge Management` -> `BR05: Gemini Session Tree Snapshots`
- **Target Repositories:** `D:\projects\fn_physics_engine` & `D:\projects\wiki-live-core`
- **Workstation Profile:** `FN-WORKSTATION` (Windows 11 Pro, MSYS2 UCRT64 GCC 16.2.0, Python 3.12 `D:\envs\rl_py_env`, GTX 1660 Ti 6GB VRAM, 32GB RAM, Strict `D:\` Isolation)

---

## 1. Executive Summary
Finalized the closed-loop, zero-mock, and zero-bloat physics optimization pipeline across `fn_physics_engine` and `wiki-live-core`. All Epic Games replay storage (`DemosEpic`) is isolated onto Drive `D:` via directory Junctions, harvested immediately into the WikiLife Vault upon save, decoded via `rrrocket.exe`, analyzed by local `wikilife-yusra`, and paired with a time-bound offline bot arena trainer (`rl train`) and safe macro auto-promoter (`rl auto`).

---

## 2. Verified Architectural Milestones

1. **Epic Games `DemosEpic` Junction Isolation & Zero-Bloat Replay Harvester (`tools/yusra_autoplan_daemon.py`):**
   - Verified and enforced NTFS directory `Junction` links for `D:\Games\RocketLeague\TAGame\DemosEpic`, `D:\Games\RocketLeague_Config\TAGame\DemosEpic`, and `Documents\My Games\Rocket League\TAGame\DemosEpic` pointing exclusively to `D:\Games\RocketLeague_Replays` (zero `C:` drive dependency).
   - Running `rl auto` (or `rl auto --watch`) harvests any newly saved `.replay` immediately after file-lock release and moves it into `D:\projects\wiki-live-core\data\replays_vault`, keeping game replay directories 100% empty to prevent in-game storage bloat or input feel degradation.

2. **Authentic Replay Decoding & Multi-Panel Curve Plotting (`rrrocket.exe` + `tools/plot_telemetry_curves.py`):**
   - Configured official `rrrocket.exe` CLI in `D:\Tools\rrrocket` to extract authentic `RigidBody` coordinates (`X, Y, Z`), attitude angles (`Pitch, Yaw, Roll`), and real velocity (`speed_uu`) into `logs/replay_physics_extracted.csv`.
   - Generates executive match debriefs under `D:\projects\wiki-live-core\docs\match_analytics\` and renders 200-DPI dark-mode charts opened automatically in Google Chrome via `rl plot`.

3. **Time-Bound Anti-Stagnation Offline Bot Trainer (`tools/yusra_offline_trainer.py`):**
   - Upgraded `rl train [2h|120m]` to execute time-scheduled `240Hz` kinematic arena rollouts grounded in real replay velocity ratios (`load_real_replay_baseline`).
   - Enforced signature-based novelty (`seen` set + adaptive scale expansion) to prevent parameter stagnation, raising baseline fitness from `1822.717` to `2244.64` (`+23.15%`) and synthesizing pure-ASCII `<250`-line Logitech G HUB Lua candidates in `lua/candidates/`.
   - Active `RocketLeague.exe` process watchdog halts simulation immediately upon game launch to yield 100% of GTX 1660 Ti and CPU resources.

4. **Safe Gate Macro Auto-Promotion & Unified 11-Action `rl` CLI (`D:\terminals\config\master_profile.ps1`):**
   - `rl auto` enforces a `>= 5.0%` fitness gain gate before archiving `D:\Lua\FN_PRO_v9.4.0_FINAL.lua` to `lua/archive/`, promoting the winning candidate, and copying the clean Lua code to the Windows Clipboard (`rl lua`).
   - Consolidated all operational workflows into `rl` (`agent`, `train`, `auto`, `live`, `play`, `yusra`, `replay`, `plot`, `lua`, `status`, `stop`).

---

## 3. Repository Synchronization State
- **`D:\projects\fn_physics_engine` (`origin/main`):** Up to date with `DemosEpic` harvester, anti-stagnation time trainer, `rrrocket` spatial parser, and dual-mode plotter.
- **`D:\projects\wiki-live-core` (`origin/main`):** Updated `SNAP-20261123-FN-PHYSICS-240HZ-SHM.md` under `PATH02-BR05` with active `data/replays_vault` and `docs/match_analytics` integration.