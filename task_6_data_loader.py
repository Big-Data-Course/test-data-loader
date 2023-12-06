from astropy.io import ascii
from astroquery.gaia import Gaia
from sys import argv
import os

def load_data(currentNodeNumber, numberOfNodes):
    currentNodeNumber -= 1
    numOfParts = 10
    generalEntriesCount = 1811709771
    for i in range(numOfParts):
        query = f"SELECT random_index, phot_g_mean_mag+5*log10(parallax / 1000)+5 AS mg, bp_rp, azero_gspphot, 1000.0/parallax AS dist FROM gaiadr3.gaia_source \
        WHERE parallax_over_error > 10\
        AND phot_g_mean_flux_over_error > 50\
        AND phot_rp_mean_flux_over_error > 20\
        AND phot_bp_mean_flux_over_error > 20\
        AND phot_bp_rp_excess_factor < 1.3+0.06*power(phot_bp_mean_mag-phot_rp_mean_mag,2)\
        AND phot_bp_rp_excess_factor > 1.0+0.015*power(phot_bp_mean_mag-phot_rp_mean_mag,2)\
        AND visibility_periods_used > 8\
        AND astrometric_chi2_al/(astrometric_n_good_obs_al-5) < 1.44*greatest(1,exp(-0.4*(phot_g_mean_mag-19.5)))\
        AND random_index BETWEEN " + str(int((i + currentNodeNumber * numOfParts) * (1.0 / (numberOfNodes * numOfParts)) * generalEntriesCount))\
        + " AND " + str(int((i + currentNodeNumber * numOfParts + 1) * (1.0 / (numberOfNodes * numOfParts)) * generalEntriesCount) - 1)

        print(str(int(i + currentNodeNumber * numOfParts)))
        job     = Gaia.launch_job_async(query)
        results = job.get_results()
        #print(currentNodeNumber)
        print(f'Table size (rows): {len(results)}')

        filename = 'result/result_3_' + str(i + currentNodeNumber * numOfParts)
        ascii.write(results, filename, overwrite=True)

if __name__ == "__main__":
    if not os.path.exists("loaded_data"):
        os.makedirs("loaded_data")
    scriptPath, currentNodeNumber, numberOfNodes = argv
    load_data(int(currentNodeNumber), int(numberOfNodes))