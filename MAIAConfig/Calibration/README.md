# Pandora theta-energy calibration tables

Used only with `--pandoraCalibration default` (off by default).

- `ecal_theta_energy_calib.json`: EM branch, trained on single photons
- `hadronic_theta_energy_calib.json`: hadronic branch, trained on single pions

Produced with pandora-calibration-tools
(`make_ecal_theta_energy_calibration.py`, `make_hcal_theta_energy_calibration.py`)
from Marlin (LCIO) reconstruction: the EM table from the MAIA_v0 v6 photon gun
production plus v2.11 transition-region photon samples, the hadronic table from
v2.11 pion gun samples. They were trained with ECalToEM = 1.02373335516,
ECalToHad = 1.38, HCalToHad = 1.25 and software compensation off. The
calibration switches Pandora to these values when enabled; see
`Common/pandora_calibration.py`.

Clusters below a table's lowest energy edge (30 GeV for EM, 10 GeV for
hadronic) or outside its theta range (the EM table covers 0.15 to 2.99 rad)
are not corrected. Clusters above the top energy edge use the last bin.

## Perfect-clustering tables (hit-iso)

- `perfectClustering_ecal_theta_energy_calib.json`: EM branch, single photons
- `perfectClustering_hadronic_theta_energy_calib.json`: hadronic branch, single charged pions

Trained 2026-11-22 with pandora-calibration-tools (EDM4hep input) on v3.1 reconstruction with
`PandoraSettings_perfectClustering.xml` (PerfectClustering, no BIB): 1-5000 GeV and 1-100 GeV samples,
theta 10-170 deg, flat constants ECalToEM = 1.02373335516, ECalToHad = 1.38, HCalToHad = 1.25 (the
values in `CALIBRATED_PANDORA_CONSTANTS`). Use with
`--pandoraCalibration perfectClustering_ecal_theta_energy_calib.json,perfectClustering_hadronic_theta_energy_calib.json`
and a perfect-clustering Pandora settings XML; they are not valid for the standard clustering.
