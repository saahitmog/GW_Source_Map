#!/bin/bash
echo 'Filtering Dataset ...'
fitscopy 'desidr9_galaxy_cspcat.fits[Joined][spec_z > -10 && MASS_BEST > 0.0]' \!desidr9_galaxy_cspcat_spec.fits
echo 'Filtered Dataset Created'