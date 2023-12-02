from astropy.io import ascii
from astroquery.gaia import Gaia
from sys import argv
import os

def load_data(currentNodeNumber, numberOfNodes):
    currentNodeNumber -= 1
    numOfParts = 25
    generalEntriesCount = 1811709771
    for i in range(numOfParts):
        query = f"SELECT random_index, \
                ra, \
                ra_error, \
                pmra, \
                pmra_error, \
                dec, \
                dec_error, \
                pmdec, \
                pmdec_error, \
                parallax, \
                parallax_error, \
                parallax_over_error, \
                phot_g_mean_mag, \
                phot_g_mean_flux_over_error, \
                phot_rp_mean_mag, \
                phot_rp_mean_flux_over_error, \
                phot_bp_mean_mag, \
                phot_bp_mean_flux_over_error, \
                visibility_periods_used, \
                astrometric_matched_transits, \
                astrometric_n_obs_al, \
                astrometric_n_obs_ac, \
                bp_rp, \
                phot_bp_rp_excess_factor, \
                astrometric_chi2_al, \
                astrometric_n_good_obs_al, \
                azero_gspphot, \
                phot_g_mean_mag+5*log10(parallax)-10 AS mg, \
                1000.0/parallax AS dist \
            FROM gaiadr3.gaia_source \
            WHERE ra IS NOT NULL \
                AND ra_error IS NOT NULL \
                AND pmra IS NOT NULL \
                AND pmra_error IS NOT NULL \
                AND dec IS NOT NULL \
                AND dec_error IS NOT NULL \
                AND pmdec IS NOT NULL \
                AND pmdec_error IS NOT NULL \
                AND parallax IS NOT NULL \
                AND parallax_error IS NOT NULL \
                AND parallax_over_error IS NOT NULL \
                AND phot_g_mean_mag IS NOT NULL \
                AND phot_g_mean_flux_over_error IS NOT NULL \
                AND phot_rp_mean_mag IS NOT NULL \
                AND phot_rp_mean_flux_over_error IS NOT NULL \
                AND phot_bp_mean_mag IS NOT NULL \
                AND phot_bp_mean_flux_over_error IS NOT NULL \
                AND visibility_periods_used IS NOT NULL \
                AND astrometric_matched_transits IS NOT NULL \
                AND astrometric_n_obs_al IS NOT NULL \
                AND astrometric_n_obs_ac IS NOT NULL \
                AND bp_rp IS NOT NULL \
                AND phot_bp_rp_excess_factor IS NOT NULL \
                AND astrometric_chi2_al IS NOT NULL \
                AND astrometric_n_good_obs_al IS NOT NULL \
                AND azero_gspphot IS NOT NULL \
                AND parallax_over_error > 10 \
                AND phot_g_mean_flux_over_error > 50 \
                AND phot_rp_mean_flux_over_error > 20 \
                AND phot_bp_mean_flux_over_error > 20 \
                AND phot_bp_rp_excess_factor < 1.3+0.06*power(phot_bp_mean_mag-phot_rp_mean_mag,2) \
                AND phot_bp_rp_excess_factor > 1.0+0.015*power(phot_bp_mean_mag-phot_rp_mean_mag,2) \
                AND visibility_periods_used > 8 \
                AND astrometric_chi2_al/(astrometric_n_good_obs_al-5) < 1.44*greatest(1,exp(-0.4*(phot_g_mean_mag-19.5))) \
                AND random_index BETWEEN " + str(int((i + currentNodeNumber * numOfParts) * (1.0 / (numberOfNodes * numOfParts)) * generalEntriesCount))\
                + " AND " + str(int((i + currentNodeNumber * numOfParts + 1) * (1.0 / (numberOfNodes * numOfParts)) * generalEntriesCount) - 1)

        job     = Gaia.launch_job_async(query)
        results = job.get_results()
        print(i)
        print(f'Table size (rows): {len(results)}')

        filename = 'loaded_data/data_dr3_' + str(i + currentNodeNumber * numOfParts)
        ascii.write(results, filename, overwrite=True)

if __name__ == "__main__":
    if not os.path.exists("loaded_data"):
        os.makedirs("loaded_data")
    scriptPath, currentNodeNumber, numberOfNodes = argv
    load_data(int(currentNodeNumber), int(numberOfNodes))