# GREAT3 galaxy sample
======================

This directory contains scripts that were used to produce the galaxy catalogs
and selection criteria for GREAT3.  This process can be roughly divided into two
steps:

1. Making a COSMOS galaxy sample to I<23.5 with associated files for parametric
files.  The outputs of this process were packaged and made available on the
GREAT3 download page, http://great3.projects.phys.ucl.ac.uk/leaderboard/data

2. Calculating additional quantities that were needed to cut the sample in
various ways, for example, to ensure the galaxy images were within our target
S/N range, were sufficiently resolved in the ground-based simulated images, were
not too contaminated by blends or image defects, etc.

Below we describe the steps in and files associated with both of these
processes.


## Files related to the basic COSMOS I<23.5 sample
--------------------------------------------------

The first step in the processing is based on legacy code from the SHERA software
package.  It consists of five IDL scripts, the inputs for which are not
available here, so they are primarily made available for users to see what was
done.

1. `make_shera_cat.pro` was used to put together a catalog listing all galaxies
in the F814W<23.5 sample, in a format that can be used by SHERA.

2. `run_many.pro` was used to drive the three scripts below, in sequence, to
generate the postage stamps and a GalSim-style catalog representing the galaxy
sample.  The calling sequence is described in comments at the top of the script
itself.

3. `makecatalog_many.pro` is the first script driven by `run_many.pro`.  It
takes the SHERA catalog, and puts it into the format needed by GalSim.

4. `makestamps_many.pro` is the second script driven by `run_many.pro`.  It
creates postage stamps for all the galaxies in the proper format, and calculates
their noise properties (variance).

5. `makecatalog_many_var.pro` is the third script driven by `run_many.pro`.  It
adds the noise variances from step (4) to the catalogs from step (3).
After this step, we have a catalog that GalSim can read and use, along with the
galaxy postage stamp images and PSF images.

6. `make_fits_catalog.py` takes information about parametric fits to the galaxy
light profiles, and combines the info from several files into a single coherent
catalog with entries in an order corresponding to the output of (5).  Users will
not be able to run it because they won't have the inputs, but it is provided as
a record of how this process was done.

7. `check_catalog.py` is a script with some sanity checks of the catalog
properties: histograms of galaxy properties, and so on.  It is run on the
catalogs that are publicly available, so people who are interested can run it
themselves (after changing a single line in the script to specify the location
of the catalogs on their system).


## Files related to the additional selection criteria
-----------------------------------------------------

1. `shape_2comp.py` determines the effective shapes of the 2-component galaxy
models.  For galaxies for which we use a single Sersic profile, the isophotes
are elliptical and we can just use the fit parameters for that Sersic profile to
determine the shape.  For 2-component galaxies we have to make the images and
measure their shapes directly using adaptive moments.  The purpose is to get
shapes we can use when defining the B-mode shape noise field.  While what we
have here is not perfect (for two-component models the shape will depend on the
radial weight) it should be good enough for these purposes.

2. `check_failure.py` investigates the 3% of objects for which measurement in
the previous step failed.  The goal is to determine if they are a particularly
weird subset of the sample, or just random failures.  The answer seems to be
that there are slight trends in Sersic n (preferentially low n failures) and
radius, but nothing very strong.  Since it's only 3% of objects lost, we will
just get rid of them.

3. `training_galaxy_props.py` computes several quantities that are needed for
selection of galaxies in the GREAT3 simulations.  It takes a target PSF as an
argument, and for that target PSF, makes a simulation of each galaxy with that
target PSF.  Then it uses the images to answer the following questions: (a) What
noise variance should we add if we want to achieve S/N=20 using an optimal S/N
estimator? (b) What is the resolution factor for that PSF and galaxy?  (c) What
fraction of the galaxy flux is contained in our postage stamp size?  These
outputs are saved to catalogs, to be used in GREAT3 galaxy selection.

4. `run_props.py` takes some command-line arguments for the PSF and pixel scale,
and runs `training_galaxy_props.py`.  See the docstring for this file for
details as to how the script was run for GREAT3, i.e., which PSFs did we choose
to simulate.  There were six PSFs and hence six runs of `run_props.py`.

5. `combine_info.py` takes the outputs of `run_props.py` and combines them into
a single file that is used by the GREAT3 simulation scripts to select galaxies.
It applies cuts for basic measurement failures, after which we can use 54456 out
of 56062 galaxies, or 97%.

6. `training_galaxy_props_real.py` works like `training_galaxy_props.py`, and
computes two additional quantities that were later found to be necessary for
using the real galaxy sample (as opposed to the parametric fits).  These are:
(a) the S/N within an elliptical Gaussian filter on the original image, and (b)
the minimum noise variance after noise whitening to eliminate correlated noise
in the simulated image.  If (a) is too low, that can indicate some issue with
the galaxy image that makes it unusable.  If (b) is too high compared to the
noise variance we want to add, then we cannot use a galaxy in our simulation
with our desired S/N limit.  In practice, this script was also run by
`run_props.py` using the same command-line arguments, and the information in
those outputs was combined using `combine_image_info.py` (see below).

7. `combine_image_info.py` takes the outputs of the previous script for 6
different PSFs defined in `run_props.py`, and combines them into a single file
that is used by the GREAT3 simulation scripts to select galaxies for which the
use of real galaxy images is not problematic in some way.
