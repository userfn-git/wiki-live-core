# Official Epic Games Rocket League Match Stats API Schema (`MatchStatsExporter_TA`)

- **Authoritative Source:** Epic Games / Psyonix Developer Documentation (`MatchStatsExporter_TA`)
- **Configuration File:** `D:\Games\RocketLeague\TAGame\Config\TAStatsAPI.ini`
- **Transport:** Local TCP (`127.0.0.1:49123`) & WebSocket (`127.0.0.1:49124`), capped at `120Hz` (`PacketSendRate=120`).
- **Telemetry Envelope (Client -> Tool):** `{"Event": "<EventName>", "Data": { ... }}`
- **Command Envelope (Tool -> Client):** `{"Command": "<CommandName>", "Data": { ... }}`
- **Visibility Flags:** `CONDITIONAL` (when relevant), `SPECTATOR` (while spectating/replay), `TEAM` (same team), `REPLAY` (during replay playback).

---

## 1. Periodic Telemetry: `UpdateState`
- **`Players[]`**: `Name`, `PrimaryId` (`Platform|Uid|Splitscreen`), `Shortcut`, `TeamNum` (`0=Blue, 1=Orange`), `Score`, `Goals`, `Shots`, `Assists`, `Saves`, `Touches`, `CarTouches`, `Demos`, `Loadout[]`, `bHasCar`, `Speed` (`uu/s`), `Boost` (`0-100`), `bBoosting`, `bOnGround` (`>=3 wheels`), `bOnWall`, `bPowersliding`, `bDemolished`, `bSupersonic`, `PickupClass`, `Attacker` (`{Name, Shortcut, TeamNum}`).
- **`Game`**: `Teams[]` (`{Name, TeamNum, Score, ColorPrimary, ColorSecondary}`), `PlaylistId`, `TimeSeconds`, `bOvertime`, `Ball` (`{Speed, TeamNum}`), `bReplay`, `bHasWinner`, `Winner`, `Arena`, `bHasTarget`, `Target` (`{Name, Shortcut, TeamNum}`), `Frame` (`REPLAY`), `Elapsed` (`REPLAY`).

---

## 2. All Official Match & Replay Events (Forms 1 to 4)

### Gameplay & Physics Events
- **`BallHit`** (1 frame after impact): `MatchGuid`, `Players[]` (`[{Name, Shortcut, TeamNum}]`), `Ball` (`{PreHitSpeed, PostHitSpeed, Location: {X, Y, Z}}`).
- **`BoostPickup`** (`SPECTATOR`): `MatchGuid`, `Player` (`{Name, Shortcut, TeamNum}`), `Location` (`{X, Y, Z}`), `BoostAmount` (`float`), `BoostType` (`"BoostType_Pad"` | `"BoostType_Pill"`), `bReplay` (`bool`).
- **`CrossbarHit`**: `MatchGuid`, `BallLocation` (`{X, Y, Z}`), `BallSpeed` (`float`), `ImpactForce` (`float`), `BallLastTouch` (`{Player, Speed}`).
- **`GoalScored`**: `MatchGuid`, `GoalSpeed` (`float`), `GoalTime` (`float`), `ImpactLocation` (`{X, Y, Z}`), `Scorer` (`{Name, Shortcut, TeamNum}`), `Assister` (`CONDITIONAL`), `BallLastTouch` (`{Player, Speed}`).
- **`StatfeedEvent`**: `MatchGuid`, `EventName` (e.g. `"Demolish"`, `"Save"`), `Type` (e.g. `"Demolition"`), `MainTarget` (`{Name, Shortcut, TeamNum}`), `SecondaryTarget` (`CONDITIONAL`, same shape).

### Match & Round Lifecycle Events
- **`MatchCreated`**: `{"MatchGuid": "..."}` — Sent when all teams are created and replicated.
- **`MatchInitialized`**: `{"MatchGuid": "..."}` — Sent when the first countdown starts.
- **`CountdownBegin`**: `{"MatchGuid": "..."}` — Sent at the start of each round countdown.
- **`RoundStarted`**: `{"MatchGuid": "..."}` — Sent when active gameplay begins after countdown finishes.
- **`ClockUpdatedSeconds`**: `{"MatchGuid": "...", "TimeSeconds": int, "bOvertime": bool}`.
- **`MatchPaused`** / **`MatchUnpaused`**: `{"MatchGuid": "..."}` — Sent when paused/unpaused by match admin.
- **`MatchEnded`**: `{"MatchGuid": "...", "WinnerTeamNum": int}` — Sent when match ends and winner is chosen.
- **`PodiumStart`**: `{"MatchGuid": "..."}` — Sent when entering post-match podium state.
- **`MatchDestroyed`**: `{"MatchGuid": "..."}` — Sent when leaving the game.

### Replay Lifecycle Events
- **`ReplayCreated`**: `{"MatchGuid": "", "FileName": "Stadium_P_2026-06-05_18-42", "Date": "2026-06-05 18:42:13"}` — Sent when a Match History replay is initialized.
- **`GoalReplayStart`** / **`GoalReplayWillEnd`** / **`GoalReplayEnd`**: `{"MatchGuid": ""}` — Goal replay lifecycle markers.

---

## 3. Two-Way Client Control Commands (Socket Ingestion)

1. **`ChangePOV`** (`SPECTATOR`, `REPLAY`):
   - `Focus`: `"Ball"` or `"<shortcut>"` (all digits string, e.g. `"1"`).
   - `Perspective`: `"Fly"`, `"SoftAttach"`, `"HardAttach"`, `"PlayerView"`, `"AutoCam"`, `"Camera_Director"`.
2. **`LoadReplay`**:
   - `FileName` (`string`, takes precedence) or `Path` (`string`, full file path to `.replay`).
3. **`SeekReplay`** (`REPLAY`):
   - `Frame` (`int`, takes precedence) or `TimeSeconds` (`float`).
4. **`SetGameSpeed`** (`REPLAY`):
   - `Speed` (`float >= 0`, e.g. `0.5` half speed, `1.0` normal, `2.0` double).
5. **`SetHUDVisibility`**:
   - `bVisible` (`bool`).
6. **`SetMatchPaused`**:
   - `bPaused` (`bool`).