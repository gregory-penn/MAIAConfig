from GaudiKernel.Constants import INFO, WARNING, DEBUG


def _truth_track_finder(name, fit_mode, track_collection, relation_collection):
    """
    One TruthTrackFinder instance (TruthTracking repository, built against
    k4ActsTracking): the tracker hits are grouped by the MCParticle that made
    them and each group is turned into a track with fit_mode:
      * "CKF": the Combinatorial Kalman Filter (k4ActsTracking CKFRunner) over
               the particle's hits only, with the chi2 hit rejection of the
               standard CKF (settings copied from CKFTracker_cfg below)
      * "KF":  the Kalman fitter (k4ActsTracking KFRunner), every hit fitted

    It reads the same hits and hit links as the CKF, so it sees the same
    digitized (and, with --doTrackerConing, coned) hits. Its outputs are separate
    collections, so the standard CKF chain and SiTracks are unaffected:
      * track_collection:    the tracks
      * relation_collection: one TrackMCParticleLink per track, weight 1
    """
    # Imported here so that jobs without --doTruthTracking do not need the
    # TruthTracking library on LD_LIBRARY_PATH / PYTHONPATH.
    from Configurables import TruthTrackFinder

    return TruthTrackFinder(
        name,
        FitMode = fit_mode,
        InputTrackerHitCollection = ["MergedTrackerHits"],
        InputTrackerHitRelationCollection = ["MergedTrackerHitsRelations"],
        # No MCParticle input: each hit's particle is read from its SimTrackerHit,
        # so the output links point to MCParticles without overlay and to the
        # overlay's copy of the signal particles with overlay.
        OutputTrackCollection = [track_collection],
        OutputTrackRelationCollection = [relation_collection],
        MinHitsPerTrack = 3,
        MinTruePt = 0.,
        SkipSecondaryHits = True,
        # CKF hit rejection, as in CKFTracker_cfg (CKF_tracking.py). Only used
        # with FitMode "CKF". The branch stopper stays off: it exists to end fake
        # branches, and its pT cut would end low-pT truth tracks.
        CKF_Chi2CutOff = 10,
        CKF_Chi2CutOffOutlier = 25,
        CKF_NumMeasurementsCutOff = 2,
        # Same calorimeter-state settings as the CKF (CKF_tracking.py), so Pandora gets the same track states
        ExtrapolateToCalo = True,
        AddEndcapCaloState = True,
        OutputLevel = INFO,
    )


def TruthTracker_cfg(args):
    """
    The TruthTrackFinder instances for --truthTrackingFit:
      * "CKF"  (default): TruthTrackFinder   -> TruthTracks,   TruthTrackRelations
      * "KF":             TruthTrackFinderKF -> TruthTracksKF, TruthTrackRelationsKF
      * "both":           both of the above, in the same job
    Returns a list of algorithms.
    """
    algs = []
    if args.truthTrackingFit in ("CKF", "both"):
        algs.append(_truth_track_finder("TruthTrackFinder", "CKF", "TruthTracks", "TruthTrackRelations"))
    if args.truthTrackingFit in ("KF", "both"):
        algs.append(_truth_track_finder("TruthTrackFinderKF", "KF", "TruthTracksKF", "TruthTrackRelationsKF"))
    return algs
