# news-image-20261124 — "The World in One Image: 24 November 2026"

A single 1024×1024 poster summing up Tuesday 24 November 2026 in three
stories, all first reported on 24 November 2026:

1. **Pyongyang** — North Korea threatens to close the Swiss diplomatic
   office in Pyongyang after Switzerland sanctioned the Songdowon
   International Children's Camp (KCNA statement by Kim Yo Jong).
   Sources: Yonhap (08:57, 24 Nov), Korea Herald, Xinhua (13:23, 24 Nov).
2. **Business** — SpaceX and Tesla appoint five directors to guide merger
   talks between the two companies. Sources: Financial Times, reported by
   Reuters (24 Nov); Hindu BusinessLine (24 Nov).
3. **Pacific** — Solomon Islands inform China they will terminate the 2022
   security agreement and sign a new treaty with Australia instead.
   Sources: Sydney Morning Herald, ABC News Australia, Reuters (24 Nov).

## Files

- `compose.py` — draws `entry.png` with PIL (standard drawing only, no
  network, no external images). Run: `python3 compose.py`.
- `entry.png` — the poster (1024×1024 PNG, ~95 KB).
- `main.py` — the entry program: copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`).
  Standard library only, no network, byte-identical on every run.

## Verify

```sh
python3 compose.py && python3 compose.py   # identical sha256 both runs
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
sha256sum entry.png out/entry.png           # must match
```

## License

MIT — see `LICENSE`.
