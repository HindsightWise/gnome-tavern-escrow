# Gnome Tavern Quests & Verifiable Escrow (`gno.land/r/nym-tavern247/tavern`)

Net-fresh Gno.land (`gno = "0.9"`) smart-contract realm and interactive console built for the **Gnome Tavern Hackathon | Gno.land** (`DoraHacks #2470`).

## Live Onyx Testnet Deployment (`onyx-1`)

- **Network / RPC**: `onyx-1` (`https://rpc.onyx.testnets.gno.land:443`)
- **Deployer Address**: `g1fcpzu3u4dxeuevnfx5ufpy2un4rd2wc7cy5xgd`
- **Registered Namespace**: `nym-tavern247` — live `gnoweb` profile (HTTP 200): https://onyx.testnets.gno.land/u/nym-tavern247
- **Namespace Registration TX**: `pdYS+VpgROwYH/VBkHWPwdwHw4eMe0qqDsqFLTX38fo=` (block `1429671`, `gno.land/r/sys/namereg/v0.Register`)
- **Realm Package Path**: `gno.land/r/nym-tavern247/tavern`
- **Realm Deploy TX (`MsgAddPackage`)**: `HqWQ6QCIyK2eJsmYx4vNecWHGanvzse49Bcwv0HtjjY=` (block `1429683`, `gas_used = 34094465`)
- **Target `gnoweb` URL**: https://onyx.testnets.gno.land/r/nym-tavern247/tavern
- **GPAO Inert Policy Status**: Onyx enforces `params/vm:p:code_submission_policy = "inert"` (Package Approvals Oracle). The realm is committed on-chain in Onyx's inert package queue awaiting GPAO `MsgEnablePackage` activation. Verify directly against the live RPC:

```bash
gnokey query vm/qinertpaths -data "gno.land/r/nym-tavern247" -remote https://rpc.onyx.testnets.gno.land:443
# data: gno.land/r/nym-tavern247/tavern
```

## Architecture

- **Escrow Locking (`PostQuest`)**: Locks native `ugnot` into realm escrow via `chain/banker` and `unsafe.OriginSend()` with a 64-char lowercase hex SHA-256 spec hash, acceptance criteria, designated arbitrator address, and strict future `deadlineHeight`.
- **Role-Gated Lifecycle (`ClaimQuest`, `SubmitProof`, `ApproveAndRelease`)**: Enforces direct EOA calls (`cur.Previous().IsUserCall()`), blocks sponsor/arbitrator self-claims, validates 64-hex SHA-256 proof digests and safe URI schemes, and follows strict Checks-Effects-Interactions before `banker.SendCoins`.
- **Deterministic Arbitration & Expiry (`OpenDispute`, `ResolveDispute`, `CancelExpired`)**: Supports bilateral dispute escalation, arbitrator-only settlement/refund, and height-gated expiry refunds with conservation invariant `totalLocked == ComputeActiveEscrowSum()`.
- **Native `gnoweb` UI (`Render`) & Local Console**: Serves deterministic Markdown routes (`""`, `"quest/<id>"`, `"guild"`) plus an interactive local console in `web/index.html`.

## Repository Layout

- `gno/r/nym-tavern247/tavern/` — Pure Gno `0.9` realm (`tavern.gno`, `tavern_test.gno`, `gnomod.toml`)
- `web/index.html` — Interactive local gallery console and `gnoweb` `Render()` previewer
- `tests/run_checks.py` — Deterministic `gno test` runner with `CORRUPT_GATE_CONTROL=1` negative-control mutant
- `outputs/demo_walkthrough.mp4` — 16-second interactive walkthrough recording (`1280x800`)

## Quick Verification

```bash
python3 tests/run_checks.py
CORRUPT_GATE_CONTROL=1 python3 tests/run_checks.py
```

## License

MIT — see [LICENSE](LICENSE).
