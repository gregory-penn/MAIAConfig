'''-------------------------------------------------------------'''
'''  Helpers for resolving digitiser input collections          '''
'''-------------------------------------------------------------'''
# The overlay algorithms rename their output collections, so a digitiser must
# read whichever collection sits at the end of the overlay chain.


def overlay_input(base_name, args):
    """
    Return the input collection list for a digitiser that nominally reads
    `base_name`, accounting for the overlay chain produced upstream:

      * if --doOverlayIP   -> "OverlayIP<base_name>"
      * elif --doOverlayFull -> "Overlay<base_name>"
      * else               -> "<base_name>" (raw simulation collection)

    IP takes precedence because, when both overlays run, the IP step is the
    last in the chain: it reads the BIB output ("Overlay*") and writes
    "OverlayIP*".
    """
    if getattr(args, "doOverlayIP", False):
        return ["OverlayIP" + base_name]
    if getattr(args, "doOverlayFull", False):
        return ["Overlay" + base_name]
    return [base_name]


def overlay_mc_particles(args):
    """
    Return the MCParticle collection that the calorimeter hit contributions point
    to after the overlay chain, following the same precedence as overlay_input:

      * if --doOverlayIP   -> "MCParticlesIP"  (OutputMCParticles of overlay_IP.py)
      * elif --doOverlayFull -> "NewMCParticles" (OutputMCParticles default of the
                                                  BIB overlay; with MergeMCParticles
                                                  False it holds the signal particles)
      * else               -> "MCParticles"

    The overlay copies the signal hits into new collections whose contributions
    point to its copy of the signal particles, so an algorithm that follows the
    contributions (e.g. Pandora's truth links) must read this collection.
    """
    if getattr(args, "doOverlayIP", False):
        return ["MCParticlesIP"]
    if getattr(args, "doOverlayFull", False):
        return ["NewMCParticles"]
    return ["MCParticles"]
