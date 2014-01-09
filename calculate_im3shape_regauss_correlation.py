#!/usr/bin/env python
import os
import sys
import numpy as np
sys.path.append(os.path.join("..", "server", "great3"))
import evaluate

EXPERIMENT = "control"
OBS_TYPE = "ground"
SHEAR_TYPE = "constant"

# Paths to control-ground-constant filenames (im3shape score ~225, regauss score ~ 68), make sure
# these are present!
I3FILE = os.path.join("results", "cogs-im3shape-im3shape-0-2013-10-18T15:46:28.199250+00:00.g3")
RGFILE = os.path.join(
    "results", "great3_ec-regauss-example-example_1-2013-12-27T15:24:57.472170+00:00.g3")

TRUTH_DIR = "/Users/browe/great3/beta/truth" # Modify to wherever truth is unpacked


if __name__ == "__main__":

    # Load up relevant data
    i3data = np.loadtxt(I3FILE)
    rgdata = np.loadtxt(RGFILE)
    subfield_index, g1true, g2true = evaluate.get_generate_const_truth(
        EXPERIMENT, OBS_TYPE, truth_dir=TRUTH_DIR)
    rotations = evaluate.get_generate_const_rotations(EXPERIMENT, OBS_TYPE, truth_dir=TRUTH_DIR)
    # Calculate m and c factors
    qi3, cpi3, mpi3, cxi3, mxi3, sigcpi3, sigmpi3, sigmxi3, sigcxi3 = evaluate.q_constant(
        I3FILE, EXPERIMENT, OBS_TYPE, truth_dir=TRUTH_DIR)
    qrg, cprg, mprg, cxrg, mxrg, sigcprg, sigmprg, sigmxrg, sigcxrg = evaluate.q_constant(
        RGFILE, EXPERIMENT, OBS_TYPE, truth_dir=TRUTH_DIR)
    # Rotate these c and m
    c1i3 = cpi3 * np.cos(2. * rotations) - cxi3 * np.sin(2. * rotations)
    c2i3 = cpi3 * np.sin(2. * rotations) + cxi3 * np.cos(2. * rotations)
    m1i3 = mpi3 * np.cos(2. * rotations) - mxi3 * np.sin(2. * rotations)
    m2i3 = mpi3 * np.sin(2. * rotations) + mxi3 * np.sin(2. * rotations)
    c1rg = cprg * np.cos(2. * rotations) - cxrg * np.sin(2. * rotations)
    c2rg = cprg * np.sin(2. * rotations) + cxrg * np.cos(2. * rotations)
    m1rg = mprg * np.cos(2. * rotations) - mxrg * np.sin(2. * rotations)
    m2rg = mprg * np.sin(2. * rotations) + mxrg * np.sin(2. * rotations)
    # Calculate bias model using these m and c values
    g1i3model = (1. + m1i3) * g1true + c1i3 
    g2i3model = (1. + m2i3) * g2true + c2i3
    g1rgmodel = (1. + m1rg) * g1true + c1rg 
    g2rgmodel = (1. + m2rg) * g2true + c2rg
    # Then get the bias model corrected differences
    g1i3 = i3data[:, 1]
    g2i3 = i3data[:, 2]
    g1rg = rgdata[:, 1]
    g2rg = rgdata[:, 2]
    d1i3 = g1i3 - g1i3model
    d2i3 = g2i3 - g2i3model
    d1rg = g1rg - g1rgmodel
    d2rg = g2rg - g2rgmodel
    # Calculate covariance matrices
    cov1 = np.cov(d1i3, d1rg) 
    cov2 = np.cov(d2i3, d2rg)
    # Calculate correlation coefficient
    rho1 = cov1[1, 0] / np.sqrt(cov1[0, 0] * cov1[1, 1])
    rho2 = cov2[1, 0] / np.sqrt(cov2[0, 0] * cov2[1, 1])
    print "Correlation coefficient (g1) rho = "+str(rho1) 
    print "Correlation coefficient (g2) rho = "+str(rho2) 
