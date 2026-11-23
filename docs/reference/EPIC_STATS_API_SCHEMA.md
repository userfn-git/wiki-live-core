# Official Epic Games Rocket League Match Stats API Schema (`MatchStatsExporter_TA`)

- **Configuration File:** `D:\Games\RocketLeague\TAGame\Config\TAStatsAPI.ini`
- **Transport:** Local TCP (`127.0.0.1:49123`) & WebSocket (`127.0.0.1:49124`), capped at `120Hz` (`PacketSendRate=120`).
- **Envelope:** `{"Event": "<EventName>", "Data": { ... }}`

---

## Form 1 & 2: `UpdateState` Payload Specification

### `Players[]` Fields
- `Name` (string): Display name.
- `PrimaryId` (string): Format `Platform|Uid|Splitscreen` (e.g., `"Epic|456|0"`).
- `Shortcut` (int), `TeamNum` (int: `0=Blue`, `1=Orange`), `Score` (int).
- `Goals`, `Shots`, `Assists`, `Saves`, `Touches`, `CarTouches`, `Demos` (int).
- `Loadout` (array<string>): Equipped items sorted by product slot.
- `bHasCar` (bool, SPECTATOR), `Speed` (float, uu/s), `Boost` (int, 0-100).
- `bBoosting` (bool, SPECTATOR), `bOnGround` (bool: >=3 wheels touching world), `bOnWall` (bool), `bPowersliding` (bool), `bDemolished` (bool), `bSupersonic` (bool).
- `PickupClass` (string, SPECTATOR/CONDITIONAL: Rumble item).
- `Attacker` (object, CONDITIONAL on demolition): `{Name, Shortcut, TeamNum}`.

### `Game` Object Fields
- `Teams[]`: `{Name, TeamNum, Score, ColorPrimary, ColorSecondary}`.
- `PlaylistId` (int), `TimeSeconds` (int), `bOvertime` (bool), `Arena` (string, e.g. `"Stadium_P"`).
- `Ball`: `{Speed (float, uu/s), TeamNum (int, 255 if untouched)}`.
- `bReplay` (bool), `bHasWinner` (bool), `Winner` (string).
- `bHasTarget` (bool), `Target` (object, CONDITIONAL): `{Name, Shortcut, TeamNum}`.
- `Frame` (int, CONDITIONAL in replay), `Elapsed` (float, CONDITIONAL in replay).

---

## Form 2 Event: `BallHit`
Emitted **1 frame after** the ball is struck.
- `MatchGuid` (string)
- `Players[]`: `[{Name, Shortcut, TeamNum}]` (1 player = Solo Touch; >=2 players = 50/50 Challenge)
- `Ball`:
  - `PreHitSpeed` (float, uu/s)
  - `PostHitSpeed` (float, uu/s)
  - `Location`: `{X (float), Y (float), Z (float)}`