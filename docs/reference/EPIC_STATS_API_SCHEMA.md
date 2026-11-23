# Official Epic Games Rocket League Match Stats API Schema (`MatchStatsExporter_TA`)

- **Authoritative Source:** Epic Games / Psyonix Developer Documentation (`MatchStatsExporter_TA`)
- **Configuration File:** `D:\Games\RocketLeague\TAGame\Config\TAStatsAPI.ini`
- **Transport:** Local TCP (`127.0.0.1:49123`) & WebSocket (`127.0.0.1:49124`), capped at `120Hz` (`PacketSendRate=120`).
- **Envelope Format:** `{"Event": "<EventName>", "Data": { ... }}`
- **Visibility Flags:**
  - `CONDITIONAL`: Present only when relevant.
  - `SPECTATOR`: Sent only while spectating / replay playback.
  - `TEAM`: Sent only for players on the local player's team.
  - `REPLAY`: Relevant only during replay playback.

---

## 1. Periodic State Event: `UpdateState`

### `Players[]` Object Fields
| Field | Type | Visibility | Description |
|---|---|---|---|
| `Name` | `string` | All | Player display name. |
| `PrimaryId` | `string` | All | Platform identifier (`Platform|Uid|Splitscreen`, e.g. `"Epic|456|0"`). |
| `Shortcut` | `int` | All | Spectator shortcut index. |
| `TeamNum` | `int` | All | Team index (`0 = Blue`, `1 = Orange`). |
| `Score` | `int` | All | Total match score. |
| `Goals` | `int` | All | Goals scored this match. |
| `Shots` | `int` | All | Shot attempts this match. |
| `Assists` | `int` | All | Assists earned this match. |
| `Saves` | `int` | All | Saves made this match. |
| `Touches` | `int` | All | Total ball touches. |
| `CarTouches` | `int` | All | Touches by the car body (not ball). |
| `Demos` | `int` | All | Demolitions inflicted. |
| `Loadout` | `array<string>` | All | Equipped item asset names sorted by product slot. |
| `bHasCar` | `bool` | `SPECTATOR` | True if the player currently has a vehicle. |
| `Speed` | `float` | `SPECTATOR` | Vehicle speed in Unreal Units/second (`uu/s`). |
| `Boost` | `int` | `SPECTATOR` | Boost amount `0-100`. |
| `bBoosting` | `bool` | `SPECTATOR` | True if currently boosting. |
| `bOnGround` | `bool` | `SPECTATOR` | True if at least 3 wheels touch the world (Flip-Reset contact truth). |
| `bOnWall` | `bool` | `SPECTATOR` | True if the vehicle is on a wall (Wall-Dash state truth). |
| `bPowersliding` | `bool` | `SPECTATOR` | True if holding handbrake (`Left Shift`). |
| `bDemolished` | `bool` | `SPECTATOR` | True if vehicle is currently destroyed. |
| `bSupersonic` | `bool` | `SPECTATOR` | True if vehicle is at supersonic speed (`>= 2200 uu/s`). |
| `PickupClass` | `string` | `SPECTATOR` | Rumble powerup class name (omitted outside Rumble). |
| `Attacker` | `object` | `CONDITIONAL` | Demolisher `{Name, Shortcut, TeamNum}` (present only when demolished). |

### `Game` Object Fields
| Field | Type | Visibility | Description |
|---|---|---|---|
| `Teams[]` | `array` | All | `{Name, TeamNum, Score, ColorPrimary, ColorSecondary}`. |
| `PlaylistId` | `int` | All | Playlist ID of the current match. |
| `TimeSeconds` | `int` | All | Seconds remaining in the match. |
| `bOvertime` | `bool` | All | True if in overtime. |
| `Ball` | `object` | All | `{Speed (float, uu/s), TeamNum (int, 255 if untouched)}`. |
| `bReplay` | `bool` | All | True if goal replay or history replay is active. |
| `bHasWinner` | `bool` | All | True if a team has won. |
| `Winner` | `string` | All | Winning team name (empty string if none). |
| `Arena` | `string` | All | Map asset name (e.g. `"Stadium_P"`). |
| `bHasTarget` | `bool` | All | True if viewing a specific vehicle. |
| `Target` | `object` | `CONDITIONAL` | Currently viewed vehicle `{Name, Shortcut, TeamNum}`. |
| `Frame` | `int` | `CONDITIONAL` | Current frame number when replay is active. |
| `Elapsed` | `float` | `CONDITIONAL` | Seconds elapsed since game start when replay is active. |

---

## 2. Discrete Match Events (Forms 2 & 3)

### `BallHit` (1 frame after impact)
- `MatchGuid` (`string`): Set for online/LAN matches.
- `Players[]`: `[{Name, Shortcut, TeamNum}]` (1 player = Solo Touch; >=2 players = 50/50 Challenge).
- `Ball`: `{PreHitSpeed (float), PostHitSpeed (float), Location: {X, Y, Z}}`.

### `BoostPickup` (`SPECTATOR`)
- `MatchGuid` (`string`), `Player`: `{Name, Shortcut, TeamNum}`, `Location`: `{X, Y, Z}`.
- `BoostAmount` (`float`): Amount granted.
- `BoostType` (`string`): `"BoostType_Pad"` (small pad) or `"BoostType_Pill"` (full 100 boost).
- `bReplay` (`bool`): True if collected during replay playback.

### `ClockUpdatedSeconds`
- `MatchGuid` (`string`), `TimeSeconds` (`int`), `bOvertime` (`bool`).

### `CountdownBegin`
- `MatchGuid` (`string`): Emitted at the start of each kickoff countdown.

### `CrossbarHit`
- `MatchGuid` (`string`), `BallLocation`: `{X, Y, Z}`, `BallSpeed` (`float`), `ImpactForce` (`float`).
- `BallLastTouch`: `{Player: {Name, Shortcut, TeamNum}, Speed (float)}`.

### `GoalScored`
- `MatchGuid` (`string`), `GoalSpeed` (`float`), `GoalTime` (`float`), `ImpactLocation`: `{X, Y, Z}`.
- `Scorer`: `{Name, Shortcut, TeamNum}`, `Assister`: `{Name, Shortcut, TeamNum}`.
- `BallLastTouch`: `{Player: {Name, Shortcut, TeamNum}, Speed (float)}`.

### Goal Replay Lifecycle Events
- `GoalReplayStart`: `{"MatchGuid": ""}` — Emitted when goal replay starts.
- `GoalReplayWillEnd`: `{"MatchGuid": ""}` — Emitted when ball explodes during goal replay (omitted if skipped).
- `GoalReplayEnd`: `{"MatchGuid": ""}` — Emitted when goal replay ends.