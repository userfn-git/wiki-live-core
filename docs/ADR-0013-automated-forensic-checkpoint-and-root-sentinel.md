# ADR-0013: Automated Forensic Checkpoint, Kernel Hive Unload, and C:\ Root Sentinel

- **Status:** Accepted & Active
- **Date:** 2026-11-18
- **Path / Branch:** `PATH01-BR03` (Security & Access) / `PATH02-BR04` (Architectural Documentation)
- **Author:** Mohammed Al-Khaldi (`userfn-git`) — Engineered with Yusra (`WikiLife Core`)
- **Environment:** `FN-WORKSTATION` (Windows 11 Pro Build 26200)

---

## 1. Context & Problem Statement (السياق وتوصيف المشكلة)
During security auditing of `FN-WORKSTATION`, unauthorized OS staging directories (`C:\$WINDOWS.~BT` and `C:\Windows.old`) repeatedly materialized on the system root (`C:\`) containing over **246,984 binaries** (`SafeOS` mounted WIM images, drivers, and system packages). 

Standard administrative removal (`Remove-Item`, `takeown /R`, `icacls /T`) hung indefinitely or failed due to four root causes:
1. **Single-Threaded ACL Bottleneck:** Traversing ~500,000 total nodes sequentially caused terminal freezes before deletion commands could execute.
2. **Windows 11 Orchestrator Locks:** Background processes (`MoUsoCoreWorker.exe`, `SetupHost.exe`, `SetupPrep.exe`) and services (`UsoSvc`, `WaaSMedicSvc`) actively held file handles.
3. **Mounted WIM & Reparse Points:** Embedded `SafeOS.mount` WIM images and directory junctions blocked standard directory removal.
4. **Kernel-Mounted Registry Hives (`hivelist`):** Staging rollback tasks mounted `C:\$WINDOWS.~BT\NewOS\Users\Default\NTUSER.DAT` and transaction logs (`.TM.blf`) directly into `HKLM:\SYSTEM\CurrentControlSet\Control\hivelist`, locking the final 60 files at the `NT Kernel` level.

---

## 2. Decision (القرار المعماري)
We adopt a two-pillar security architecture within `wiki-live-core`:

### Pillar A: 5-Stage Kernel-Aware Root Eradication Protocol
1. **Process & Service Isolation:** Force-stop `MoUsoCoreWorker`, `SetupPrep`, `SetupHost`, `TiWorker`, and services `UsoSvc`, `wuauserv`, `bits`, `TrustedInstaller`.
2. **WIM & Junction Detachment:** Run `dism.exe /Cleanup-Mountpoints`, `Dismount-WindowsImage -Discard`, and strip `ReparsePoint` junctions without traversing target trees.
3. **64-Thread Backup-Mode Mirror Wipe:** Execute `robocopy.exe <EmptyDir> C:\$WINDOWS.~BT /MIR /B /MT:64` to bypass ACL bottlenecks and purge 246k+ binaries in under 20 seconds.
4. **Kernel Registry Hive Unload:** Enumerate `HKLM:\SYSTEM\CurrentControlSet\Control\hivelist` for `NewOS` or `Windows.old` mounts and detach them via `reg.exe unload`, with fallback registration in `Session Manager\PendingFileRenameOperations` for Kernel Transaction Manager (`.TM.blf`) files.
5. **Trigger Lockdown:** Disable scheduled tasks under `\Microsoft\Windows\Setup\*` and `\Microsoft\Windows\UpdateOrchestrator\*`, set `DisableOSUpgrade = 1`, and redirect update staging to `D:\projects\wiki-live-core\.isolation\WindowsUpdates`.

### Pillar B: Automated Forensic Checkpoint (`WikiLife_Forensic_Checkpoint`)
Deploy a persistent background sentinel (`D:\projects\wiki-live-core\.isolation\checkpoint\wikilife_checkpoint_sentinel.ps1`) running as `NT AUTHORITY\SYSTEM` at startup and every 5 minutes:
- **Process Interception:** Captures any invocation of `SetupHost.exe` or `SetupPrep.exe`, logs PID, Parent PID, CommandLine, Authenticode signature status, and `SHA-256` hash to `.isolation\checkpoint\logs\Forensic_Intercept_<timestamp>.json`.
- **Native EDR / Defender ASR Integration:** Enforces Windows Defender Attack Surface Reduction rule `b2b3f03d-6a65-4f7b-a9c7-1c7ef74a9ba4` (Block untrusted/unsigned processes) and triggers `Start-MpScan -ScanType CustomScan` on intercepted binaries before terminating the process and wiping unauthorized root folders.

---

## 3. Consequences (الأثر المعماري والنتائج)
- **Positive:**
  - `C:\` root remains 100% clean (`0` residual files) without requiring Safe Mode or system reinstallation.
  - Full cryptographic forensic chain (`SHA-256` + Authenticode verification) is generated automatically prior to eradication.
  - Zero performance impact on real-time workloads (such as `fn_physics_engine` and 240 FPS telemetry pipelines).
- **Mitigations:**
  - Raw forensic dumps and quarantine artifacts in `.isolation/` are excluded via `.gitignore` to keep the Git repository lightweight.
