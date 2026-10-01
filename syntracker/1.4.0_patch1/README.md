  # Modification

  This version pins SynTracker's R stack to the versions SynTracker 1.4.0 was written for
  (upstream `SynTracker_env.yml`: `r-base=4.0.5`, `r-tidyverse=1.3.0`), with
  `bioconductor-decipher=2.18.1` (the R 4.0 build) and `r-rsqlite` made explicit.

  `1.4.0` installed these dependencies unpinned and resolved a current DECIPHER (3.x). SynTracker's
  `Seqs2DB(..., <file path>, ...)` call fails on every region with that version
  (`N function calls resulted in an error`), after which SynTracker crashes in `left_join()`.

  The final `RUN` step is a build-time smoke test of that exact `Seqs2DB` + `FindSynteny` path, so a
  future rebuild that drifts to a different DECIPHER fails at build time.

  ## amd64 only

  The R 4.0-matched DECIPHER has no `linux-aarch64` build. Build with:

      ./build.py build-push --platforms linux/amd64 syntracker 1.4.0_patch1

  ## patch1

  This was selected as an addition to the container version, but the SynTracker version remains
  identical - `1.4.0`.
