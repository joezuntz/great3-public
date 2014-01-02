"""@file tabulate_variable_shear_metric_rev1.py

Tabulate values of the new variable shear metrics (revision 1: Dec 13/Jan 14) for given biases, for
inclusion in the GREAT3 Handbook.
"""

import sys
import os
import tempfile
import numpy as np
import g3metrics
path, module = os.path.split(__file__)
sys.path.append(os.path.join(path, "..", "server", "great3")) # Appends the folder
                                                              # great3-private/server/great3 to
                                                              # sys.path
import evaluate
import test_evaluate

NTEST = 10
NGALS_PER_IMAGE = 10000
NOISE_SIGMA = {"ground": 0.15, "space": 0.10}
CVALS = evaluate.CFID * 10.**(.5 * np.arange(5))
MVALS = evaluate.MFID * 10.**(.5 * np.arange(5))

TRUTH_DIR = "/Users/browe/great3/beta/truth" # Modify to wherever truth is unpacked

EXPERIMENT = "control" # Use the control truth values


if __name__ == "__main__":

    # Dicts containing arrays for storing Q_c values versus m and c, for ground and space
    qc = {"ground": np.empty((NTEST, len(CVALS))), "space": np.empty((NTEST, len(CVALS)))}
    qm = {"ground": np.empty((NTEST, len(MVALS))), "space": np.empty((NTEST, len(MVALS)))}
    coutfile = os.path.join("results", "tabulated_variable_Q_v_versus_c_norm1.pkl")
    moutfile = os.path.join("results", "tabulated_variable_Q_v_versus_m_norm1.pkl")

    if not os.path.isfile(coutfile):
        for obs_type in ("ground", "space",):

            print "Calculating Q_v values versus c for control-"+obs_type+"-variable data in GREAT3"
            print "NOISE_SIGMA = "+str(NOISE_SIGMA[obs_type])
            # First we build the truth table
            print "Building truth tables for control-"+obs_type+"-variable"
            # Get the x,y, true intrinsic ellips and shears for making fake submissions
            _, x, y, g1true, g2true = test_evaluate.get_variable_gtrue(
                EXPERIMENT, obs_type, truth_dir=TRUTH_DIR)
            _, _, _, g1int, g2int = test_evaluate.get_variable_gsuffix(
                EXPERIMENT, obs_type, truth_dir=TRUTH_DIR)           
            for jc, cval in enumerate(CVALS):

                for itest in xrange(NTEST):

                    # Build the submission
                    fdsub, subfile = tempfile.mkstemp(suffix=".dat")
                    result = test_evaluate.make_variable_submission(
                        x, y, g1true, g2true, g1int, g2int, cval, cval, evaluate.MFID,
                        evaluate.MFID, outfile=subfile, noise_sigma=NOISE_SIGMA[obs_type])
                    os.close(fdsub)
                    # Then evaluate Q_v
                    qc[obs_type][itest, jc] = evaluate.q_variable(
                        subfile, EXPERIMENT, obs_type, usebins=evaluate.USEBINS,
                        truth_dir=TRUTH_DIR)
                    os.remove(subfile)
                    print "Test %4d / %4d (c = %.3e) Q_v = %.4f" % (
                        itest+1, NTEST, cval, qc[obs_type][itest, jc])

                print "Mean Q_v = "+str(qc[obs_type][:, jc].mean())+" for "+str(NTEST)+\
                        " sims (with c = "+str(cval)+", obs_type = "+str(obs_type)+")"
                print

        import cPickle
        print "Saving pickled Q_v versus c dict to "+coutfile
        with open(coutfile, "wb") as fout:
            cPickle.dump(qc, fout)
        print

    if not os.path.isfile(moutfile):
        for obs_type in ("ground", "space",):

            print "Calculating Q_v values versus m for control-"+obs_type+"-variable data in GREAT3"
            print "NOISE_SIGMA = "+str(NOISE_SIGMA[obs_type])
            # First we build the truth table
            print "Building truth tables for control-"+obs_type+"-variable"
            # Get the x,y, true intrinsic ellips and shears for making fake submissions
            _, x, y, g1true, g2true = test_evaluate.get_variable_gtrue(
                EXPERIMENT, obs_type, truth_dir=TRUTH_DIR)
            _, _, _, g1int, g2int = test_evaluate.get_variable_gsuffix(
                EXPERIMENT, obs_type, truth_dir=TRUTH_DIR)
            for jm, mval in enumerate(MVALS):

                for itest in xrange(NTEST):

                    # Build the submission
                    fdsub, subfile = tempfile.mkstemp(suffix=".dat")
                    result = test_evaluate.make_variable_submission(
                        x, y, g1true, g2true, g1int, g2int, evaluate.CFID, evaluate.CFID, mval,
                        mval, outfile=subfile, noise_sigma=NOISE_SIGMA[obs_type])
                    os.close(fdsub)
                    # Then evaluate Q_v
                    qm[obs_type][itest, jm] = evaluate.q_variable(
                        subfile, EXPERIMENT, obs_type, usebins=evaluate.USEBINS,
                        truth_dir=TRUTH_DIR)
                    os.remove(subfile)
                    print "Test %4d / %4d (m = %.3e) Q_v = %.4f" % (
                        itest+1, NTEST, mval, qm[obs_type][itest, jm])

                print "Mean Q_v = "+str(qm[obs_type][:, jm].mean())+" for "+str(NTEST)+\
                    " sims (with m = "+str(mval)+", obs_type = "+str(obs_type)+")"
                print

        import cPickle
        print "Saving pickled Q_v versus m dict to "+moutfile
        with open(moutfile, "wb") as fout:
            cPickle.dump(qm, fout)
        print

    print ""
    print "Table of Q_v (ground sims) at constant m = mfid = "+str(evaluate.MFID)
    print "    c        Q   "
    for c, Q in zip(CVALS, np.mean(qc["ground"], axis=0)):

        print "{:8f} {:8.3f}".format(c, Q)

    print ""
    print "Table of Q_v (space sims) at constant m = mfid = "+str(evaluate.MFID)
    print "    c        Q   "
    for c, Q in zip(CVALS, np.mean(qc["space"], axis=0)):

        print "{:8f} {:8.3f}".format(c, Q)

    print ""
    print "Table of Q_v (ground sims) at constant c = cfid = "+str(evaluate.CFID)
    print "    m        Q   "
    for m, Q in zip(MVALS, np.mean(qm["ground"], axis=0)):

        print "{:8f} {:8.3f}".format(m, Q)

    print ""
    print "Table of Q_v (space sims) at constant c = cfid = "+str(evaluate.CFID)
    print "    m        Q   "
    for m, Q in zip(MVALS, np.mean(qm["space"], axis=0)):

        print "{:8f} {:8.3f}".format(m, Q)

    



