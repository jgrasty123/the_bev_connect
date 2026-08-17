# Rate review — /rate-calculator

The public rate calculator prices from two configured constants and one carrier
grid. A stale constant makes every estimate on the page wrong without throwing
an error, so this needs an owner and a monthly pass.

**Owner:** _unassigned — assign before this page is promoted in sales material._
**Cadence:** monthly.

---

## What to check each month

### 1. Fuel surcharge — `FUEL_SURCHARGE_PCT`

Located at the top of the calculator script in `rate-calculator.html`.

```js
const FUEL_SURCHARGE_PCT = 15.0;
```

| | |
|---|---|
| Current value | 15.0% |
| Last reviewed | 2026-08-17 |
| Provenance | **Back-solved, not quoted.** Reconciles WeShip invoices (BoozeFinders, May–Jun 2026, $25.55–$27.53 actuals) against the 2025 grid for those parcels. |

WeShip bills fuel at UPS's published weekly ground rate; it is explicitly
excluded from the rate grid. Compare against the UPS published ground fuel
surcharge and against the most recent WeShip invoice. If the two disagree,
the invoice wins.

> **Open:** confirm the current published number with the WeShip rep and set
> this deliberately rather than inheriting the back-solved figure.

### 2. Admin fee — `ADMIN_FEE_PCT`

```js
const ADMIN_FEE_PCT = 8.0;   // applied to (carrier base + fuel)
```

Flat 8% per James. Applied to `(carrier base + fuel)`.

> **Open:** confirm the basis. Alternatives are base only, or
> base + fuel + accessorials. Materially different at volume.

The separate 12% on packaging materials (`MATERIALS_ADMIN_PCT`) is a different
mechanism and is not part of this review.

### 3. Adult signature treatment — `ASR_TREATMENT`

```js
const ASR_TREATMENT = 'inclusive';   // 'inclusive' | 'stacked'
const ASR_SURCHARGE = 5.92;
```

The `national_asr` and `national_non_asr` grids differ by exactly $1.25,
uniformly across all 150 weights and all zones. The WeShip notes list
"Adult Signature Required" under PRICING INCLUDES, but Orion Ship UPS invoices
show adult signature at ~$5.92.

Current assumption is **inclusive** — the grid already prices ASR in, and the
$1.25 is a program margin adder.

> **Open — highest impact item on the page.** If ASR is actually stacked,
> every estimate rises ~$5.92 per parcel (~30% on a light parcel). Resolve by
> pulling one WeShip invoice with line-item accessorial detail on an alcohol
> parcel: if ASR appears as its own line, it is stacked. Flipping
> `ASR_TREATMENT` to `'stacked'` is the only code change required.

### 4. Carrier grid

`WESHIP_ASR` / `WESHIP_NASR` in `rate-calculator.html`, verified identical to
`weship-ground-rates-2025.json` (`national_asr` / `national_non_asr`) as of
2026-08-17 — 1,500 cells each, zero variance.

Re-verify whenever WeShip issues a new rate sheet. `UPS_DAILY` is public UPS
retail and drives only the savings comparison.

### 5. ZIP3 → zone table

`assets/data/zip3-zones-930.json`, built from the UPS zone chart for origin
930 (Ventura) via `tools/build_zip3_zones.py`.

Re-pull when UPS republishes zone charts (typically with an annual rate
change). Never hand-edit this file or infer entries from state guesses — an
unmapped ZIP3 correctly falls through to "request a quote."

---

## Log

| Date | Reviewed by | Fuel | Admin | ASR | Notes |
|---|---|---|---|---|---|
| 2026-08-17 | — | 15.0% | 8.0% | inclusive | Initial v2 build. Fuel back-solved; ASR treatment unconfirmed. |
