# Intraday archive QA report

- Generated: 2026-09-23T00:36:43.118490-04:00
- Files checked: 1581 (240 tickers, 8 bar-dates)
- QA tool: `tools/qa_intraday.py` — flags only, nothing deleted or corrected
- Daily envelope source: `data\cache\bars`

## Summary

- regular-session coverage < 98%: 1097 files
- interior gap minutes across archive: 711467
- envelope violations (high/low): 0 / 0
- volume-sum mismatches (> 2%): 0
- daily-bar envelope unavailable (missing/not-loaded): 1314 files
- naive-tz / not-minute-floored / unsorted / dup-ts files: 0 / 0 / 0 / 0

## Anomalies (flagged, not fixed)

| file | rows | RTH coverage | gap minutes | OHLC violations | env>High | env<Low | vol ratio | zero-vol mins | NaN prices | non-pos prices | dup timestamps | naive tz | not floored | unsorted | daily missing | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-09-11/ABSI.parquet | 410 | 90.5% | 550 | 0 | 0 | 0 |  | 56 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/ACRS.parquet | 350 | 87.9% | 264 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/ADTN.parquet | 337 | 82.0% | 408 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  |  | RTH coverage 82.0% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/AESI.parquet | 376 | 92.6% | 298 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.6% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/AG.parquet | 557 | 100.0% | 403 | 0 | 0 | 0 |  | 166 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/ALKT.parquet | 402 | 90.8% | 363 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/AMRX.parquet | 318 | 76.7% | 541 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | RTH coverage 76.7% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/ANGX.parquet | 402 | 90.5% | 521 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/ANNX.parquet | 386 | 92.8% | 553 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/APUS.parquet | 28 | 6.4% | 411 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 6.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/ARHS.parquet | 312 | 78.0% | 619 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/ARIS.parquet | 380 | 90.3% | 406 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/ASM.parquet | 449 | 99.7% | 330 | 0 | 0 | 0 |  | 59 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/AUTL.parquet | 322 | 73.1% | 609 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/BBWI.parquet | 410 | 99.7% | 232 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/BEKE.parquet | 391 | 98.5% | 349 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/BGC.parquet | 344 | 84.6% | 407 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 84.6% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/BILI.parquet | 406 | 89.5% | 543 | 0 | 0 | 0 |  | 56 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/BKKT.parquet | 341 | 77.7% | 608 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/BMEA.parquet | 269 | 61.5% | 643 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 61.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/BORR.parquet | 392 | 93.8% | 494 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/BTG.parquet | 447 | 99.5% | 484 | 0 | 0 | 0 |  | 58 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/BTGO.parquet | 371 | 90.8% | 576 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/CANG.parquet | 106 | 26.9% | 285 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 26.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/CHPT.parquet | 412 | 91.3% | 472 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/CIFR.parquet | 736 | 100.0% | 223 | 0 | 0 | 0 |  | 345 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/CMPS.parquet | 439 | 89.5% | 511 | 0 | 0 | 0 |  | 89 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/CORZ.parquet | 457 | 99.7% | 498 | 0 | 0 | 0 |  | 67 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/CTKB.parquet | 229 | 56.1% | 631 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 56.1% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/CTNM.parquet | 137 | 34.4% | 264 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 34.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/DDD.parquet | 361 | 89.5% | 226 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.5% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/DSP.parquet | 135 | 32.0% | 791 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 32.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/EC.parquet | 315 | 76.4% | 413 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/EMBC.parquet | 257 | 62.1% | 674 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 62.1% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/ENOV.parquet | 386 | 95.9% | 398 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 95.9% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/ENVX.parquet | 496 | 95.9% | 462 | 0 | 0 | 0 |  | 121 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/EQX.parquet | 451 | 99.7% | 507 | 0 | 0 | 0 |  | 61 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/EROC.parquet | 437 | 99.0% | 476 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/EVGO.parquet | 403 | 87.2% | 555 | 0 | 0 | 0 |  | 62 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/FDMT.parquet | 209 | 50.0% | 711 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/FEAM.parquet | 181 | 43.3% | 477 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 43.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/FIP.parquet | 255 | 64.1% | 346 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/FRVO.parquet | 562 | 99.7% | 395 | 0 | 0 | 0 |  | 172 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/FUBO.parquet | 348 | 82.8% | 574 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/GAU.parquet | 346 | 85.6% | 557 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/GEMI.parquet | 421 | 94.9% | 531 | 0 | 0 | 0 |  | 51 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/GORO.parquet | 324 | 74.9% | 623 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/GRPN.parquet | 304 | 73.6% | 460 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/HAFN.parquet | 387 | 86.7% | 502 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/HLF.parquet | 305 | 76.7% | 247 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/HLIT.parquet | 297 | 71.0% | 648 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  |  | RTH coverage 71.0% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/HYLN.parquet | 397 | 94.4% | 403 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/IAUX.parquet | 384 | 93.1% | 462 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/IRWD.parquet | 309 | 74.1% | 622 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  |  | RTH coverage 74.1% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/KC.parquet | 259 | 60.0% | 694 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 60.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/KLXE.parquet | 137 | 33.1% | 794 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 33.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/KPTI.parquet | 470 | 89.0% | 479 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/LBRT.parquet | 379 | 94.9% | 421 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 94.9% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/LI.parquet | 431 | 93.8% | 524 | 0 | 0 | 0 |  | 64 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/LVWR.parquet | 144 | 34.6% | 651 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 34.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/MBC.parquet | 388 | 99.0% | 5 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-11 |
| 2026-09-11/NAK.parquet | 427 | 98.7% | 513 | 0 | 0 | 0 |  | 42 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/NAT.parquet | 437 | 99.7% | 518 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/NEOG.parquet | 330 | 78.0% | 559 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.0% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/NEWP.parquet | 349 | 86.7% | 364 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/NIO.parquet | 750 | 100.0% | 210 | 0 | 0 | 0 |  | 359 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/NRGV.parquet | 381 | 94.6% | 266 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/NTSK.parquet | 437 | 100.0% | 521 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/NVAX.parquet | 501 | 99.5% | 459 | 0 | 0 | 0 |  | 112 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/NXH.parquet | 392 | 87.9% | 490 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/OCTV.parquet | 386 | 94.6% | 433 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/OPK.parquet | 344 | 77.2% | 536 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/OPTU.parquet | 307 | 78.2% | 234 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/PINS.parquet | 431 | 100.0% | 528 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/PLAY.parquet | 352 | 79.5% | 416 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  |  | RTH coverage 79.5% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/PTON.parquet | 412 | 95.6% | 548 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  |  | RTH coverage 95.6% < 98%; no daily bar for 2026-09-11 |
| 2026-09-11/PWP.parquet | 342 | 85.4% | 579 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/RBBN.parquet | 178 | 42.6% | 519 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 42.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/RC.parquet | 393 | 98.5% | 170 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-11 |
| 2026-09-11/RXRX.parquet | 611 | 98.7% | 348 | 0 | 0 | 0 |  | 225 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/SB.parquet | 325 | 82.8% | 67 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/SECZ.parquet | 358 | 79.0% | 567 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/SG.parquet | 407 | 99.5% | 335 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/SLI.parquet | 338 | 82.0% | 295 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/SOC.parquet | 419 | 98.0% | 468 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/SOFI.parquet | 866 | 100.0% | 94 | 0 | 0 | 0 |  | 475 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/STTK.parquet | 303 | 76.1% | 337 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/TDUP.parquet | 329 | 80.5% | 397 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/TGB.parquet | 411 | 97.4% | 403 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/THM.parquet | 243 | 59.7% | 305 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 59.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/TLRY.parquet | 480 | 96.2% | 479 | 0 | 0 | 0 |  | 104 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/TMC.parquet | 514 | 96.9% | 437 | 0 | 0 | 0 |  | 135 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/TRX.parquet | 386 | 89.7% | 568 | 0 | 0 | 0 |  | 35 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/USAS.parquet | 444 | 97.7% | 480 | 0 | 0 | 0 |  | 62 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/VISN.parquet | 378 | 92.8% | 553 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/VNET.parquet | 326 | 78.5% | 605 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/VZLA.parquet | 426 | 98.0% | 496 | 0 | 0 | 0 |  | 43 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-11/XRAY.parquet | 405 | 99.0% | 255 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/XXI.parquet | 416 | 98.7% | 505 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-11/ZH.parquet | 149 | 36.1% | 735 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 36.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/ABSI.parquet | 436 | 91.0% | 517 | 0 | 0 | 0 |  | 81 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/ACRS.parquet | 344 | 84.4% | 386 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/ADTN.parquet | 327 | 77.4% | 604 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  |  | RTH coverage 77.4% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/AESI.parquet | 393 | 97.7% | 147 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.7% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/AG.parquet | 638 | 100.0% | 319 | 0 | 0 | 0 |  | 247 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/ALKT.parquet | 336 | 80.5% | 413 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/AMRX.parquet | 322 | 78.5% | 403 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.5% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/ANGX.parquet | 428 | 94.4% | 525 | 0 | 0 | 0 |  | 59 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/ANNX.parquet | 382 | 92.6% | 450 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/APUS.parquet | 49 | 10.0% | 725 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 10.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/ARHS.parquet | 267 | 65.1% | 663 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/ARIS.parquet | 385 | 95.6% | 325 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/ASM.parquet | 437 | 97.2% | 515 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/AUTL.parquet | 276 | 66.4% | 500 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/BBWI.parquet | 403 | 100.0% | 460 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/BEKE.parquet | 399 | 97.7% | 363 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/BGC.parquet | 358 | 89.7% | 338 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.7% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/BILI.parquet | 398 | 89.5% | 557 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/BKKT.parquet | 359 | 80.3% | 597 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/BMEA.parquet | 233 | 54.4% | 706 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 54.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/BORR.parquet | 419 | 97.2% | 520 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/BTG.parquet | 466 | 99.5% | 494 | 0 | 0 | 0 |  | 77 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/BTGO.parquet | 365 | 87.7% | 576 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/CANG.parquet | 92 | 21.8% | 813 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 21.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/CHPT.parquet | 353 | 83.6% | 597 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/CIFR.parquet | 846 | 100.0% | 112 | 0 | 0 | 0 |  | 457 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/CMPS.parquet | 455 | 93.3% | 504 | 0 | 0 | 0 |  | 91 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/CORZ.parquet | 529 | 100.0% | 427 | 0 | 0 | 0 |  | 138 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/CTKB.parquet | 272 | 66.9% | 455 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 66.9% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/CTNM.parquet | 171 | 35.6% | 647 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 35.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/DDD.parquet | 371 | 91.0% | 310 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.0% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/DSP.parquet | 136 | 32.3% | 787 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 32.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/EC.parquet | 338 | 84.9% | 421 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/EMBC.parquet | 282 | 70.3% | 443 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 70.3% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/ENOV.parquet | 397 | 96.9% | 424 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.9% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/ENVX.parquet | 522 | 98.2% | 436 | 0 | 0 | 0 |  | 138 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/EQX.parquet | 468 | 99.5% | 453 | 0 | 0 | 0 |  | 79 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/EROC.parquet | 449 | 99.0% | 498 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/EVGO.parquet | 393 | 87.7% | 543 | 0 | 0 | 0 |  | 52 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/FDMT.parquet | 342 | 78.5% | 469 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/FEAM.parquet | 209 | 49.2% | 747 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 49.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/FIP.parquet | 347 | 86.9% | 584 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/FRVO.parquet | 564 | 99.0% | 395 | 0 | 0 | 0 |  | 177 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/FUBO.parquet | 370 | 89.5% | 563 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/GAU.parquet | 322 | 79.0% | 399 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/GEMI.parquet | 479 | 93.3% | 478 | 0 | 0 | 0 |  | 116 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/GORO.parquet | 387 | 89.2% | 525 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/GRPN.parquet | 273 | 65.1% | 686 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/HAFN.parquet | 393 | 88.7% | 551 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/HLF.parquet | 306 | 76.7% | 465 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/HLIT.parquet | 346 | 81.0% | 595 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  |  | RTH coverage 81.0% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/HYLN.parquet | 409 | 94.9% | 528 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/IAUX.parquet | 407 | 99.7% | 319 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/IRWD.parquet | 303 | 73.9% | 448 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 73.9% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/KC.parquet | 305 | 72.8% | 651 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/KLXE.parquet | 168 | 40.5% | 452 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 40.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/KPTI.parquet | 208 | 45.6% | 723 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 45.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/LBRT.parquet | 396 | 97.4% | 370 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.4% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/LI.parquet | 419 | 94.6% | 530 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/LVWR.parquet | 191 | 46.4% | 444 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 46.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/MBC.parquet | 390 | 96.7% | 331 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.7% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/NAK.parquet | 439 | 100.0% | 492 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/NAT.parquet | 435 | 99.7% | 510 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/NEOG.parquet | 394 | 94.9% | 344 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  |  | RTH coverage 94.9% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/NEWP.parquet | 400 | 99.0% | 391 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/NIO.parquet | 770 | 100.0% | 190 | 0 | 0 | 0 |  | 379 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/NRGV.parquet | 416 | 98.0% | 390 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/NTSK.parquet | 530 | 100.0% | 430 | 0 | 0 | 0 |  | 139 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/NVAX.parquet | 455 | 96.9% | 504 | 0 | 0 | 0 |  | 76 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/NXH.parquet | 353 | 79.5% | 506 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/OCTV.parquet | 392 | 93.1% | 520 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/OPK.parquet | 361 | 81.3% | 594 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/OPTU.parquet | 353 | 89.5% | 119 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/PINS.parquet | 449 | 99.7% | 490 | 0 | 0 | 0 |  | 59 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/PLAY.parquet | 676 | 98.7% | 284 | 0 | 0 | 0 |  | 291 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-14 |
| 2026-09-14/PTON.parquet | 402 | 92.6% | 558 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.6% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/PWP.parquet | 297 | 72.8% | 631 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/RBBN.parquet | 184 | 44.6% | 717 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 44.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/RC.parquet | 308 | 77.2% | 440 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | RTH coverage 77.2% < 98%; no daily bar for 2026-09-14 |
| 2026-09-14/RXRX.parquet | 670 | 100.0% | 287 | 0 | 0 | 0 |  | 279 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/SB.parquet | 345 | 78.5% | 377 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/SECZ.parquet | 369 | 84.4% | 561 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/SG.parquet | 403 | 99.2% | 513 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/SLI.parquet | 362 | 89.0% | 301 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/SOC.parquet | 445 | 100.0% | 515 | 0 | 0 | 0 |  | 54 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/SOFI.parquet | 916 | 100.0% | 44 | 0 | 0 | 0 |  | 525 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/STTK.parquet | 280 | 70.0% | 385 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/TDUP.parquet | 339 | 80.3% | 602 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/TGB.parquet | 418 | 98.7% | 515 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/THM.parquet | 291 | 72.0% | 342 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/TLRY.parquet | 524 | 95.4% | 426 | 0 | 0 | 0 |  | 151 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/TMC.parquet | 535 | 98.7% | 425 | 0 | 0 | 0 |  | 150 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/TRX.parquet | 465 | 99.2% | 495 | 0 | 0 | 0 |  | 77 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/USAS.parquet | 454 | 97.7% | 488 | 0 | 0 | 0 |  | 72 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/VISN.parquet | 414 | 99.0% | 331 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/VNET.parquet | 338 | 81.0% | 622 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/VZLA.parquet | 409 | 94.6% | 480 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/XRAY.parquet | 371 | 91.8% | 316 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-14/XXI.parquet | 424 | 98.5% | 527 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-14/ZH.parquet | 148 | 36.4% | 635 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 36.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/AAL.parquet | 652 | 100.0% | 307 | 0 | 0 | 0 |  | 262 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/ABSI.parquet | 419 | 94.9% | 521 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ACRS.parquet | 339 | 83.3% | 400 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ADCT.parquet | 331 | 82.6% | 394 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ADTN.parquet | 272 | 67.4% | 348 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 67.4% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/AESI.parquet | 390 | 98.0% | 345 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 98.0% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/AG.parquet | 512 | 100.0% | 448 | 0 | 0 | 0 |  | 121 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/AI.parquet | 450 | 99.5% | 510 | 0 | 0 | 0 |  | 61 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/ALKT.parquet | 334 | 82.6% | 617 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/AMC.parquet | 555 | 100.0% | 404 | 0 | 0 | 0 |  | 164 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/AMRX.parquet | 331 | 79.0% | 490 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  |  | RTH coverage 79.0% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/ANGX.parquet | 384 | 94.9% | 560 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ANNX.parquet | 385 | 94.1% | 546 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/APUS.parquet | 79 | 16.2% | 693 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 16.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ARHS.parquet | 287 | 71.8% | 629 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ARIS.parquet | 389 | 92.8% | 360 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ASM.parquet | 414 | 98.0% | 468 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/AUTL.parquet | 195 | 44.9% | 714 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 44.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BB.parquet | 469 | 99.5% | 489 | 0 | 0 | 0 |  | 80 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/BBAI.parquet | 512 | 100.0% | 448 | 0 | 0 | 0 |  | 121 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/BBWI.parquet | 417 | 100.0% | 525 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/BEKE.parquet | 389 | 98.0% | 368 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BFLY.parquet | 434 | 99.7% | 523 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/BGC.parquet | 368 | 92.0% | 233 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.0% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/BHVN.parquet | 385 | 95.9% | 386 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BILI.parquet | 371 | 83.9% | 568 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BKKT.parquet | 409 | 92.3% | 547 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BLMN.parquet | 384 | 93.3% | 311 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.3% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/BLND.parquet | 380 | 94.9% | 244 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BMEA.parquet | 268 | 63.1% | 552 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BORR.parquet | 410 | 94.9% | 540 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BTG.parquet | 434 | 99.2% | 510 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/BTGO.parquet | 394 | 93.6% | 542 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/BYND.parquet | 386 | 80.3% | 570 | 0 | 0 | 0 |  | 74 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/CANG.parquet | 331 | 75.6% | 508 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/CHPT.parquet | 332 | 76.4% | 621 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/CIFR.parquet | 738 | 100.0% | 222 | 0 | 0 | 0 |  | 347 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/CMPS.parquet | 465 | 94.6% | 490 | 0 | 0 | 0 |  | 95 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/CORZ.parquet | 488 | 100.0% | 468 | 0 | 0 | 0 |  | 97 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/COTY.parquet | 394 | 99.7% | 207 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-15 |
| 2026-09-15/CTKB.parquet | 271 | 66.9% | 660 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 66.9% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/CTNM.parquet | 267 | 67.2% | 339 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 67.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/CWK.parquet | 309 | 78.5% | 87 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.5% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/DC.parquet | 351 | 89.2% | 371 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/DDD.parquet | 378 | 93.3% | 581 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.3% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/DSP.parquet | 98 | 23.1% | 503 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 23.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/EC.parquet | 348 | 87.9% | 381 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/EDIT.parquet | 353 | 83.6% | 593 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/EGHT.parquet | 287 | 70.5% | 644 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 70.5% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/ELME.parquet | 191 | 48.5% | 201 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  |  | RTH coverage 48.5% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/EMBC.parquet | 267 | 66.4% | 431 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 66.4% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/ENOV.parquet | 397 | 98.2% | 418 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-15 |
| 2026-09-15/ENVX.parquet | 487 | 97.7% | 464 | 0 | 0 | 0 |  | 106 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/EQX.parquet | 457 | 100.0% | 490 | 0 | 0 | 0 |  | 66 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/EROC.parquet | 408 | 95.4% | 494 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/ESRT.parquet | 389 | 99.0% | 333 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/EVGO.parquet | 394 | 91.5% | 523 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/FDMT.parquet | 205 | 50.8% | 461 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/FEAM.parquet | 193 | 45.9% | 738 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 45.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/FIP.parquet | 392 | 97.2% | 359 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/FJET.parquet | 400 | 96.9% | 298 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/FRVO.parquet | 522 | 99.0% | 430 | 0 | 0 | 0 |  | 136 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/FUBO.parquet | 381 | 94.1% | 450 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/GAU.parquet | 325 | 80.8% | 467 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/GCTS.parquet | 413 | 91.0% | 525 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/GEMI.parquet | 449 | 90.8% | 511 | 0 | 0 | 0 |  | 95 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/GOGO.parquet | 303 | 74.6% | 630 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 74.6% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/GORO.parquet | 354 | 82.8% | 593 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/GRAB.parquet | 853 | 100.0% | 107 | 0 | 0 | 0 |  | 462 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/GRPN.parquet | 251 | 61.0% | 500 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 61.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/GTN.parquet | 291 | 74.4% | 100 | 0 | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/HAFN.parquet | 389 | 90.0% | 563 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/HIMX.parquet | 404 | 96.9% | 546 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/HLF.parquet | 284 | 70.8% | 480 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/HLIT.parquet | 369 | 90.8% | 562 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 90.8% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/HSAI.parquet | 339 | 80.8% | 592 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/HUYA.parquet | 370 | 94.1% | 105 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/HYLN.parquet | 384 | 93.6% | 567 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/IAUX.parquet | 392 | 97.4% | 249 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/IE.parquet | 390 | 94.4% | 470 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/IMSR.parquet | 392 | 88.2% | 566 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/INFQ.parquet | 524 | 100.0% | 436 | 0 | 0 | 0 |  | 133 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/INTR.parquet | 350 | 85.9% | 295 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/IRWD.parquet | 309 | 74.9% | 493 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  |  | RTH coverage 74.9% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/JBLU.parquet | 531 | 100.0% | 429 | 0 | 0 | 0 |  | 141 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-15 |
| 2026-09-15/JOBY.parquet | 711 | 100.0% | 248 | 0 | 0 | 0 |  | 320 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/KC.parquet | 333 | 79.2% | 598 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/KLXE.parquet | 89 | 21.3% | 588 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 21.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/KPTI.parquet | 278 | 65.9% | 645 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/KSS.parquet | 407 | 100.0% | 412 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-15 |
| 2026-09-15/LAC.parquet | 505 | 99.7% | 455 | 0 | 0 | 0 |  | 115 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/LAES.parquet | 781 | 95.9% | 179 | 0 | 0 | 0 |  | 408 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/LBRT.parquet | 390 | 98.0% | 167 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 98.0% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/LCID.parquet | 648 | 100.0% | 312 | 0 | 0 | 0 |  | 257 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/LEGN.parquet | 420 | 96.4% | 511 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/LI.parquet | 438 | 93.1% | 521 | 0 | 0 | 0 |  | 74 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/LILAK.parquet | 265 | 66.9% | 136 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/LION.parquet | 389 | 98.7% | 204 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/LPL.parquet | 290 | 71.8% | 618 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/LVWR.parquet | 105 | 24.6% | 663 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 24.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/MBC.parquet | 411 | 99.7% | 311 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-15 |
| 2026-09-15/MNRO.parquet | 300 | 75.4% | 301 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  |  | RTH coverage 75.4% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/MNSO.parquet | 292 | 69.7% | 650 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/MPT.parquet | 416 | 100.0% | 538 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-15 |
| 2026-09-15/MX.parquet | 174 | 41.5% | 745 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 41.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/NAK.parquet | 451 | 98.7% | 507 | 0 | 0 | 0 |  | 66 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/NAT.parquet | 427 | 99.7% | 523 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/NEOG.parquet | 370 | 91.0% | 483 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.0% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/NEWP.parquet | 386 | 97.4% | 205 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/NIO.parquet | 651 | 100.0% | 309 | 0 | 0 | 0 |  | 260 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/NMAX.parquet | 349 | 87.9% | 398 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/NNVC.parquet | 268 | 65.1% | 428 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/NRGV.parquet | 396 | 98.5% | 163 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/NTSK.parquet | 501 | 100.0% | 459 | 0 | 0 | 0 |  | 110 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/NUVB.parquet | 415 | 99.5% | 425 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/NVAX.parquet | 433 | 96.4% | 521 | 0 | 0 | 0 |  | 56 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/NXDR.parquet | 384 | 96.7% | 226 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/NXE.parquet | 410 | 97.4% | 542 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/NXH.parquet | 374 | 84.9% | 342 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/OCTV.parquet | 363 | 85.9% | 568 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/OPEN.parquet | 723 | 100.0% | 237 | 0 | 0 | 0 |  | 332 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/OPK.parquet | 355 | 78.2% | 590 | 0 | 0 | 0 |  | 51 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/OPTU.parquet | 333 | 84.6% | 499 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/PAX.parquet | 265 | 66.4% | 531 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/PD.parquet | 353 | 89.5% | 121 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/PINS.parquet | 440 | 100.0% | 519 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/PL.parquet | 542 | 100.0% | 418 | 0 | 0 | 0 |  | 151 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/PLAY.parquet | 702 | 99.7% | 258 | 0 | 0 | 0 |  | 312 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-15 |
| 2026-09-15/PLTK.parquet | 232 | 57.4% | 519 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 57.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/PRGO.parquet | 347 | 86.2% | 548 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 86.2% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/PTON.parquet | 438 | 97.2% | 522 | 0 | 0 | 0 |  | 58 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.2% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/PWP.parquet | 323 | 81.0% | 525 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/QBTS.parquet | 720 | 100.0% | 240 | 0 | 0 | 0 |  | 329 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/QXO.parquet | 515 | 100.0% | 445 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/RBBN.parquet | 272 | 66.9% | 461 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/RC.parquet | 386 | 97.4% | 100 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.4% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/RDW.parquet | 562 | 100.0% | 388 | 0 | 0 | 0 |  | 171 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/RXRX.parquet | 588 | 99.7% | 372 | 0 | 0 | 0 |  | 198 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/RXT.parquet | 588 | 99.2% | 351 | 0 | 0 | 0 |  | 200 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/SB.parquet | 406 | 97.7% | 464 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/SECZ.parquet | 381 | 87.7% | 464 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/SG.parquet | 407 | 99.7% | 513 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/SHEN.parquet | 214 | 52.6% | 387 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 52.6% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/SID.parquet | 342 | 83.6% | 458 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/SLI.parquet | 390 | 94.6% | 367 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/SMR.parquet | 678 | 100.0% | 281 | 0 | 0 | 0 |  | 286 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/SOC.parquet | 414 | 98.7% | 493 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/SOFI.parquet | 875 | 100.0% | 85 | 0 | 0 | 0 |  | 484 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/SONO.parquet | 328 | 82.0% | 273 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 82.0% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/SPCE.parquet | 454 | 98.5% | 506 | 0 | 0 | 0 |  | 69 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/SPRU.parquet | 129 | 19.7% | 677 | 0 | 0 | 0 |  | 52 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 19.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/SRAD.parquet | 347 | 85.6% | 399 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/STKE.parquet | 101 | 21.3% | 841 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 21.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/STTK.parquet | 256 | 63.8% | 378 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/TDUP.parquet | 382 | 89.7% | 527 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/TE.parquet | 580 | 100.0% | 380 | 0 | 0 | 0 |  | 189 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/TGB.parquet | 406 | 97.2% | 505 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/THM.parquet | 307 | 76.1% | 274 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/TIGR.parquet | 355 | 83.3% | 576 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/TLRY.parquet | 462 | 91.3% | 495 | 0 | 0 | 0 |  | 108 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/TMC.parquet | 502 | 95.9% | 455 | 0 | 0 | 0 |  | 128 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/TME.parquet | 408 | 99.2% | 423 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/TRLV.parquet | 375 | 94.6% | 325 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/TRX.parquet | 442 | 98.7% | 505 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/TV.parquet | 357 | 91.0% | 35 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/UAMY.parquet | 464 | 99.2% | 493 | 0 | 0 | 0 |  | 77 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/ULCC.parquet | 373 | 93.1% | 378 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/URG.parquet | 442 | 99.0% | 503 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/USAS.parquet | 423 | 96.9% | 508 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/UUUU.parquet | 514 | 100.0% | 446 | 0 | 0 | 0 |  | 123 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/VGZ.parquet | 368 | 90.5% | 378 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/VISN.parquet | 397 | 96.9% | 533 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/VNET.parquet | 357 | 88.2% | 535 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/VYX.parquet | 398 | 96.7% | 366 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.7% < 98%; no daily bar for 2026-09-15 |
| 2026-09-15/VZLA.parquet | 402 | 97.7% | 349 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/XE.parquet | 617 | 99.7% | 343 | 0 | 0 | 0 |  | 227 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/XERS.parquet | 306 | 75.6% | 450 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/XRAY.parquet | 415 | 99.0% | 220 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/XXI.parquet | 431 | 97.7% | 496 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-15/YSS.parquet | 407 | 98.7% | 548 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-15/ZH.parquet | 189 | 47.4% | 531 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 47.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/AAL.parquet | 721 | 100.0% | 239 | 0 | 0 | 0 |  | 330 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/ABSI.parquet | 421 | 96.2% | 510 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ACHR.parquet | 673 | 100.0% | 287 | 0 | 0 | 0 |  | 282 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/ACRS.parquet | 337 | 84.1% | 270 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ADCT.parquet | 353 | 88.5% | 260 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ADTN.parquet | 290 | 71.0% | 367 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  |  | RTH coverage 71.0% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/AESI.parquet | 373 | 93.1% | 484 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.1% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/AG.parquet | 645 | 100.0% | 311 | 0 | 0 | 0 |  | 254 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/AI.parquet | 463 | 99.7% | 497 | 0 | 0 | 0 |  | 73 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/ALEC.parquet | 187 | 46.9% | 414 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 46.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ALKT.parquet | 314 | 77.4% | 437 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/AMC.parquet | 661 | 100.0% | 299 | 0 | 0 | 0 |  | 270 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/AMPX.parquet | 493 | 99.5% | 464 | 0 | 0 | 0 |  | 104 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/AMRX.parquet | 393 | 96.2% | 298 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.2% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/ANGX.parquet | 348 | 82.6% | 578 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ANNX.parquet | 360 | 87.7% | 571 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ANVS.parquet | 384 | 92.0% | 532 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/APUS.parquet | 58 | 12.3% | 697 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 12.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ARHS.parquet | 299 | 74.4% | 391 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ARIS.parquet | 417 | 94.1% | 465 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ASM.parquet | 448 | 98.0% | 475 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ASPN.parquet | 324 | 81.5% | 277 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/AUTL.parquet | 296 | 72.6% | 455 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BB.parquet | 524 | 99.5% | 435 | 0 | 0 | 0 |  | 135 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/BBAI.parquet | 640 | 100.0% | 320 | 0 | 0 | 0 |  | 249 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/BBWI.parquet | 427 | 99.7% | 533 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/BEKE.parquet | 396 | 97.7% | 557 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BFLY.parquet | 452 | 99.7% | 503 | 0 | 0 | 0 |  | 62 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/BGC.parquet | 358 | 87.9% | 361 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.9% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/BGS.parquet | 372 | 90.3% | 379 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  |  | RTH coverage 90.3% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/BHVN.parquet | 397 | 98.0% | 454 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BILI.parquet | 477 | 98.5% | 476 | 0 | 0 | 0 |  | 92 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/BIOA.parquet | 282 | 68.2% | 649 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BKKT.parquet | 427 | 94.6% | 530 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BLMN.parquet | 362 | 89.0% | 506 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.0% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/BLND.parquet | 377 | 93.3% | 578 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BMEA.parquet | 272 | 62.3% | 495 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 62.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BOBS.parquet | 332 | 82.6% | 621 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BORR.parquet | 418 | 95.4% | 542 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BTG.parquet | 489 | 99.5% | 471 | 0 | 0 | 0 |  | 100 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/BTGO.parquet | 452 | 98.2% | 504 | 0 | 0 | 0 |  | 69 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/BUR.parquet | 379 | 91.8% | 563 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/BYND.parquet | 449 | 90.0% | 511 | 0 | 0 | 0 |  | 97 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CANG.parquet | 286 | 65.1% | 668 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CAPR.parquet | 432 | 93.1% | 526 | 0 | 0 | 0 |  | 69 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CERT.parquet | 380 | 93.8% | 251 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.8% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/CHPT.parquet | 361 | 82.6% | 560 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CIFR.parquet | 780 | 100.0% | 180 | 0 | 0 | 0 |  | 389 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/CLF.parquet | 439 | 100.0% | 518 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/CMPS.parquet | 429 | 91.5% | 527 | 0 | 0 | 0 |  | 72 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CORZ.parquet | 501 | 100.0% | 457 | 0 | 0 | 0 |  | 110 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/COTY.parquet | 401 | 99.2% | 410 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/CPRI.parquet | 409 | 100.0% | 278 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/CTKB.parquet | 310 | 77.4% | 554 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 77.4% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/CTMX.parquet | 406 | 95.9% | 525 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CTNM.parquet | 307 | 77.4% | 294 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CWH.parquet | 387 | 94.4% | 296 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/CWK.parquet | 349 | 88.2% | 252 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  |  | RTH coverage 88.2% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/DC.parquet | 299 | 74.4% | 302 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/DDD.parquet | 367 | 90.5% | 393 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 90.5% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/DFH.parquet | 293 | 72.6% | 361 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 72.6% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/DNA.parquet | 346 | 80.3% | 610 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/DSP.parquet | 190 | 36.9% | 430 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 36.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/EAF.parquet | 298 | 71.3% | 359 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/EC.parquet | 402 | 98.7% | 371 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/EDIT.parquet | 379 | 91.3% | 552 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/EGHT.parquet | 281 | 70.3% | 650 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 70.3% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/ELME.parquet | 240 | 60.3% | 361 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  |  | RTH coverage 60.3% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/EMBC.parquet | 252 | 62.6% | 349 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 62.6% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/ENOV.parquet | 373 | 93.8% | 311 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.8% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/ENVX.parquet | 507 | 99.5% | 451 | 0 | 0 | 0 |  | 119 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/EQX.parquet | 493 | 99.7% | 467 | 0 | 0 | 0 |  | 103 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/EROC.parquet | 450 | 97.2% | 504 | 0 | 0 | 0 |  | 70 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ESRT.parquet | 401 | 99.5% | 200 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/EVGO.parquet | 390 | 91.5% | 382 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/EXK.parquet | 480 | 99.2% | 480 | 0 | 0 | 0 |  | 92 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/FDMT.parquet | 276 | 68.7% | 636 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/FEAM.parquet | 394 | 65.4% | 362 | 0 | 0 | 0 |  | 139 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/FIP.parquet | 297 | 73.9% | 574 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/FJET.parquet | 414 | 96.7% | 304 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/FOSL.parquet | 242 | 59.7% | 359 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 59.7% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/FRVO.parquet | 523 | 100.0% | 437 | 0 | 0 | 0 |  | 133 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/FSM.parquet | 422 | 97.7% | 502 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/FUBO.parquet | 345 | 79.2% | 603 | 0 | 0 | 0 |  | 35 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/GAU.parquet | 335 | 80.8% | 428 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/GCTS.parquet | 429 | 87.4% | 525 | 0 | 0 | 0 |  | 87 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/GEMI.parquet | 447 | 91.3% | 508 | 0 | 0 | 0 |  | 92 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/GENI.parquet | 401 | 99.0% | 540 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/GOGO.parquet | 317 | 78.5% | 363 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.5% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/GORO.parquet | 391 | 88.2% | 567 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/GRAB.parquet | 857 | 100.0% | 103 | 0 | 0 | 0 |  | 466 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/GRPN.parquet | 291 | 71.8% | 335 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/GT.parquet | 457 | 100.0% | 484 | 0 | 0 | 0 |  | 66 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/GTN.parquet | 267 | 67.2% | 416 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 67.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HAFN.parquet | 418 | 94.6% | 539 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HIMX.parquet | 333 | 74.9% | 573 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HL.parquet | 568 | 100.0% | 391 | 0 | 0 | 0 |  | 177 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/HLF.parquet | 331 | 83.6% | 270 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HLIT.parquet | 346 | 83.3% | 450 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  |  | RTH coverage 83.3% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/HLLY.parquet | 325 | 81.8% | 276 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HMY.parquet | 471 | 94.6% | 471 | 0 | 0 | 0 |  | 101 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HSAI.parquet | 351 | 83.1% | 580 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HUYA.parquet | 348 | 87.2% | 390 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/HYLN.parquet | 389 | 91.5% | 571 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/IAUX.parquet | 416 | 97.7% | 517 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/IBRX.parquet | 534 | 99.7% | 420 | 0 | 0 | 0 |  | 144 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/IE.parquet | 389 | 94.6% | 369 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/IMSR.parquet | 385 | 84.9% | 573 | 0 | 0 | 0 |  | 53 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/INFQ.parquet | 570 | 99.7% | 390 | 0 | 0 | 0 |  | 180 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/INTR.parquet | 357 | 86.2% | 426 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/IRWD.parquet | 335 | 82.8% | 468 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  |  | RTH coverage 82.8% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/ITRG.parquet | 286 | 69.0% | 389 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/JBLU.parquet | 523 | 99.7% | 433 | 0 | 0 | 0 |  | 133 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/JELD.parquet | 276 | 67.2% | 429 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 67.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/JOBY.parquet | 731 | 100.0% | 229 | 0 | 0 | 0 |  | 340 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/KC.parquet | 293 | 69.7% | 645 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/KLRA.parquet | 343 | 83.9% | 408 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/KLXE.parquet | 93 | 21.3% | 855 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 21.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/KPTI.parquet | 326 | 78.0% | 491 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/KRO.parquet | 225 | 55.9% | 396 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 55.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/KSS.parquet | 394 | 96.9% | 332 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.9% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/LAC.parquet | 570 | 99.5% | 390 | 0 | 0 | 0 |  | 181 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/LAES.parquet | 747 | 98.0% | 213 | 0 | 0 | 0 |  | 367 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/LBRT.parquet | 384 | 95.9% | 308 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 95.9% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/LCID.parquet | 670 | 99.5% | 290 | 0 | 0 | 0 |  | 281 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/LEGN.parquet | 420 | 97.7% | 535 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/LI.parquet | 458 | 96.2% | 473 | 0 | 0 | 0 |  | 82 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/LILAK.parquet | 281 | 70.5% | 320 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/LION.parquet | 379 | 94.9% | 244 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/LODE.parquet | 327 | 79.0% | 383 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/LPL.parquet | 336 | 79.7% | 623 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/LVWR.parquet | 325 | 77.7% | 626 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/MBC.parquet | 391 | 98.5% | 218 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/MNRO.parquet | 300 | 72.3% | 631 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 72.3% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/MNSO.parquet | 306 | 74.1% | 625 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/MPT.parquet | 490 | 99.5% | 313 | 0 | 0 | 0 |  | 101 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/MRVI.parquet | 341 | 83.6% | 590 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/MX.parquet | 256 | 59.2% | 696 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 59.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NABL.parquet | 395 | 99.0% | 227 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/NAK.parquet | 446 | 91.8% | 507 | 0 | 0 | 0 |  | 87 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NAT.parquet | 441 | 98.7% | 518 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/NEOG.parquet | 383 | 92.3% | 498 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.3% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/NEWP.parquet | 377 | 93.8% | 486 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NG.parquet | 459 | 99.7% | 497 | 0 | 0 | 0 |  | 69 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/NIO.parquet | 732 | 100.0% | 228 | 0 | 0 | 0 |  | 341 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/NMAX.parquet | 347 | 84.6% | 303 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NNVC.parquet | 345 | 67.2% | 443 | 0 | 0 | 0 |  | 82 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 67.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NRGV.parquet | 400 | 94.6% | 356 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NTSK.parquet | 462 | 99.7% | 497 | 0 | 0 | 0 |  | 72 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/NUVB.parquet | 399 | 96.7% | 552 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NVAX.parquet | 432 | 95.1% | 522 | 0 | 0 | 0 |  | 60 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/NXDR.parquet | 426 | 98.5% | 529 | 0 | 0 | 0 |  | 42 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/NXE.parquet | 423 | 98.5% | 522 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/NXH.parquet | 312 | 72.0% | 509 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/OCTV.parquet | 383 | 91.5% | 539 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/OGG.parquet | 364 | 89.2% | 251 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/OPEN.parquet | 722 | 100.0% | 238 | 0 | 0 | 0 |  | 331 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/OPK.parquet | 310 | 69.2% | 456 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/OPTU.parquet | 364 | 91.0% | 238 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/ORIC.parquet | 321 | 80.0% | 587 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PAAI.parquet | 79 | 16.9% | 635 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 16.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PACB.parquet | 380 | 90.8% | 551 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PAX.parquet | 279 | 68.7% | 472 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PD.parquet | 318 | 78.2% | 304 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PHAT.parquet | 371 | 81.0% | 316 | 0 | 0 | 0 |  | 54 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PINS.parquet | 425 | 100.0% | 497 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/PL.parquet | 606 | 99.7% | 354 | 0 | 0 | 0 |  | 216 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/PLAY.parquet | 527 | 99.2% | 433 | 0 | 0 | 0 |  | 139 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/PLTK.parquet | 258 | 64.4% | 343 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PONY.parquet | 428 | 92.3% | 518 | 0 | 0 | 0 |  | 67 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/PRGO.parquet | 373 | 92.0% | 318 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.0% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/PTON.parquet | 434 | 98.7% | 509 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/PWP.parquet | 320 | 80.3% | 283 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/QBTS.parquet | 771 | 100.0% | 189 | 0 | 0 | 0 |  | 380 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/QXO.parquet | 504 | 100.0% | 455 | 0 | 0 | 0 |  | 113 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/RARE.parquet | 496 | 99.7% | 464 | 0 | 0 | 0 |  | 106 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/RBBN.parquet | 277 | 65.6% | 621 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/RC.parquet | 372 | 91.8% | 477 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.8% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/RDW.parquet | 643 | 100.0% | 317 | 0 | 0 | 0 |  | 252 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/REPL.parquet | 384 | 93.3% | 547 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/RSKD.parquet | 288 | 72.6% | 313 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/RXRX.parquet | 586 | 100.0% | 372 | 0 | 0 | 0 |  | 195 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/RXT.parquet | 540 | 98.7% | 420 | 0 | 0 | 0 |  | 154 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/RYAM.parquet | 256 | 64.6% | 345 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  |  | RTH coverage 64.6% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/SANA.parquet | 396 | 89.0% | 472 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SB.parquet | 413 | 97.4% | 528 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SBH.parquet | 360 | 85.4% | 591 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  |  | RTH coverage 85.4% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/SDEV.parquet | 171 | 31.3% | 780 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 31.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SECZ.parquet | 436 | 97.4% | 520 | 0 | 0 | 0 |  | 56 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SFIX.parquet | 308 | 75.1% | 576 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SG.parquet | 410 | 100.0% | 353 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/SGRY.parquet | 314 | 76.9% | 430 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SHEN.parquet | 319 | 79.2% | 448 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 79.2% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/SID.parquet | 364 | 90.3% | 298 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SLDB.parquet | 380 | 92.0% | 538 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SLI.parquet | 389 | 92.6% | 379 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SMJF.parquet | 165 | 32.0% | 770 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 32.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SMR.parquet | 760 | 100.0% | 200 | 0 | 0 | 0 |  | 368 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/SOC.parquet | 429 | 99.5% | 503 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/SOFI.parquet | 863 | 100.0% | 97 | 0 | 0 | 0 |  | 472 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/SONO.parquet | 351 | 86.4% | 530 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 86.4% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/SPCE.parquet | 470 | 99.2% | 488 | 0 | 0 | 0 |  | 82 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/SPRO.parquet | 153 | 37.4% | 517 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 37.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SPRU.parquet | 189 | 38.7% | 731 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 38.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SRAD.parquet | 347 | 85.1% | 425 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/STKE.parquet | 59 | 12.0% | 700 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 12.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/STTK.parquet | 233 | 58.2% | 368 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 58.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/SVM.parquet | 396 | 92.6% | 552 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/TDUP.parquet | 342 | 81.3% | 611 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/TE.parquet | 697 | 100.0% | 263 | 0 | 0 | 0 |  | 306 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/TGB.parquet | 419 | 98.7% | 532 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/THM.parquet | 318 | 79.0% | 381 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/TIGR.parquet | 399 | 92.6% | 545 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/TLRY.parquet | 485 | 94.6% | 475 | 0 | 0 | 0 |  | 116 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/TMC.parquet | 567 | 98.7% | 393 | 0 | 0 | 0 |  | 182 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/TME.parquet | 427 | 99.5% | 529 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/TRLV.parquet | 363 | 88.5% | 366 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/TRX.parquet | 439 | 97.4% | 521 | 0 | 0 | 0 |  | 59 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/TV.parquet | 208 | 50.5% | 419 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/UAMY.parquet | 501 | 99.2% | 459 | 0 | 0 | 0 |  | 113 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/ULCC.parquet | 351 | 86.2% | 513 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/URG.parquet | 474 | 99.5% | 482 | 0 | 0 | 0 |  | 85 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/USAS.parquet | 436 | 98.2% | 522 | 0 | 0 | 0 |  | 52 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/UUUU.parquet | 581 | 100.0% | 378 | 0 | 0 | 0 |  | 190 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/VFC.parquet | 409 | 100.0% | 248 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-16 |
| 2026-09-16/VGZ.parquet | 345 | 86.7% | 281 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/VIR.parquet | 343 | 85.4% | 588 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 85.4% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/VISN.parquet | 394 | 96.7% | 331 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/VLN.parquet | 268 | 63.8% | 493 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/VNET.parquet | 336 | 80.3% | 598 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/VYX.parquet | 424 | 96.7% | 530 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.7% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/VZLA.parquet | 404 | 93.6% | 455 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/WRN.parquet | 345 | 85.4% | 365 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/XE.parquet | 663 | 100.0% | 297 | 0 | 0 | 0 |  | 272 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/XERS.parquet | 324 | 78.5% | 377 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/XRAY.parquet | 407 | 99.0% | 536 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/XRX.parquet | 380 | 87.2% | 568 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.2% < 98%; no daily bar for 2026-09-16 |
| 2026-09-16/XXI.parquet | 412 | 96.9% | 362 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-16/YSS.parquet | 416 | 99.0% | 541 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-16/ZH.parquet | 201 | 48.5% | 685 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 48.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/AAL.parquet | 719 | 100.0% | 240 | 0 | 0 | 0 |  | 328 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/ABSI.parquet | 482 | 99.5% | 477 | 0 | 0 | 0 |  | 93 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/ACHR.parquet | 796 | 100.0% | 164 | 0 | 0 | 0 |  | 405 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/ACRS.parquet | 365 | 91.0% | 345 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ADCT.parquet | 345 | 80.3% | 586 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ADTN.parquet | 324 | 78.5% | 393 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.5% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/AESI.parquet | 378 | 92.0% | 553 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.0% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/AG.parquet | 684 | 100.0% | 276 | 0 | 0 | 0 |  | 293 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/AI.parquet | 525 | 96.7% | 435 | 0 | 0 | 0 |  | 147 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ALEC.parquet | 208 | 52.0% | 393 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 52.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ALKT.parquet | 266 | 65.6% | 348 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/AMC.parquet | 770 | 99.5% | 190 | 0 | 0 | 0 |  | 381 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/AMPX.parquet | 582 | 99.7% | 375 | 0 | 0 | 0 |  | 192 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/AMRX.parquet | 370 | 87.9% | 569 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.9% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/ANGX.parquet | 473 | 96.7% | 484 | 0 | 0 | 0 |  | 95 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ANNX.parquet | 355 | 86.7% | 386 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ANVS.parquet | 398 | 92.0% | 533 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/APUS.parquet | 89 | 15.1% | 868 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 15.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ARHS.parquet | 312 | 78.0% | 291 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ARIS.parquet | 460 | 95.4% | 471 | 0 | 0 | 0 |  | 87 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ASM.parquet | 501 | 95.6% | 455 | 0 | 0 | 0 |  | 127 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ASPN.parquet | 356 | 82.3% | 590 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/AUTL.parquet | 246 | 58.2% | 425 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 58.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BB.parquet | 674 | 99.7% | 286 | 0 | 0 | 0 |  | 284 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BBAI.parquet | 748 | 100.0% | 212 | 0 | 0 | 0 |  | 357 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BBWI.parquet | 453 | 99.7% | 478 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BEKE.parquet | 425 | 99.7% | 526 | 0 | 0 | 0 |  | 35 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BFLY.parquet | 515 | 100.0% | 444 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BGC.parquet | 346 | 86.4% | 422 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 86.4% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/BGS.parquet | 422 | 87.7% | 538 | 0 | 0 | 0 |  | 79 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.7% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/BHVN.parquet | 460 | 99.7% | 500 | 0 | 0 | 0 |  | 70 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BILI.parquet | 514 | 98.5% | 446 | 0 | 0 | 0 |  | 129 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BIOA.parquet | 272 | 64.4% | 574 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BKKT.parquet | 430 | 82.8% | 503 | 0 | 0 | 0 |  | 106 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BLMN.parquet | 373 | 90.3% | 405 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | RTH coverage 90.3% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/BLND.parquet | 424 | 96.9% | 533 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BMEA.parquet | 295 | 71.5% | 637 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BOBS.parquet | 280 | 62.8% | 650 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 62.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BORR.parquet | 502 | 100.0% | 457 | 0 | 0 | 0 |  | 111 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BTG.parquet | 528 | 100.0% | 431 | 0 | 0 | 0 |  | 137 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/BTGO.parquet | 485 | 96.7% | 468 | 0 | 0 | 0 |  | 107 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BUR.parquet | 406 | 94.4% | 525 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/BYND.parquet | 493 | 87.7% | 466 | 0 | 0 | 0 |  | 150 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CANG.parquet | 321 | 63.3% | 637 | 0 | 0 | 0 |  | 73 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CAPR.parquet | 494 | 96.9% | 463 | 0 | 0 | 0 |  | 115 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CERT.parquet | 370 | 89.0% | 561 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.0% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/CHPT.parquet | 529 | 93.1% | 430 | 0 | 0 | 0 |  | 165 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CIFR.parquet | 825 | 100.0% | 135 | 0 | 0 | 0 |  | 434 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/CLF.parquet | 544 | 100.0% | 404 | 0 | 0 | 0 |  | 153 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/CMPS.parquet | 469 | 97.4% | 489 | 0 | 0 | 0 |  | 88 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CORZ.parquet | 551 | 100.0% | 404 | 0 | 0 | 0 |  | 160 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/COTY.parquet | 432 | 100.0% | 525 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/CPRI.parquet | 413 | 99.7% | 521 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/CTKB.parquet | 297 | 74.6% | 304 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | RTH coverage 74.6% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/CTMX.parquet | 391 | 95.6% | 519 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CTNM.parquet | 254 | 63.6% | 347 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CWH.parquet | 403 | 95.1% | 557 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/CWK.parquet | 378 | 90.0% | 408 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  |  | RTH coverage 90.0% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/DC.parquet | 354 | 80.0% | 600 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/DDD.parquet | 439 | 97.2% | 502 | 0 | 0 | 0 |  | 59 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.2% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/DFH.parquet | 339 | 80.3% | 616 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  |  | RTH coverage 80.3% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/DNA.parquet | 484 | 99.0% | 466 | 0 | 0 | 0 |  | 97 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/DSP.parquet | 456 | 85.1% | 504 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/EAF.parquet | 283 | 64.1% | 657 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/EC.parquet | 363 | 84.6% | 582 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/EDIT.parquet | 355 | 85.1% | 400 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/EGHT.parquet | 228 | 56.1% | 673 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 56.1% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/ELME.parquet | 203 | 44.1% | 728 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  |  | RTH coverage 44.1% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/EMBC.parquet | 229 | 56.9% | 516 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | RTH coverage 56.9% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/ENOV.parquet | 423 | 96.9% | 532 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.9% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/ENVX.parquet | 492 | 98.5% | 439 | 0 | 0 | 0 |  | 107 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/EQX.parquet | 514 | 99.7% | 441 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/EROC.parquet | 557 | 99.7% | 395 | 0 | 0 | 0 |  | 167 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/ESRT.parquet | 410 | 97.4% | 520 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/EVGO.parquet | 415 | 89.5% | 542 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/EXK.parquet | 520 | 99.2% | 431 | 0 | 0 | 0 |  | 132 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/FDMT.parquet | 282 | 68.0% | 578 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/FEAM.parquet | 415 | 73.1% | 531 | 0 | 0 | 0 |  | 132 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/FIP.parquet | 345 | 85.9% | 570 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/FJET.parquet | 450 | 94.9% | 505 | 0 | 0 | 0 |  | 79 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/FOSL.parquet | 233 | 58.0% | 398 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | RTH coverage 58.0% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/FRVO.parquet | 530 | 99.5% | 427 | 0 | 0 | 0 |  | 142 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/FSM.parquet | 461 | 98.7% | 480 | 0 | 0 | 0 |  | 75 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/FUBO.parquet | 490 | 93.3% | 470 | 0 | 0 | 0 |  | 125 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/GAU.parquet | 333 | 75.4% | 416 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/GCTS.parquet | 523 | 85.6% | 428 | 0 | 0 | 0 |  | 188 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/GEMI.parquet | 432 | 89.2% | 527 | 0 | 0 | 0 |  | 84 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/GENI.parquet | 435 | 99.2% | 495 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/GOGO.parquet | 258 | 62.6% | 363 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 62.6% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/GORO.parquet | 418 | 82.8% | 518 | 0 | 0 | 0 |  | 94 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/GRAB.parquet | 878 | 100.0% | 82 | 0 | 0 | 0 |  | 488 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/GRPN.parquet | 298 | 72.0% | 660 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/GT.parquet | 443 | 99.7% | 511 | 0 | 0 | 0 |  | 54 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/GTN.parquet | 265 | 63.1% | 666 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/HAFN.parquet | 441 | 93.6% | 495 | 0 | 0 | 0 |  | 75 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/HIMX.parquet | 317 | 71.5% | 631 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/HL.parquet | 624 | 100.0% | 334 | 0 | 0 | 0 |  | 233 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/HLF.parquet | 360 | 82.8% | 586 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/HLIT.parquet | 344 | 83.3% | 421 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | RTH coverage 83.3% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/HLLY.parquet | 277 | 65.6% | 654 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/HMY.parquet | 555 | 98.2% | 401 | 0 | 0 | 0 |  | 171 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/HSAI.parquet | 306 | 70.5% | 625 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/HUYA.parquet | 356 | 85.1% | 575 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/HYLN.parquet | 469 | 96.4% | 487 | 0 | 0 | 0 |  | 92 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/IAUX.parquet | 455 | 99.7% | 502 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/IBRX.parquet | 557 | 100.0% | 403 | 0 | 0 | 0 |  | 166 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/IE.parquet | 453 | 96.2% | 497 | 0 | 0 | 0 |  | 77 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/IMSR.parquet | 379 | 83.3% | 513 | 0 | 0 | 0 |  | 53 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/INFQ.parquet | 780 | 100.0% | 179 | 0 | 0 | 0 |  | 389 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/INTR.parquet | 317 | 79.2% | 605 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/IRWD.parquet | 362 | 87.4% | 389 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.4% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/ITRG.parquet | 314 | 71.8% | 639 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/JBLU.parquet | 541 | 100.0% | 376 | 0 | 0 | 0 |  | 151 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/JELD.parquet | 309 | 75.6% | 621 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/JOBY.parquet | 904 | 100.0% | 56 | 0 | 0 | 0 |  | 513 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/KC.parquet | 344 | 79.2% | 598 | 0 | 0 | 0 |  | 35 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/KLRA.parquet | 327 | 80.8% | 346 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/KLXE.parquet | 238 | 59.5% | 363 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 59.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/KPTI.parquet | 219 | 51.8% | 522 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 51.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/KRO.parquet | 249 | 59.7% | 706 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 59.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/KSS.parquet | 440 | 99.5% | 509 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/LAC.parquet | 669 | 100.0% | 291 | 0 | 0 | 0 |  | 278 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/LAES.parquet | 693 | 96.7% | 267 | 0 | 0 | 0 |  | 316 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/LBRT.parquet | 431 | 96.7% | 518 | 0 | 0 | 0 |  | 53 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.7% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/LCID.parquet | 719 | 100.0% | 241 | 0 | 0 | 0 |  | 329 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/LEGN.parquet | 385 | 92.3% | 546 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/LI.parquet | 419 | 88.2% | 533 | 0 | 0 | 0 |  | 75 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/LILAK.parquet | 265 | 66.7% | 336 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/LION.parquet | 399 | 94.1% | 535 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/LODE.parquet | 384 | 87.7% | 547 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/LPL.parquet | 341 | 77.7% | 615 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/LVWR.parquet | 428 | 87.9% | 527 | 0 | 0 | 0 |  | 84 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/MBC.parquet | 419 | 98.7% | 508 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/MNRO.parquet | 320 | 80.0% | 285 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 80.0% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/MNSO.parquet | 325 | 75.4% | 628 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/MPT.parquet | 509 | 100.0% | 449 | 0 | 0 | 0 |  | 118 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/MRVI.parquet | 379 | 92.0% | 389 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/MX.parquet | 260 | 47.9% | 698 | 0 | 0 | 0 |  | 72 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 47.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/NABL.parquet | 394 | 96.4% | 533 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.4% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/NAK.parquet | 492 | 99.5% | 466 | 0 | 0 | 0 |  | 103 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NAT.parquet | 505 | 100.0% | 455 | 0 | 0 | 0 |  | 114 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NEOG.parquet | 376 | 93.1% | 403 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.1% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/NEWP.parquet | 381 | 90.3% | 508 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/NG.parquet | 512 | 100.0% | 445 | 0 | 0 | 0 |  | 121 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NIO.parquet | 799 | 100.0% | 161 | 0 | 0 | 0 |  | 408 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NMAX.parquet | 390 | 87.2% | 555 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/NNVC.parquet | 482 | 71.0% | 478 | 0 | 0 | 0 |  | 204 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/NRGV.parquet | 437 | 99.7% | 523 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NTSK.parquet | 467 | 100.0% | 487 | 0 | 0 | 0 |  | 76 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NUVB.parquet | 472 | 98.7% | 471 | 0 | 0 | 0 |  | 86 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NVAX.parquet | 474 | 99.7% | 486 | 0 | 0 | 0 |  | 84 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/NXDR.parquet | 387 | 91.5% | 543 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/NXE.parquet | 464 | 94.1% | 488 | 0 | 0 | 0 |  | 96 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/NXH.parquet | 421 | 95.6% | 337 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/OCTV.parquet | 388 | 95.4% | 445 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/OGG.parquet | 339 | 80.3% | 598 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/OPEN.parquet | 755 | 100.0% | 205 | 0 | 0 | 0 |  | 364 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/OPK.parquet | 314 | 72.6% | 501 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/OPTU.parquet | 385 | 94.9% | 549 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/ORIC.parquet | 308 | 70.3% | 549 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PAAI.parquet | 47 | 10.8% | 258 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 10.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PACB.parquet | 399 | 95.4% | 538 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PAX.parquet | 245 | 61.0% | 506 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 61.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PD.parquet | 358 | 84.9% | 598 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PHAT.parquet | 324 | 78.7% | 427 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PINS.parquet | 509 | 100.0% | 451 | 0 | 0 | 0 |  | 118 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/PL.parquet | 835 | 100.0% | 125 | 0 | 0 | 0 |  | 444 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/PLAY.parquet | 491 | 94.1% | 277 | 0 | 0 | 0 |  | 123 | 0 | 0 | 0 |  |  |  |  | RTH coverage 94.1% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/PLTK.parquet | 273 | 68.0% | 630 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PONY.parquet | 456 | 93.3% | 503 | 0 | 0 | 0 |  | 91 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/PRGO.parquet | 405 | 93.3% | 526 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.3% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/PTON.parquet | 424 | 97.2% | 535 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.2% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/PWP.parquet | 314 | 78.5% | 466 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/QBTS.parquet | 827 | 100.0% | 133 | 0 | 0 | 0 |  | 436 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/QXO.parquet | 597 | 100.0% | 360 | 0 | 0 | 0 |  | 206 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/RARE.parquet | 679 | 99.5% | 281 | 0 | 0 | 0 |  | 290 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/RBBN.parquet | 259 | 64.1% | 342 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/RC.parquet | 390 | 86.9% | 554 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  |  | RTH coverage 86.9% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/RDW.parquet | 881 | 100.0% | 79 | 0 | 0 | 0 |  | 490 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/REPL.parquet | 376 | 90.5% | 543 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/RSKD.parquet | 227 | 52.8% | 704 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 52.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/RXRX.parquet | 679 | 100.0% | 279 | 0 | 0 | 0 |  | 288 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/RXT.parquet | 644 | 99.2% | 316 | 0 | 0 | 0 |  | 256 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/RYAM.parquet | 211 | 49.2% | 720 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | RTH coverage 49.2% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/SANA.parquet | 383 | 89.7% | 548 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SB.parquet | 433 | 95.1% | 524 | 0 | 0 | 0 |  | 61 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SBH.parquet | 337 | 78.7% | 586 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.7% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/SDEV.parquet | 231 | 41.5% | 725 | 0 | 0 | 0 |  | 68 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 41.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SECZ.parquet | 596 | 99.2% | 363 | 0 | 0 | 0 |  | 208 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/SFIX.parquet | 284 | 69.5% | 576 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SG.parquet | 430 | 99.2% | 500 | 0 | 0 | 0 |  | 42 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/SGRY.parquet | 371 | 91.3% | 479 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SHEN.parquet | 333 | 83.6% | 269 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 83.6% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/SID.parquet | 397 | 90.0% | 551 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SLDB.parquet | 306 | 74.4% | 608 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SLI.parquet | 431 | 91.5% | 525 | 0 | 0 | 0 |  | 73 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SMJF.parquet | 179 | 26.9% | 777 | 0 | 0 | 0 |  | 73 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 26.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SMR.parquet | 932 | 100.0% | 28 | 0 | 0 | 0 |  | 540 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/SOC.parquet | 490 | 99.5% | 469 | 0 | 0 | 0 |  | 101 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/SOFI.parquet | 912 | 100.0% | 48 | 0 | 0 | 0 |  | 522 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/SONO.parquet | 371 | 91.5% | 334 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.5% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/SPCE.parquet | 596 | 100.0% | 363 | 0 | 0 | 0 |  | 205 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/SPRO.parquet | 156 | 36.1% | 603 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 36.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SPRU.parquet | 134 | 14.1% | 823 | 0 | 0 | 0 |  | 78 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 14.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SRAD.parquet | 378 | 90.5% | 437 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/STKE.parquet | 67 | 14.1% | 864 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 14.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/STTK.parquet | 250 | 61.8% | 491 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 61.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/SVM.parquet | 459 | 96.7% | 495 | 0 | 0 | 0 |  | 81 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/TDUP.parquet | 274 | 62.8% | 682 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 62.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/TE.parquet | 793 | 100.0% | 167 | 0 | 0 | 0 |  | 402 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/TGB.parquet | 430 | 93.6% | 374 | 0 | 0 | 0 |  | 64 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/THM.parquet | 328 | 78.0% | 443 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/TIGR.parquet | 351 | 82.3% | 585 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/TLRY.parquet | 510 | 99.2% | 437 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/TMC.parquet | 533 | 97.2% | 427 | 0 | 0 | 0 |  | 154 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/TME.parquet | 445 | 99.2% | 513 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/TRLV.parquet | 407 | 91.8% | 541 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/TRX.parquet | 483 | 98.7% | 476 | 0 | 0 | 0 |  | 97 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/TV.parquet | 340 | 83.1% | 591 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/UAMY.parquet | 556 | 99.2% | 403 | 0 | 0 | 0 |  | 169 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/ULCC.parquet | 379 | 91.5% | 336 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/URG.parquet | 532 | 100.0% | 414 | 0 | 0 | 0 |  | 141 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/USAS.parquet | 516 | 98.2% | 442 | 0 | 0 | 0 |  | 132 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/UUUU.parquet | 730 | 100.0% | 230 | 0 | 0 | 0 |  | 339 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/VFC.parquet | 441 | 100.0% | 516 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/VGZ.parquet | 392 | 94.6% | 356 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/VIR.parquet | 339 | 82.6% | 570 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  |  | RTH coverage 82.6% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/VISN.parquet | 412 | 96.7% | 516 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/VLN.parquet | 336 | 73.9% | 623 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/VNET.parquet | 379 | 93.6% | 317 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/VYX.parquet | 436 | 98.2% | 520 | 0 | 0 | 0 |  | 52 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-17 |
| 2026-09-17/VZLA.parquet | 452 | 97.2% | 505 | 0 | 0 | 0 |  | 72 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/WRN.parquet | 333 | 73.1% | 624 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/XE.parquet | 702 | 100.0% | 258 | 0 | 0 | 0 |  | 311 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/XERS.parquet | 347 | 85.9% | 390 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/XRAY.parquet | 435 | 99.7% | 501 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/XRX.parquet | 405 | 92.0% | 555 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.0% < 98%; no daily bar for 2026-09-17 |
| 2026-09-17/XXI.parquet | 454 | 95.9% | 504 | 0 | 0 | 0 |  | 79 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-17/YSS.parquet | 479 | 99.7% | 478 | 0 | 0 | 0 |  | 89 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-17/ZH.parquet | 167 | 39.5% | 761 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 39.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/AAL.parquet | 685 | 100.0% | 275 | 0 | 0 | 0 |  | 294 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/ABSI.parquet | 533 | 98.2% | 426 | 0 | 0 | 0 |  | 149 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/ACHR.parquet | 779 | 100.0% | 181 | 0 | 0 | 0 |  | 388 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/ACRS.parquet | 344 | 83.6% | 430 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ADCT.parquet | 328 | 74.1% | 627 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ADTN.parquet | 312 | 75.1% | 624 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  |  | RTH coverage 75.1% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/AESI.parquet | 397 | 90.0% | 534 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  |  | RTH coverage 90.0% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/AG.parquet | 714 | 100.0% | 246 | 0 | 0 | 0 |  | 323 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/AI.parquet | 569 | 99.7% | 391 | 0 | 0 | 0 |  | 179 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/ALEC.parquet | 223 | 50.5% | 564 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ALKT.parquet | 307 | 75.9% | 303 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/AMC.parquet | 770 | 100.0% | 190 | 0 | 0 | 0 |  | 379 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/AMPX.parquet | 586 | 98.7% | 374 | 0 | 0 | 0 |  | 200 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/AMRX.parquet | 374 | 86.4% | 487 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  |  | RTH coverage 86.4% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/ANGX.parquet | 473 | 96.9% | 486 | 0 | 0 | 0 |  | 94 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ANNX.parquet | 366 | 89.5% | 320 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ANVS.parquet | 263 | 58.7% | 668 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 58.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/APUS.parquet | 442 | 49.2% | 492 | 0 | 0 | 0 |  | 249 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 49.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ARHS.parquet | 295 | 73.6% | 308 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ARIS.parquet | 424 | 94.4% | 520 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ASM.parquet | 474 | 96.2% | 485 | 0 | 0 | 0 |  | 98 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ASPN.parquet | 310 | 69.7% | 630 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/AUTL.parquet | 294 | 70.3% | 575 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BB.parquet | 679 | 100.0% | 281 | 0 | 0 | 0 |  | 288 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BBAI.parquet | 775 | 100.0% | 185 | 0 | 0 | 0 |  | 384 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BBWI.parquet | 461 | 99.0% | 500 | 0 | 0 | 0 |  | 74 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BEKE.parquet | 450 | 98.5% | 492 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BFLY.parquet | 493 | 99.2% | 467 | 0 | 0 | 0 |  | 105 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BGC.parquet | 359 | 88.2% | 572 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 88.2% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/BGS.parquet | 487 | 98.7% | 463 | 0 | 0 | 0 |  | 101 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/BHVN.parquet | 458 | 99.2% | 473 | 0 | 0 | 0 |  | 70 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BILI.parquet | 468 | 93.3% | 475 | 0 | 0 | 0 |  | 103 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BIOA.parquet | 243 | 57.4% | 505 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 57.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BKKT.parquet | 528 | 91.0% | 426 | 0 | 0 | 0 |  | 172 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BLMN.parquet | 389 | 93.8% | 542 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.8% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/BLND.parquet | 402 | 95.9% | 529 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BMEA.parquet | 246 | 58.2% | 693 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 58.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BOBS.parquet | 293 | 67.2% | 636 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 67.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BORR.parquet | 491 | 98.7% | 470 | 0 | 0 | 0 |  | 105 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BTG.parquet | 524 | 100.0% | 431 | 0 | 0 | 0 |  | 133 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/BTGO.parquet | 519 | 97.4% | 442 | 0 | 0 | 0 |  | 138 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BUR.parquet | 427 | 97.7% | 508 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/BYND.parquet | 417 | 83.9% | 523 | 0 | 0 | 0 |  | 91 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CANG.parquet | 412 | 84.6% | 530 | 0 | 0 | 0 |  | 81 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CAPR.parquet | 469 | 94.9% | 491 | 0 | 0 | 0 |  | 98 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CERT.parquet | 383 | 93.1% | 548 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.1% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/CHPT.parquet | 519 | 94.9% | 438 | 0 | 0 | 0 |  | 148 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CIFR.parquet | 838 | 100.0% | 122 | 0 | 0 | 0 |  | 447 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/CLF.parquet | 531 | 100.0% | 409 | 0 | 0 | 0 |  | 140 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/CMPS.parquet | 446 | 95.6% | 510 | 0 | 0 | 0 |  | 73 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CORZ.parquet | 501 | 100.0% | 457 | 0 | 0 | 0 |  | 111 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/COTY.parquet | 434 | 99.7% | 504 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/CPRI.parquet | 416 | 99.5% | 522 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/CTKB.parquet | 255 | 63.1% | 346 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 63.1% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/CTMX.parquet | 350 | 84.9% | 386 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CTNM.parquet | 208 | 51.3% | 393 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 51.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CWH.parquet | 405 | 94.6% | 526 | 0 | 0 | 0 |  | 35 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/CWK.parquet | 362 | 89.0% | 239 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.0% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/DC.parquet | 368 | 82.6% | 568 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/DDD.parquet | 458 | 96.4% | 502 | 0 | 0 | 0 |  | 81 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.4% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/DFH.parquet | 341 | 78.0% | 599 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.0% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/DNA.parquet | 430 | 79.5% | 528 | 0 | 0 | 0 |  | 119 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/DSP.parquet | 575 | 93.1% | 377 | 0 | 0 | 0 |  | 212 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/EAF.parquet | 254 | 59.5% | 675 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 59.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/EC.parquet | 353 | 80.8% | 578 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/EDIT.parquet | 353 | 82.8% | 598 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/EGHT.parquet | 233 | 56.9% | 473 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  |  | RTH coverage 56.9% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/ELME.parquet | 269 | 55.1% | 686 | 0 | 0 | 0 |  | 53 | 0 | 0 | 0 |  |  |  |  | RTH coverage 55.1% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/EMBC.parquet | 233 | 55.9% | 698 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | RTH coverage 55.9% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/ENOV.parquet | 393 | 91.3% | 538 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.3% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/ENVX.parquet | 465 | 96.2% | 494 | 0 | 0 | 0 |  | 91 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/EQX.parquet | 522 | 100.0% | 438 | 0 | 0 | 0 |  | 131 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/EROC.parquet | 522 | 97.7% | 429 | 0 | 0 | 0 |  | 140 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ESRT.parquet | 415 | 96.2% | 544 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/EVGO.parquet | 425 | 89.0% | 531 | 0 | 0 | 0 |  | 78 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/EXK.parquet | 526 | 99.7% | 428 | 0 | 0 | 0 |  | 136 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/FDMT.parquet | 271 | 62.1% | 470 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 62.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/FEAM.parquet | 469 | 89.7% | 491 | 0 | 0 | 0 |  | 123 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/FIP.parquet | 286 | 65.9% | 674 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/FJET.parquet | 514 | 97.2% | 445 | 0 | 0 | 0 |  | 134 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/FOSL.parquet | 161 | 38.5% | 441 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 38.5% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/FRVO.parquet | 516 | 99.5% | 441 | 0 | 0 | 0 |  | 127 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/FSM.parquet | 462 | 98.0% | 487 | 0 | 0 | 0 |  | 79 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/FUBO.parquet | 444 | 91.3% | 516 | 0 | 0 | 0 |  | 87 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/GAU.parquet | 342 | 80.5% | 616 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/GCTS.parquet | 443 | 75.9% | 508 | 0 | 0 | 0 |  | 146 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/GEMI.parquet | 650 | 99.7% | 310 | 0 | 0 | 0 |  | 262 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/GENI.parquet | 491 | 100.0% | 468 | 0 | 0 | 0 |  | 100 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/GOGO.parquet | 311 | 75.6% | 392 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 75.6% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/GORO.parquet | 325 | 66.4% | 606 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/GRAB.parquet | 857 | 100.0% | 103 | 0 | 0 | 0 |  | 467 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/GRPN.parquet | 278 | 65.6% | 659 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/GT.parquet | 483 | 99.0% | 477 | 0 | 0 | 0 |  | 97 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/GTN.parquet | 287 | 68.0% | 644 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/HAFN.parquet | 466 | 98.2% | 485 | 0 | 0 | 0 |  | 82 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/HIMX.parquet | 303 | 66.9% | 628 | 0 | 0 | 0 |  | 42 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/HL.parquet | 637 | 100.0% | 320 | 0 | 0 | 0 |  | 246 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/HLF.parquet | 381 | 88.7% | 543 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/HLIT.parquet | 350 | 84.6% | 581 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  |  | RTH coverage 84.6% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/HLLY.parquet | 286 | 66.1% | 667 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/HMY.parquet | 519 | 96.9% | 431 | 0 | 0 | 0 |  | 140 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/HSAI.parquet | 300 | 68.5% | 652 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/HUYA.parquet | 352 | 85.9% | 579 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/HYLN.parquet | 449 | 92.0% | 509 | 0 | 0 | 0 |  | 89 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/IAUX.parquet | 506 | 93.8% | 447 | 0 | 0 | 0 |  | 139 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/IBRX.parquet | 555 | 99.2% | 405 | 0 | 0 | 0 |  | 170 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/IE.parquet | 420 | 91.5% | 533 | 0 | 0 | 0 |  | 62 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/IMSR.parquet | 389 | 83.1% | 571 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/INFQ.parquet | 786 | 100.0% | 174 | 0 | 0 | 0 |  | 395 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/INTR.parquet | 358 | 87.7% | 388 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/IRWD.parquet | 311 | 75.6% | 389 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 75.6% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/ITRG.parquet | 302 | 66.9% | 560 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/JBLU.parquet | 516 | 100.0% | 278 | 0 | 0 | 0 |  | 127 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/JELD.parquet | 342 | 81.3% | 589 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/JOBY.parquet | 915 | 100.0% | 45 | 0 | 0 | 0 |  | 524 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/KC.parquet | 421 | 87.4% | 539 | 0 | 0 | 0 |  | 80 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/KLRA.parquet | 345 | 84.1% | 311 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/KLXE.parquet | 133 | 32.3% | 511 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 32.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/KPTI.parquet | 212 | 48.7% | 660 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 48.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/KRO.parquet | 182 | 43.3% | 749 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 43.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/KSS.parquet | 441 | 98.7% | 503 | 0 | 0 | 0 |  | 56 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/LAC.parquet | 681 | 100.0% | 279 | 0 | 0 | 0 |  | 290 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/LAES.parquet | 701 | 97.7% | 253 | 0 | 0 | 0 |  | 321 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/LBRT.parquet | 427 | 96.2% | 511 | 0 | 0 | 0 |  | 51 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.2% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/LCID.parquet | 717 | 100.0% | 242 | 0 | 0 | 0 |  | 327 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/LEGN.parquet | 399 | 94.6% | 543 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/LI.parquet | 399 | 89.5% | 532 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/LILAK.parquet | 270 | 65.9% | 393 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/LION.parquet | 427 | 98.0% | 520 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/LODE.parquet | 307 | 71.0% | 604 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/LPL.parquet | 363 | 80.3% | 588 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/LVWR.parquet | 491 | 93.1% | 469 | 0 | 0 | 0 |  | 127 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/MBC.parquet | 421 | 100.0% | 512 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/MNRO.parquet | 310 | 76.9% | 621 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 76.9% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/MNSO.parquet | 388 | 83.6% | 563 | 0 | 0 | 0 |  | 61 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/MPT.parquet | 509 | 100.0% | 451 | 0 | 0 | 0 |  | 118 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/MRVI.parquet | 370 | 90.5% | 538 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/MX.parquet | 254 | 48.7% | 700 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 48.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NABL.parquet | 406 | 96.7% | 524 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.7% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/NAK.parquet | 485 | 95.9% | 475 | 0 | 0 | 0 |  | 110 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NAT.parquet | 499 | 100.0% | 461 | 0 | 0 | 0 |  | 108 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/NEOG.parquet | 377 | 89.5% | 554 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.5% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/NEWP.parquet | 369 | 89.5% | 462 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NG.parquet | 484 | 98.7% | 476 | 0 | 0 | 0 |  | 98 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/NIO.parquet | 828 | 100.0% | 132 | 0 | 0 | 0 |  | 437 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/NMAX.parquet | 364 | 76.9% | 592 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NNVC.parquet | 361 | 60.8% | 595 | 0 | 0 | 0 |  | 123 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 60.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NRGV.parquet | 453 | 96.4% | 503 | 0 | 0 | 0 |  | 76 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NTSK.parquet | 453 | 100.0% | 505 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/NUVB.parquet | 419 | 94.1% | 537 | 0 | 0 | 0 |  | 51 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NVAX.parquet | 474 | 97.7% | 479 | 0 | 0 | 0 |  | 93 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NXDR.parquet | 360 | 84.1% | 593 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/NXE.parquet | 471 | 98.5% | 484 | 0 | 0 | 0 |  | 86 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/NXH.parquet | 343 | 77.4% | 504 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/OCTV.parquet | 401 | 97.2% | 387 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/OGG.parquet | 287 | 68.5% | 644 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/OPEN.parquet | 718 | 100.0% | 242 | 0 | 0 | 0 |  | 328 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/OPK.parquet | 311 | 72.8% | 448 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/OPTU.parquet | 359 | 86.4% | 597 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ORIC.parquet | 302 | 72.8% | 427 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PAAI.parquet | 594 | 86.9% | 66 | 0 | 0 | 0 |  | 254 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PACB.parquet | 371 | 85.9% | 548 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PAX.parquet | 230 | 56.4% | 371 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 56.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PD.parquet | 355 | 81.0% | 594 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PHAT.parquet | 263 | 62.6% | 607 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 62.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PINS.parquet | 522 | 100.0% | 427 | 0 | 0 | 0 |  | 131 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/PL.parquet | 867 | 99.7% | 93 | 0 | 0 | 0 |  | 477 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/PLAY.parquet | 437 | 90.3% | 513 | 0 | 0 | 0 |  | 85 | 0 | 0 | 0 |  |  |  |  | RTH coverage 90.3% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/PLTK.parquet | 292 | 70.8% | 314 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PONY.parquet | 445 | 93.1% | 515 | 0 | 0 | 0 |  | 82 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/PRGO.parquet | 393 | 89.2% | 538 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.2% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/PTON.parquet | 433 | 98.5% | 520 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/PWP.parquet | 315 | 77.2% | 616 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/QBTS.parquet | 842 | 100.0% | 118 | 0 | 0 | 0 |  | 452 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/QXO.parquet | 561 | 100.0% | 398 | 0 | 0 | 0 |  | 170 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/RARE.parquet | 663 | 100.0% | 297 | 0 | 0 | 0 |  | 272 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/RBBN.parquet | 189 | 44.6% | 554 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 44.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/RC.parquet | 342 | 77.4% | 617 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  |  | RTH coverage 77.4% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/RDW.parquet | 904 | 100.0% | 56 | 0 | 0 | 0 |  | 513 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/REPL.parquet | 315 | 75.1% | 585 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/RSKD.parquet | 280 | 66.9% | 676 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/RXRX.parquet | 742 | 100.0% | 218 | 0 | 0 | 0 |  | 352 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/RXT.parquet | 581 | 97.2% | 350 | 0 | 0 | 0 |  | 202 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/RYAM.parquet | 284 | 68.2% | 673 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 68.2% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/SANA.parquet | 357 | 83.1% | 595 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SB.parquet | 392 | 88.2% | 539 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SBH.parquet | 352 | 81.0% | 568 | 0 | 0 | 0 |  | 35 | 0 | 0 | 0 |  |  |  |  | RTH coverage 81.0% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/SDEV.parquet | 496 | 52.8% | 460 | 0 | 0 | 0 |  | 289 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 52.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SECZ.parquet | 835 | 99.7% | 125 | 0 | 0 | 0 |  | 445 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/SFIX.parquet | 304 | 73.6% | 434 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SG.parquet | 451 | 98.7% | 498 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/SGRY.parquet | 366 | 90.3% | 308 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SHEN.parquet | 366 | 89.5% | 565 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  |  | RTH coverage 89.5% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/SID.parquet | 398 | 92.3% | 559 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SLDB.parquet | 266 | 65.1% | 335 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SLI.parquet | 327 | 69.5% | 631 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SMJF.parquet | 248 | 51.0% | 708 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 51.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SMR.parquet | 939 | 100.0% | 21 | 0 | 0 | 0 |  | 548 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/SOC.parquet | 486 | 99.7% | 474 | 0 | 0 | 0 |  | 96 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/SOFI.parquet | 908 | 100.0% | 52 | 0 | 0 | 0 |  | 518 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/SONO.parquet | 362 | 87.4% | 569 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.4% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/SPCE.parquet | 538 | 97.2% | 419 | 0 | 0 | 0 |  | 158 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SPRO.parquet | 81 | 18.5% | 850 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 18.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SPRU.parquet | 374 | 50.3% | 586 | 0 | 0 | 0 |  | 177 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SRAD.parquet | 337 | 80.0% | 594 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/STKE.parquet | 137 | 28.2% | 823 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 28.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/STTK.parquet | 294 | 72.8% | 307 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/SVM.parquet | 470 | 96.9% | 487 | 0 | 0 | 0 |  | 91 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/TDUP.parquet | 332 | 74.4% | 599 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/TE.parquet | 787 | 100.0% | 173 | 0 | 0 | 0 |  | 396 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/TGB.parquet | 438 | 99.0% | 519 | 0 | 0 | 0 |  | 51 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/THM.parquet | 432 | 92.6% | 527 | 0 | 0 | 0 |  | 70 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/TIGR.parquet | 363 | 82.0% | 594 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/TLRY.parquet | 489 | 85.4% | 409 | 0 | 0 | 0 |  | 156 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/TMC.parquet | 516 | 95.1% | 442 | 0 | 0 | 0 |  | 145 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/TME.parquet | 470 | 100.0% | 489 | 0 | 0 | 0 |  | 79 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/TRLV.parquet | 452 | 98.2% | 506 | 0 | 0 | 0 |  | 68 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/TRX.parquet | 499 | 98.2% | 461 | 0 | 0 | 0 |  | 115 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/TV.parquet | 385 | 94.4% | 555 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/UAMY.parquet | 587 | 99.2% | 369 | 0 | 0 | 0 |  | 199 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/ULCC.parquet | 314 | 77.2% | 323 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/URG.parquet | 526 | 99.2% | 434 | 0 | 0 | 0 |  | 138 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/USAS.parquet | 498 | 96.7% | 459 | 0 | 0 | 0 |  | 120 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/UUUU.parquet | 804 | 100.0% | 155 | 0 | 0 | 0 |  | 413 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/VFC.parquet | 443 | 100.0% | 502 | 0 | 0 | 0 |  | 52 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-18 |
| 2026-09-18/VGZ.parquet | 393 | 92.8% | 371 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/VIR.parquet | 391 | 96.2% | 219 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  |  | RTH coverage 96.2% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/VISN.parquet | 427 | 99.7% | 514 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/VLN.parquet | 285 | 58.7% | 670 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 58.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/VNET.parquet | 375 | 90.5% | 558 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/VYX.parquet | 445 | 97.7% | 514 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.7% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/VZLA.parquet | 433 | 92.6% | 498 | 0 | 0 | 0 |  | 71 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/WRN.parquet | 311 | 70.3% | 594 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/XE.parquet | 649 | 100.0% | 308 | 0 | 0 | 0 |  | 259 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/XERS.parquet | 340 | 83.9% | 390 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/XRAY.parquet | 448 | 100.0% | 483 | 0 | 0 | 0 |  | 58 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-18/XRX.parquet | 374 | 85.1% | 586 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  |  | RTH coverage 85.1% < 98%; no daily bar for 2026-09-18 |
| 2026-09-18/XXI.parquet | 501 | 96.4% | 454 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/YSS.parquet | 464 | 97.7% | 485 | 0 | 0 | 0 |  | 82 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-18/ZH.parquet | 245 | 59.2% | 685 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 59.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/AAL.parquet | 750 | 100.0% | 210 | 0 | 0 | 0 |  | 359 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/ABSI.parquet | 511 | 97.4% | 436 | 0 | 0 | 0 |  | 131 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ACHR.parquet | 664 | 100.0% | 293 | 0 | 0 | 0 |  | 273 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/ACRS.parquet | 330 | 81.5% | 393 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ADCT.parquet | 375 | 93.6% | 271 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ADTN.parquet | 285 | 69.2% | 466 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 69.2% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/AESI.parquet | 393 | 98.7% | 155 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/AG.parquet | 604 | 100.0% | 348 | 0 | 0 | 0 |  | 213 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/AI.parquet | 447 | 99.7% | 513 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/ALEC.parquet | 261 | 55.4% | 465 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 55.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ALKT.parquet | 298 | 73.6% | 366 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/AMC.parquet | 622 | 100.0% | 338 | 0 | 0 | 0 |  | 231 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/AMPX.parquet | 483 | 99.2% | 473 | 0 | 0 | 0 |  | 95 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/AMRX.parquet | 439 | 98.5% | 511 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/ANGX.parquet | 367 | 89.2% | 408 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ANNX.parquet | 350 | 86.2% | 581 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ANVS.parquet | 318 | 77.7% | 452 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/APUS.parquet | 133 | 9.2% | 822 | 0 | 0 | 0 |  | 96 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 9.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ARHS.parquet | 347 | 82.3% | 598 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ARIS.parquet | 382 | 91.0% | 403 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ASM.parquet | 425 | 97.4% | 522 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ASPN.parquet | 265 | 64.9% | 519 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/AUTL.parquet | 222 | 50.8% | 709 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BB.parquet | 648 | 100.0% | 312 | 0 | 0 | 0 |  | 257 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/BBAI.parquet | 606 | 100.0% | 354 | 0 | 0 | 0 |  | 215 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/BBWI.parquet | 415 | 100.0% | 399 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/BEKE.parquet | 418 | 100.0% | 326 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/BFLY.parquet | 435 | 99.0% | 525 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/BGC.parquet | 378 | 93.1% | 389 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.1% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/BGS.parquet | 397 | 93.8% | 421 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.8% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/BHVN.parquet | 392 | 97.4% | 498 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BILI.parquet | 443 | 91.8% | 505 | 0 | 0 | 0 |  | 85 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BIOA.parquet | 268 | 64.9% | 428 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BKKT.parquet | 517 | 95.1% | 432 | 0 | 0 | 0 |  | 145 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BLMN.parquet | 353 | 87.7% | 425 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.7% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/BLND.parquet | 365 | 92.0% | 370 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BMEA.parquet | 290 | 69.0% | 575 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BOBS.parquet | 318 | 79.5% | 142 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BORR.parquet | 435 | 98.7% | 505 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/BTG.parquet | 442 | 99.0% | 507 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/BTGO.parquet | 425 | 92.3% | 530 | 0 | 0 | 0 |  | 64 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BUR.parquet | 349 | 84.4% | 459 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/BYND.parquet | 427 | 87.7% | 513 | 0 | 0 | 0 |  | 86 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/CANG.parquet | 237 | 50.0% | 701 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/CAPR.parquet | 525 | 96.2% | 427 | 0 | 0 | 0 |  | 150 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/CERT.parquet | 376 | 91.8% | 357 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.8% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/CHPT.parquet | 414 | 94.1% | 544 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/CIFR.parquet | 851 | 100.0% | 109 | 0 | 0 | 0 |  | 461 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/CLF.parquet | 434 | 100.0% | 526 | 0 | 0 | 0 |  | 43 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/CMPS.parquet | 463 | 93.1% | 489 | 0 | 0 | 0 |  | 100 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/CORZ.parquet | 568 | 100.0% | 391 | 0 | 0 | 0 |  | 178 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/COTY.parquet | 396 | 99.2% | 443 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/CPRI.parquet | 399 | 99.7% | 511 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/CTKB.parquet | 285 | 69.7% | 617 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 69.7% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/CTMX.parquet | 325 | 78.5% | 420 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/CTNM.parquet | 303 | 70.8% | 628 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/CWH.parquet | 395 | 99.2% | 378 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/CWK.parquet | 336 | 85.6% | 56 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  |  | RTH coverage 85.6% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/DC.parquet | 417 | 95.1% | 538 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/DDD.parquet | 393 | 92.3% | 543 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.3% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/DFH.parquet | 333 | 81.5% | 320 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 81.5% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/DNA.parquet | 388 | 94.1% | 521 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/DSP.parquet | 327 | 75.4% | 610 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/EAF.parquet | 284 | 72.0% | 181 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/EC.parquet | 350 | 86.7% | 404 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/EDIT.parquet | 357 | 84.6% | 574 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/EGHT.parquet | 334 | 82.0% | 433 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  |  | RTH coverage 82.0% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/ELME.parquet | 353 | 88.7% | 535 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | RTH coverage 88.7% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/EMBC.parquet | 234 | 57.4% | 697 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 57.4% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/ENOV.parquet | 364 | 91.3% | 142 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.3% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/ENVX.parquet | 478 | 96.4% | 481 | 0 | 0 | 0 |  | 103 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/EQX.parquet | 455 | 100.0% | 487 | 0 | 0 | 0 |  | 64 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/EROC.parquet | 428 | 98.0% | 533 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ESRT.parquet | 391 | 98.2% | 150 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/EVGO.parquet | 467 | 99.2% | 492 | 0 | 0 | 0 |  | 80 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/EXK.parquet | 435 | 99.7% | 513 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/FDMT.parquet | 283 | 70.0% | 648 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/FEAM.parquet | 328 | 65.6% | 603 | 0 | 0 | 0 |  | 78 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/FIP.parquet | 333 | 82.0% | 598 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/FJET.parquet | 489 | 99.5% | 468 | 0 | 0 | 0 |  | 100 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/FOSL.parquet | 201 | 49.2% | 400 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 49.2% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/FRVO.parquet | 525 | 100.0% | 418 | 0 | 0 | 0 |  | 136 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/FSM.parquet | 408 | 97.2% | 508 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/FUBO.parquet | 379 | 91.0% | 497 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/GAU.parquet | 338 | 84.1% | 451 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/GCTS.parquet | 440 | 90.0% | 487 | 0 | 0 | 0 |  | 88 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/GEMI.parquet | 688 | 98.0% | 269 | 0 | 0 | 0 |  | 305 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/GENI.parquet | 412 | 99.5% | 480 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/GOGO.parquet | 247 | 61.5% | 354 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 61.5% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/GORO.parquet | 332 | 77.7% | 628 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/GRAB.parquet | 844 | 100.0% | 116 | 0 | 0 | 0 |  | 455 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/GRPN.parquet | 387 | 89.2% | 567 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/GT.parquet | 477 | 99.7% | 483 | 0 | 0 | 0 |  | 89 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/GTN.parquet | 321 | 81.8% | 155 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/HAFN.parquet | 414 | 92.0% | 542 | 0 | 0 | 0 |  | 54 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/HIMX.parquet | 406 | 87.9% | 554 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/HL.parquet | 496 | 100.0% | 463 | 0 | 0 | 0 |  | 105 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/HLF.parquet | 314 | 79.7% | 89 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/HLIT.parquet | 302 | 72.0% | 628 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | RTH coverage 72.0% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/HLLY.parquet | 281 | 71.0% | 350 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/HMY.parquet | 488 | 99.5% | 472 | 0 | 0 | 0 |  | 98 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/HSAI.parquet | 400 | 91.8% | 534 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/HUYA.parquet | 330 | 82.6% | 469 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/HYLN.parquet | 404 | 94.9% | 554 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/IAUX.parquet | 407 | 98.7% | 390 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/IBRX.parquet | 552 | 99.0% | 403 | 0 | 0 | 0 |  | 165 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/IE.parquet | 352 | 89.0% | 277 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/IMSR.parquet | 417 | 83.9% | 520 | 0 | 0 | 0 |  | 89 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/INFQ.parquet | 612 | 100.0% | 349 | 0 | 0 | 0 |  | 221 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/INTR.parquet | 352 | 86.7% | 299 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/IRWD.parquet | 335 | 81.0% | 429 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  |  | RTH coverage 81.0% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/ITRG.parquet | 305 | 74.6% | 606 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/JBLU.parquet | 543 | 99.7% | 417 | 0 | 0 | 0 |  | 154 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/JELD.parquet | 295 | 72.3% | 261 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/JOBY.parquet | 742 | 100.0% | 218 | 0 | 0 | 0 |  | 351 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/KC.parquet | 402 | 93.3% | 546 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/KLRA.parquet | 322 | 78.0% | 619 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/KLXE.parquet | 121 | 28.5% | 810 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 28.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/KPTI.parquet | 207 | 49.5% | 734 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 49.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/KRO.parquet | 163 | 39.0% | 472 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 39.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/KSS.parquet | 417 | 99.5% | 514 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/LAC.parquet | 544 | 100.0% | 416 | 0 | 0 | 0 |  | 153 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/LAES.parquet | 716 | 98.5% | 244 | 0 | 0 | 0 |  | 332 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/LBRT.parquet | 392 | 98.7% | 239 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/LCID.parquet | 727 | 100.0% | 233 | 0 | 0 | 0 |  | 336 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/LEGN.parquet | 419 | 98.2% | 530 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/LI.parquet | 543 | 99.5% | 417 | 0 | 0 | 0 |  | 155 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/LILAK.parquet | 263 | 65.6% | 486 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/LION.parquet | 390 | 96.4% | 212 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/LODE.parquet | 342 | 84.4% | 236 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/LPL.parquet | 364 | 89.7% | 440 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/LVWR.parquet | 238 | 52.6% | 706 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 52.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/MBC.parquet | 373 | 92.3% | 349 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.3% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/MNRO.parquet | 352 | 87.4% | 381 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.4% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/MNSO.parquet | 386 | 93.8% | 532 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/MPT.parquet | 413 | 100.0% | 477 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/MRVI.parquet | 378 | 90.5% | 524 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/MX.parquet | 555 | 92.0% | 402 | 0 | 0 | 0 |  | 195 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/NABL.parquet | 367 | 91.0% | 265 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 91.0% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/NAK.parquet | 510 | 98.2% | 439 | 0 | 0 | 0 |  | 126 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NAT.parquet | 423 | 99.7% | 527 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NEOG.parquet | 376 | 92.0% | 397 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.0% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/NEWP.parquet | 371 | 91.8% | 572 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/NG.parquet | 419 | 99.0% | 535 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NIO.parquet | 698 | 100.0% | 262 | 0 | 0 | 0 |  | 307 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NMAX.parquet | 354 | 85.4% | 436 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/NNVC.parquet | 410 | 86.9% | 536 | 0 | 0 | 0 |  | 70 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/NRGV.parquet | 417 | 98.7% | 541 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NTSK.parquet | 482 | 99.7% | 475 | 0 | 0 | 0 |  | 92 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NUVB.parquet | 378 | 93.1% | 562 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/NVAX.parquet | 482 | 99.7% | 477 | 0 | 0 | 0 |  | 92 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NXDR.parquet | 324 | 80.3% | 405 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/NXE.parquet | 450 | 99.7% | 501 | 0 | 0 | 0 |  | 60 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/NXH.parquet | 356 | 78.0% | 554 | 0 | 0 | 0 |  | 51 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/OCTV.parquet | 373 | 87.4% | 558 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/OGG.parquet | 363 | 92.6% | 99 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/OPEN.parquet | 764 | 100.0% | 196 | 0 | 0 | 0 |  | 373 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/OPK.parquet | 322 | 71.8% | 425 | 0 | 0 | 0 |  | 42 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/OPTU.parquet | 361 | 90.8% | 289 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/ORIC.parquet | 247 | 60.3% | 662 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 60.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PAAI.parquet | 891 | 96.7% | 69 | 0 | 0 | 0 |  | 513 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PACB.parquet | 402 | 96.7% | 551 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PAX.parquet | 304 | 74.6% | 390 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PD.parquet | 333 | 81.0% | 322 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PHAT.parquet | 282 | 68.7% | 469 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PINS.parquet | 425 | 100.0% | 522 | 0 | 0 | 0 |  | 34 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/PL.parquet | 607 | 100.0% | 352 | 0 | 0 | 0 |  | 216 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/PLAY.parquet | 426 | 95.1% | 352 | 0 | 0 | 0 |  | 54 | 0 | 0 | 0 |  |  |  |  | RTH coverage 95.1% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/PLTK.parquet | 293 | 72.3% | 637 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PONY.parquet | 474 | 95.6% | 484 | 0 | 0 | 0 |  | 101 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/PRGO.parquet | 369 | 92.3% | 173 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 92.3% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/PTON.parquet | 424 | 95.6% | 536 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  |  | RTH coverage 95.6% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/PWP.parquet | 339 | 84.9% | 267 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/QBTS.parquet | 831 | 100.0% | 129 | 0 | 0 | 0 |  | 440 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/QXO.parquet | 570 | 100.0% | 388 | 0 | 0 | 0 |  | 179 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/RARE.parquet | 529 | 99.0% | 430 | 0 | 0 | 0 |  | 143 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/RBBN.parquet | 209 | 50.8% | 512 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/RC.parquet | 300 | 72.8% | 336 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 72.8% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/RDW.parquet | 679 | 100.0% | 281 | 0 | 0 | 0 |  | 288 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/REPL.parquet | 349 | 84.1% | 606 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/RSKD.parquet | 270 | 68.0% | 509 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/RXRX.parquet | 767 | 100.0% | 193 | 0 | 0 | 0 |  | 376 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/RXT.parquet | 587 | 99.5% | 373 | 0 | 0 | 0 |  | 199 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/RYAM.parquet | 257 | 65.1% | 225 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  |  | RTH coverage 65.1% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/SANA.parquet | 382 | 88.7% | 566 | 0 | 0 | 0 |  | 35 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SB.parquet | 384 | 95.1% | 305 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SBH.parquet | 308 | 78.5% | 84 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.5% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/SDEV.parquet | 553 | 78.5% | 400 | 0 | 0 | 0 |  | 246 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SECZ.parquet | 757 | 99.7% | 201 | 0 | 0 | 0 |  | 367 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/SFIX.parquet | 392 | 93.8% | 559 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SG.parquet | 400 | 100.0% | 429 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/SGRY.parquet | 364 | 91.5% | 452 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SHEN.parquet | 322 | 80.8% | 279 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 80.8% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/SID.parquet | 371 | 91.0% | 415 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SLDB.parquet | 284 | 70.5% | 320 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SLI.parquet | 396 | 93.6% | 337 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SMJF.parquet | 151 | 31.3% | 693 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 31.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SMR.parquet | 813 | 100.0% | 147 | 0 | 0 | 0 |  | 422 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/SOC.parquet | 409 | 97.2% | 550 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SOFI.parquet | 932 | 100.0% | 28 | 0 | 0 | 0 |  | 542 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/SONO.parquet | 344 | 85.1% | 275 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  |  | RTH coverage 85.1% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/SPCE.parquet | 492 | 100.0% | 467 | 0 | 0 | 0 |  | 101 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/SPRO.parquet | 146 | 32.8% | 630 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 32.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SPRU.parquet | 490 | 70.3% | 470 | 0 | 0 | 0 |  | 215 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SRAD.parquet | 321 | 78.2% | 430 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/STKE.parquet | 461 | 86.9% | 498 | 0 | 0 | 0 |  | 131 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/STTK.parquet | 291 | 72.8% | 391 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/SVM.parquet | 415 | 94.6% | 464 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/TDUP.parquet | 360 | 81.5% | 571 | 0 | 0 | 0 |  | 42 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/TE.parquet | 667 | 99.7% | 293 | 0 | 0 | 0 |  | 277 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/TGB.parquet | 417 | 98.2% | 529 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/THM.parquet | 317 | 73.1% | 544 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/TIGR.parquet | 358 | 81.0% | 602 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/TLRY.parquet | 474 | 92.3% | 483 | 0 | 0 | 0 |  | 114 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/TMC.parquet | 602 | 99.5% | 358 | 0 | 0 | 0 |  | 214 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/TME.parquet | 445 | 99.5% | 513 | 0 | 0 | 0 |  | 56 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/TRLV.parquet | 394 | 96.7% | 350 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/TRX.parquet | 433 | 99.7% | 525 | 0 | 0 | 0 |  | 43 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/TV.parquet | 244 | 61.3% | 212 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 61.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/UAMY.parquet | 528 | 100.0% | 431 | 0 | 0 | 0 |  | 137 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/ULCC.parquet | 339 | 81.5% | 406 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/URG.parquet | 443 | 98.2% | 514 | 0 | 0 | 0 |  | 59 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/USAS.parquet | 432 | 98.2% | 523 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/UUUU.parquet | 668 | 99.7% | 289 | 0 | 0 | 0 |  | 278 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/VFC.parquet | 404 | 99.7% | 256 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/VGZ.parquet | 512 | 96.2% | 267 | 0 | 0 | 0 |  | 136 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/VIR.parquet | 342 | 82.8% | 409 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  |  | RTH coverage 82.8% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/VISN.parquet | 412 | 97.7% | 517 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/VLN.parquet | 320 | 75.6% | 639 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/VNET.parquet | 471 | 99.5% | 477 | 0 | 0 | 0 |  | 83 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/VYX.parquet | 411 | 99.2% | 459 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-21 |
| 2026-09-21/VZLA.parquet | 398 | 96.2% | 545 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/WRN.parquet | 289 | 69.7% | 485 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/XE.parquet | 651 | 100.0% | 306 | 0 | 0 | 0 |  | 260 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/XERS.parquet | 337 | 83.1% | 507 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-21/XRAY.parquet | 411 | 99.5% | 546 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/XRX.parquet | 334 | 78.7% | 626 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  |  | RTH coverage 78.7% < 98%; no daily bar for 2026-09-21 |
| 2026-09-21/XXI.parquet | 539 | 99.5% | 417 | 0 | 0 | 0 |  | 150 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/YSS.parquet | 424 | 100.0% | 533 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-21/ZH.parquet | 304 | 75.4% | 311 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/AAL.parquet | 774 | 100.0% | 186 | 0 | 0 | 0 |  | 383 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ABSI.parquet | 544 | 99.7% | 416 | 0 | 0 | 0 |  | 155 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ACHR.parquet | 661 | 100.0% | 298 | 0 | 0 | 0 |  | 270 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ACRS.parquet | 341 | 81.8% | 420 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ADCT.parquet | 371 | 91.3% | 562 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ADTN.parquet | 310 | 76.9% | 431 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 76.9% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/AESI.parquet | 399 | 98.5% | 231 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/AG.parquet | 589 | 100.0% | 371 | 0 | 0 | 0 |  | 198 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/AI.parquet | 439 | 99.5% | 513 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ALEC.parquet | 273 | 68.5% | 328 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ALKT.parquet | 305 | 76.1% | 298 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 76.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/AMC.parquet | 651 | 100.0% | 309 | 0 | 0 | 0 |  | 260 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/AMPX.parquet | 473 | 99.7% | 479 | 0 | 0 | 0 |  | 83 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/AMRX.parquet | 416 | 97.4% | 531 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  |  | RTH coverage 97.4% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/ANGX.parquet | 359 | 90.0% | 263 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ANNX.parquet | 341 | 84.1% | 386 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ANVS.parquet | 360 | 90.5% | 480 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/APUS.parquet | 129 | 20.3% | 830 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 20.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ARHS.parquet | 337 | 83.1% | 414 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ARIS.parquet | 419 | 99.7% | 538 | 0 | 0 | 0 |  | 29 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ASM.parquet | 441 | 99.0% | 518 | 0 | 0 | 0 |  | 54 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ASPN.parquet | 348 | 87.2% | 508 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/AUTL.parquet | 273 | 63.3% | 658 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BB.parquet | 795 | 100.0% | 165 | 0 | 0 | 0 |  | 404 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BBAI.parquet | 613 | 100.0% | 347 | 0 | 0 | 0 |  | 222 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BBWI.parquet | 401 | 100.0% | 115 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BEKE.parquet | 400 | 98.0% | 524 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BFLY.parquet | 555 | 100.0% | 403 | 0 | 0 | 0 |  | 164 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BGC.parquet | 347 | 85.1% | 428 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 85.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/BGS.parquet | 331 | 82.3% | 624 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | RTH coverage 82.3% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/BHVN.parquet | 393 | 97.4% | 269 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BILI.parquet | 429 | 92.8% | 529 | 0 | 0 | 0 |  | 67 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BIOA.parquet | 329 | 79.2% | 602 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BKKT.parquet | 428 | 92.8% | 531 | 0 | 0 | 0 |  | 65 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BLMN.parquet | 386 | 95.1% | 327 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 95.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/BLND.parquet | 410 | 98.2% | 520 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BMEA.parquet | 449 | 71.8% | 479 | 0 | 0 | 0 |  | 178 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BOBS.parquet | 345 | 86.9% | 279 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BORR.parquet | 434 | 98.5% | 397 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BTG.parquet | 418 | 99.0% | 389 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BTGO.parquet | 424 | 96.7% | 498 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/BUR.parquet | 403 | 98.5% | 258 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/BYND.parquet | 398 | 75.9% | 561 | 0 | 0 | 0 |  | 104 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CANG.parquet | 180 | 43.9% | 561 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 43.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CAPR.parquet | 482 | 91.3% | 475 | 0 | 0 | 0 |  | 125 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CERT.parquet | 357 | 87.2% | 574 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 87.2% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/CHPT.parquet | 389 | 91.3% | 546 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CIFR.parquet | 779 | 100.0% | 181 | 0 | 0 | 0 |  | 389 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/CLF.parquet | 434 | 100.0% | 527 | 0 | 0 | 0 |  | 43 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/CMPS.parquet | 428 | 91.3% | 394 | 0 | 0 | 0 |  | 72 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CORZ.parquet | 505 | 100.0% | 452 | 0 | 0 | 0 |  | 115 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/COTY.parquet | 389 | 98.0% | 124 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  |  | RTH coverage 98.0% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/CPRI.parquet | 451 | 100.0% | 328 | 0 | 0 | 0 |  | 60 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/CTKB.parquet | 336 | 83.1% | 602 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  |  | RTH coverage 83.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/CTMX.parquet | 401 | 95.6% | 469 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CTNM.parquet | 269 | 65.6% | 478 | 0 | 0 | 0 |  | 12 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 65.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CWH.parquet | 374 | 94.6% | 72 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/CWK.parquet | 390 | 98.5% | 66 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/DC.parquet | 423 | 97.2% | 535 | 0 | 0 | 0 |  | 43 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/DDD.parquet | 353 | 84.9% | 585 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  |  | RTH coverage 84.9% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/DFH.parquet | 320 | 81.3% | 76 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  |  | RTH coverage 81.3% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/DNA.parquet | 420 | 98.0% | 487 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/DSP.parquet | 294 | 70.0% | 637 | 0 | 0 | 0 |  | 21 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/EAF.parquet | 354 | 85.9% | 453 | 0 | 0 | 0 |  | 18 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/EC.parquet | 339 | 81.8% | 448 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/EDIT.parquet | 369 | 86.7% | 370 | 0 | 0 | 0 |  | 30 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/EGHT.parquet | 254 | 62.1% | 677 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 62.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/ELME.parquet | 244 | 62.1% | 173 | 0 | 0 | 0 |  | 1 | 0 | 0 | 0 |  |  |  |  | RTH coverage 62.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/EMBC.parquet | 274 | 68.2% | 657 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  |  | RTH coverage 68.2% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/ENOV.parquet | 377 | 95.1% | 53 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  |  | RTH coverage 95.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/ENVX.parquet | 483 | 96.4% | 471 | 0 | 0 | 0 |  | 107 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/EQX.parquet | 462 | 100.0% | 496 | 0 | 0 | 0 |  | 71 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/EROC.parquet | 445 | 99.5% | 507 | 0 | 0 | 0 |  | 56 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ESRT.parquet | 386 | 98.0% | 194 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/EVGO.parquet | 419 | 94.4% | 512 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/EXK.parquet | 440 | 98.0% | 513 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/FDMT.parquet | 284 | 67.7% | 467 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 67.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/FEAM.parquet | 397 | 80.8% | 430 | 0 | 0 | 0 |  | 86 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/FIP.parquet | 260 | 64.9% | 341 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/FJET.parquet | 433 | 93.3% | 524 | 0 | 0 | 0 |  | 68 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/FOSL.parquet | 280 | 65.4% | 520 | 0 | 0 | 0 |  | 26 | 0 | 0 | 0 |  |  |  |  | RTH coverage 65.4% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/FRVO.parquet | 510 | 98.7% | 449 | 0 | 0 | 0 |  | 124 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/FSM.parquet | 410 | 99.2% | 540 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/FUBO.parquet | 344 | 84.4% | 431 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/GAU.parquet | 351 | 87.9% | 270 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/GCTS.parquet | 420 | 92.6% | 495 | 0 | 0 | 0 |  | 58 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/GEMI.parquet | 520 | 93.6% | 428 | 0 | 0 | 0 |  | 155 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/GENI.parquet | 427 | 100.0% | 487 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/GOGO.parquet | 290 | 68.0% | 486 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  |  | RTH coverage 68.0% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/GORO.parquet | 383 | 89.5% | 453 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/GRAB.parquet | 958 | 100.0% | 2 | 0 | 0 | 0 |  | 568 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/GRPN.parquet | 381 | 85.1% | 542 | 0 | 0 | 0 |  | 49 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/GT.parquet | 468 | 100.0% | 471 | 0 | 0 | 0 |  | 78 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/GTN.parquet | 252 | 63.8% | 237 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 63.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/HAFN.parquet | 447 | 95.4% | 462 | 0 | 0 | 0 |  | 74 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/HIMX.parquet | 359 | 77.2% | 582 | 0 | 0 | 0 |  | 58 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/HL.parquet | 520 | 100.0% | 437 | 0 | 0 | 0 |  | 129 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/HLF.parquet | 321 | 81.5% | 83 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/HLIT.parquet | 311 | 75.1% | 644 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  |  | RTH coverage 75.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/HLLY.parquet | 314 | 79.5% | 146 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/HMY.parquet | 476 | 99.5% | 483 | 0 | 0 | 0 |  | 87 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/HSAI.parquet | 378 | 87.4% | 577 | 0 | 0 | 0 |  | 38 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 87.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/HUYA.parquet | 273 | 69.0% | 357 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/HYLN.parquet | 422 | 98.7% | 528 | 0 | 0 | 0 |  | 36 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/IAUX.parquet | 442 | 99.5% | 340 | 0 | 0 | 0 |  | 53 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/IBRX.parquet | 614 | 100.0% | 346 | 0 | 0 | 0 |  | 224 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/IE.parquet | 399 | 94.9% | 376 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/IMSR.parquet | 490 | 88.5% | 349 | 0 | 0 | 0 |  | 144 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/INFQ.parquet | 703 | 100.0% | 257 | 0 | 0 | 0 |  | 312 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/INTR.parquet | 347 | 81.8% | 578 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/IRWD.parquet | 325 | 77.4% | 581 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  |  | RTH coverage 77.4% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/ITRG.parquet | 354 | 85.6% | 424 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/JBLU.parquet | 554 | 99.5% | 350 | 0 | 0 | 0 |  | 166 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/JELD.parquet | 379 | 85.1% | 479 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 85.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/JOBY.parquet | 739 | 100.0% | 221 | 0 | 0 | 0 |  | 348 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/KC.parquet | 310 | 72.3% | 647 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/KLRA.parquet | 335 | 81.3% | 482 | 0 | 0 | 0 |  | 17 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/KLXE.parquet | 211 | 51.3% | 395 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 51.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/KPTI.parquet | 298 | 71.8% | 633 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/KRO.parquet | 268 | 67.2% | 222 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 67.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/KSS.parquet | 403 | 99.5% | 234 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/LAC.parquet | 519 | 99.7% | 439 | 0 | 0 | 0 |  | 129 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/LAES.parquet | 711 | 96.9% | 243 | 0 | 0 | 0 |  | 333 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/LBRT.parquet | 403 | 99.7% | 518 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/LCID.parquet | 694 | 100.0% | 265 | 0 | 0 | 0 |  | 303 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/LEGN.parquet | 385 | 89.0% | 546 | 0 | 0 | 0 |  | 37 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 89.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/LI.parquet | 442 | 91.0% | 518 | 0 | 0 | 0 |  | 86 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/LILAK.parquet | 275 | 68.2% | 656 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/LION.parquet | 407 | 100.0% | 341 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/LODE.parquet | 395 | 90.5% | 389 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/LPL.parquet | 331 | 82.6% | 494 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 82.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/LVWR.parquet | 207 | 50.0% | 691 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 50.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/MBC.parquet | 370 | 94.1% | 75 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  |  | RTH coverage 94.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/MNRO.parquet | 330 | 81.3% | 329 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 81.3% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/MNSO.parquet | 358 | 86.7% | 464 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/MPT.parquet | 410 | 99.7% | 284 | 0 | 0 | 0 |  | 20 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/MRVI.parquet | 306 | 74.4% | 652 | 0 | 0 | 0 |  | 16 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 74.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/MX.parquet | 351 | 72.0% | 606 | 0 | 0 | 0 |  | 69 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/NABL.parquet | 372 | 93.3% | 227 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.3% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/NAK.parquet | 447 | 94.6% | 509 | 0 | 0 | 0 |  | 77 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/NAT.parquet | 436 | 99.2% | 514 | 0 | 0 | 0 |  | 48 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NEOG.parquet | 397 | 98.0% | 349 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  |  | RTH coverage 98.0% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/NEWP.parquet | 372 | 94.1% | 235 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/NG.parquet | 434 | 99.2% | 516 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NIO.parquet | 701 | 100.0% | 259 | 0 | 0 | 0 |  | 310 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NMAX.parquet | 289 | 71.0% | 387 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 71.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/NNVC.parquet | 302 | 61.0% | 603 | 0 | 0 | 0 |  | 63 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 61.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/NRGV.parquet | 412 | 98.2% | 484 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NTSK.parquet | 451 | 100.0% | 506 | 0 | 0 | 0 |  | 60 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NUVB.parquet | 396 | 98.7% | 481 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NVAX.parquet | 500 | 99.5% | 460 | 0 | 0 | 0 |  | 111 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NXDR.parquet | 397 | 98.0% | 453 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 98.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/NXE.parquet | 443 | 99.2% | 511 | 0 | 0 | 0 |  | 55 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/NXH.parquet | 355 | 80.0% | 604 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/OCTV.parquet | 385 | 92.6% | 526 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/OGG.parquet | 349 | 88.5% | 406 | 0 | 0 | 0 |  | 3 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 88.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/OPEN.parquet | 776 | 100.0% | 184 | 0 | 0 | 0 |  | 385 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/OPK.parquet | 297 | 64.9% | 572 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 64.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/OPTU.parquet | 311 | 78.5% | 160 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 78.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/ORIC.parquet | 291 | 66.4% | 612 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 66.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/PAAI.parquet | 843 | 100.0% | 117 | 0 | 0 | 0 |  | 452 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/PACB.parquet | 469 | 99.5% | 479 | 0 | 0 | 0 |  | 82 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/PAX.parquet | 296 | 73.6% | 312 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/PD.parquet | 367 | 91.5% | 242 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/PHAT.parquet | 301 | 73.3% | 437 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 73.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/PINS.parquet | 462 | 100.0% | 498 | 0 | 0 | 0 |  | 71 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/PL.parquet | 631 | 100.0% | 329 | 0 | 0 | 0 |  | 240 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/PLAY.parquet | 413 | 93.1% | 518 | 0 | 0 | 0 |  | 50 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/PLTK.parquet | 233 | 56.7% | 698 | 0 | 0 | 0 |  | 11 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 56.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/PONY.parquet | 505 | 96.9% | 454 | 0 | 0 | 0 |  | 129 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/PRGO.parquet | 367 | 93.8% | 24 | 0 | 0 | 0 |  | 0 | 0 | 0 | 0 |  |  |  |  | RTH coverage 93.8% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/PTON.parquet | 528 | 100.0% | 432 | 0 | 0 | 0 |  | 137 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/PWP.parquet | 325 | 81.5% | 276 | 0 | 0 | 0 |  | 6 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 81.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/QBTS.parquet | 853 | 100.0% | 107 | 0 | 0 | 0 |  | 462 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/QXO.parquet | 573 | 100.0% | 386 | 0 | 0 | 0 |  | 182 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/RARE.parquet | 483 | 99.7% | 476 | 0 | 0 | 0 |  | 93 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/RBBN.parquet | 172 | 41.0% | 775 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 41.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/RC.parquet | 320 | 80.5% | 378 | 0 | 0 | 0 |  | 5 | 0 | 0 | 0 |  |  |  |  | RTH coverage 80.5% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/RDW.parquet | 686 | 100.0% | 270 | 0 | 0 | 0 |  | 295 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/REPL.parquet | 390 | 92.0% | 541 | 0 | 0 | 0 |  | 31 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/RSKD.parquet | 439 | 86.4% | 401 | 0 | 0 | 0 |  | 101 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/RXRX.parquet | 756 | 100.0% | 203 | 0 | 0 | 0 |  | 366 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/RXT.parquet | 532 | 95.9% | 423 | 0 | 0 | 0 |  | 157 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/RYAM.parquet | 280 | 69.0% | 561 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 69.0% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/SANA.parquet | 403 | 91.5% | 532 | 0 | 0 | 0 |  | 45 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SB.parquet | 389 | 95.6% | 219 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SBH.parquet | 349 | 84.4% | 479 | 0 | 0 | 0 |  | 19 | 0 | 0 | 0 |  |  |  |  | RTH coverage 84.4% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/SDEV.parquet | 522 | 90.0% | 428 | 0 | 0 | 0 |  | 170 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SECZ.parquet | 606 | 100.0% | 350 | 0 | 0 | 0 |  | 215 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/SFIX.parquet | 394 | 86.2% | 386 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SG.parquet | 404 | 100.0% | 556 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/SGRY.parquet | 394 | 95.1% | 532 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SHEN.parquet | 238 | 58.5% | 646 | 0 | 0 | 0 |  | 10 | 0 | 0 | 0 |  |  |  |  | RTH coverage 58.5% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/SID.parquet | 332 | 84.4% | 304 | 0 | 0 | 0 |  | 2 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 84.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SLDB.parquet | 296 | 72.0% | 452 | 0 | 0 | 0 |  | 14 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 72.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SLI.parquet | 351 | 83.9% | 420 | 0 | 0 | 0 |  | 23 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 83.9% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SMJF.parquet | 314 | 70.0% | 634 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 70.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SMR.parquet | 777 | 100.0% | 182 | 0 | 0 | 0 |  | 385 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/SOC.parquet | 424 | 97.2% | 512 | 0 | 0 | 0 |  | 44 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SOFI.parquet | 932 | 100.0% | 28 | 0 | 0 | 0 |  | 541 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/SONO.parquet | 338 | 83.1% | 413 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  |  | RTH coverage 83.1% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/SPCE.parquet | 451 | 97.2% | 502 | 0 | 0 | 0 |  | 71 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SPRO.parquet | 427 | 91.3% | 520 | 0 | 0 | 0 |  | 75 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SPRU.parquet | 183 | 33.6% | 730 | 0 | 0 | 0 |  | 51 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 33.6% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SRAD.parquet | 408 | 96.4% | 322 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 96.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/STKE.parquet | 305 | 58.2% | 649 | 0 | 0 | 0 |  | 86 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 58.2% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/STTK.parquet | 274 | 68.0% | 327 | 0 | 0 | 0 |  | 8 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 68.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/SVM.parquet | 390 | 93.3% | 547 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/TDUP.parquet | 316 | 75.4% | 629 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/TE.parquet | 639 | 100.0% | 315 | 0 | 0 | 0 |  | 248 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/TGB.parquet | 431 | 100.0% | 412 | 0 | 0 | 0 |  | 40 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/THM.parquet | 292 | 69.0% | 409 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 69.0% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/TIGR.parquet | 376 | 86.7% | 581 | 0 | 0 | 0 |  | 39 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/TLRY.parquet | 528 | 97.4% | 432 | 0 | 0 | 0 |  | 147 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/TMC.parquet | 556 | 98.2% | 403 | 0 | 0 | 0 |  | 173 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/TME.parquet | 420 | 99.2% | 398 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/TRLV.parquet | 424 | 100.0% | 330 | 0 | 0 | 0 |  | 33 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/TRX.parquet | 420 | 93.8% | 498 | 0 | 0 | 0 |  | 53 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/TV.parquet | 320 | 80.8% | 360 | 0 | 0 | 0 |  | 4 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 80.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/UAMY.parquet | 477 | 99.2% | 480 | 0 | 0 | 0 |  | 89 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ULCC.parquet | 398 | 93.8% | 404 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 93.8% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/URG.parquet | 439 | 97.7% | 506 | 0 | 0 | 0 |  | 57 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 97.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/USAS.parquet | 410 | 94.4% | 547 | 0 | 0 | 0 |  | 41 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/UUUU.parquet | 612 | 100.0% | 343 | 0 | 0 | 0 |  | 221 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/VFC.parquet | 400 | 100.0% | 242 | 0 | 0 | 0 |  | 9 | 0 | 0 | 0 |  |  |  |  | no daily bar for 2026-09-22 |
| 2026-09-22/VGZ.parquet | 401 | 90.5% | 526 | 0 | 0 | 0 |  | 47 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 90.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/VIR.parquet | 345 | 81.8% | 574 | 0 | 0 | 0 |  | 25 | 0 | 0 | 0 |  |  |  |  | RTH coverage 81.8% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/VISN.parquet | 390 | 91.5% | 361 | 0 | 0 | 0 |  | 32 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 91.5% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/VLN.parquet | 409 | 77.7% | 547 | 0 | 0 | 0 |  | 105 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 77.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/VNET.parquet | 395 | 94.4% | 536 | 0 | 0 | 0 |  | 27 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 94.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/VYX.parquet | 398 | 98.0% | 289 | 0 | 0 | 0 |  | 15 | 0 | 0 | 0 |  |  |  |  | RTH coverage 98.0% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/VZLA.parquet | 401 | 95.4% | 362 | 0 | 0 | 0 |  | 28 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 95.4% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/WRN.parquet | 307 | 75.1% | 285 | 0 | 0 | 0 |  | 13 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 75.1% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/XE.parquet | 602 | 100.0% | 358 | 0 | 0 | 0 |  | 212 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/XERS.parquet | 361 | 86.7% | 599 | 0 | 0 | 0 |  | 22 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 86.7% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/XRAY.parquet | 410 | 99.0% | 544 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/XRX.parquet | 337 | 80.5% | 516 | 0 | 0 | 0 |  | 24 | 0 | 0 | 0 |  |  |  |  | RTH coverage 80.5% < 98%; no daily bar for 2026-09-22 |
| 2026-09-22/XXI.parquet | 419 | 92.3% | 511 | 0 | 0 | 0 |  | 58 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 92.3% < 98%; daily bar missing — envelope check skipped |
| 2026-09-22/YSS.parquet | 434 | 99.2% | 523 | 0 | 0 | 0 |  | 46 | 0 | 0 | 0 |  |  |  | Y | daily bar missing — envelope check skipped |
| 2026-09-22/ZH.parquet | 318 | 79.5% | 585 | 0 | 0 | 0 |  | 7 | 0 | 0 | 0 |  |  |  | Y | RTH coverage 79.5% < 98%; daily bar missing — envelope check skipped |

## Known expected patterns (not defects)

- **Thin-name minute sparsity (verified 2026-08-18):** Yahoo 1m emits
  a bar only when the name prints a trade/quote, so thinly-traded
  S&P 600 names show real RTH minute gaps (e.g. AAT ~30-55% RTH
  coverage) while liquid names are complete (AAPL/MSFT/SPY 390/390
  RTH). This is data reality, not a pipeline fault — measurement on
  thin names must resample (e.g. 5-min) or count RTH coverage.
- Pre-market span often starts later than 04:00 for thin names
  (Yahoo coverage); regular session 09:30-16:00 is the strict check.
- Envelope/volume tolerances absorb dividend adjustments on the
  adjusted daily bars; a *sustained* break across many files is the
  signature of an unrecorded split — record it in
  `data/intraday/splits.json` (procedure in the README).
- The archive starts fresh: earlier bar-dates are legitimately
  absent before enough nightly pulls have run.

_(end of QA report — 1581 files checked)_
