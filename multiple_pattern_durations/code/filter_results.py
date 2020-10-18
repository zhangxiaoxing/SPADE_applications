import numpy as np
import elephant.spade as spade
import quantities as pq
import argparse
import yaml
from yaml import Loader


# Function to filter patterns when the output format of spade function
# is 'patterns'
def _pattern_spectrum_filter(patterns, ns_signature, spectrum, winlen):
    """
    Filter to select concept which signature is significant
    """
    if spectrum == '3d#':
        keep_concept = patterns['signature'] + tuple([max(
                np.abs(np.diff(np.array(patterns['lags']) % winlen)))]) \
                       not in ns_signature
    else:
        keep_concept = patterns['signature'] not in ns_signature

    return keep_concept


if __name__ == '__main__':
    # Load parameters dictionary
    binsize = 4 * pq.ms 
    # Filtering parameters
    # Load general parameters
    with open("configfile.yaml", 'r') as stream:
        config = yaml.load(stream, Loader=Loader)
    alpha = config['alpha']
    psr_param = config['psr_param']
    correction = config['correction']
    min_occ = config['min_occ']
    # Passing spectrum parameter
    parser = argparse.ArgumentParser(description='Compute spade on artificial data'
                                                 ' for the given winlen and '
                                                 'sess_id parameters')
    parser.add_argument('sess_id', metavar='sess_id', type=str,
                       help='sess_id parameter of the spade function')
    parser.add_argument('winlen', metavar='winlen', type=int,
                       help='winlen parameter of the spade function')

    args = parser.parse_args()
    sess_id = args.sess_id
    winlen = args.winlen
    # Filtering parameters for the different window length
    # Loading result
    res_spade, params = \
        np.load('../results/{}/winlen{}/data_results.npy'.format(sess_id,
                                                                     winlen),
                encoding='latin1',allow_pickle=True)
    concepts = res_spade['patterns']
    pval_spectrum  = res_spade['pvalue_spectrum']
    # SPADE parameters
    spectrum = params['spectrum']
    min_spikes = params['min_spikes']
    n_surr = params['n_surr']
    # PSF filtering
    if len(pval_spectrum) == 0:
        ns_sgnt = []
    else:
        # Computing non-significant entries of the spectrum applying
        # the statistical correction
        ns_sgnt = spade.test_signature_significance(
            pval_spectrum, concepts, alpha, winlen, corr=correction, report='non_significant',
            spectrum=spectrum)
    concepts_psf = list(filter(
        lambda c: spade._pattern_spectrum_filter(
            c, ns_sgnt, spectrum, winlen), concepts))
    print('Winlen:', winlen)
    print('Non significant signatures:', sorted(ns_sgnt))
    print('Number of significant patterns before psr:', len(concepts_psf))
    # PSR filtering
    # Decide whether filter the concepts using psr
    if psr_param is not None:
        # Filter using conditional tests (psr)
        if 0 < alpha < 1 and n_surr > 0:
            concepts_psr = spade.pattern_set_reduction(concepts_psf, ns_sgnt,
                                                       winlen=winlen,
						       spectrum=spectrum,
                                                       h_subset_filtering=psr_param[0],
                                                       k_superset_filtering=psr_param[1],
                                                       l_covered_spikes=psr_param[2],
                                                       min_spikes=min_spikes,
                                                       min_occ=min_occ)
        else:
            concepts_psr = spade.pattern_set_reduction(concepts_psf, [],
                                                       winlen=winlen,
						       spectrum=spectrum,
                                                       h_subset_filtering=psr_param[0],
                                                       k_superset_filtering=psr_param[1],
                                                       l_covered_spikes=psr_param[2],
                                                       min_spikes=min_spikes,
                                                       min_occ=min_occ)
        patterns = spade.concept_output_to_patterns(
            concepts_psr, winlen, binsize, pval_spectrum)
        print('Number of significant patterns after psr:', len(concepts_psr))
    else:
        patterns = spade.concept_output_to_patterns(
            concepts_psf, winlen, binsize, pval_spectrum)

    # Storing filtered results
    params['alpha'] = alpha
    params['psr_param'] = psr_param
    params['correction'] = correction
    params['min_occ'] = min_occ
    np.save(
        '../results/{}/winlen{}/filtered_patterns.npy'.format(
            sess_id, winlen), [patterns, pval_spectrum, ns_sgnt, params])
