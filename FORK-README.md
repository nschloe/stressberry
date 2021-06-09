# FORK README

## Fork Reason

This fork exists to support showing test results from my blog [www.martinrowan.co.uk](https://www.martinrowan.co.uk). Specifcally as the upstream project has been making some dramatic changes to the appearance of the charts and had removed some functionality I relied upon.

## What This Fork Provides
Compared to the upstream project this fork offers:
 - Example Helpers for:
   - plotting individual and comparison charts. `helpers\plot-individual.sh` and `helpers\plot-compare.sh`
   - running a series of incremental load tests: `helpers\runtest.sh`
   - simply getting the min, max and varience for a specific metric from a test run: `helpers\show-metric.py`
 - Reinstated lost command line arguments:
   - `--hide legend` to hide the legend
   - `-lw` `--line-width` to allow the thickness of the lines plotted to be configurable
 - Added new command line options for new features:
   - `--legacy-style` changes the graph style to the original used in previous versions of stressberry, not the new dufte style
   - `--color-blind-friendly` changes the color pallet used in the charts to matplotlib.style tableau-colorblind10 (only with `--legacy style`)

If you have other suggestions, please let me know

Martin
