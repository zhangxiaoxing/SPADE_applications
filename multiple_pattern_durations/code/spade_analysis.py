import elephant.spade as spade
import numpy as np
import os
import argparse
import neo
import quantities as pq
from mpi4py import MPI  # for parallelized routines
import yaml
from utils import mkdirp, split_path
from yaml import Loader

if __name__ == '__main__':
    #data_param = data_file['params']

    parser = argparse.ArgumentParser(description='Compute spade on artificial data '
                                                 'for the given winlen and sess_id parameters')
    parser.add_argument('winlen', metavar='winlen', type=int,
                       help='winlen parameter of the spade function')
    parser.add_argument('sess_id', metavar='sess_id', type=str,
                       help='sess_id parameter of the spade function')
    args = parser.parse_args()

    #    min_spikes = data_param['xi']
    #    max_spikes = data_param['xi']
    min_spikes = 10 
    max_spikes = 10

    with open("configfile.yaml", 'r') as stream:
        config = yaml.load(stream, Loader=Loader)
    n_surr = config['n_surr']
    binsize = 4 * pq.ms
    winlen = args.winlen
    sess_id = args.sess_id

    r=neo.io.NeoMatlabIO(filename='../data/spktO17_{}.mat'.format(sess_id))
    bl=r.read_block()
    data=bl.segments[0].spiketrains

    spectrum = '3d#'
    param = {'winlen': winlen,
             'n_surr': n_surr,
             'binsize': binsize,
             'spectrum': spectrum,
             'min_spikes': min_spikes,
             'max_spikes': max_spikes}
    # Check MPI parameters
    comm = MPI.COMM_WORLD   # create MPI communicator
    rank = comm.Get_rank()  # get rank of current MPI task
    size = comm.Get_size() # Get the total number of MPI processes
    print('Number of processes:{}'.format(size))

    # Compute spade res
    print('Running spade')
    spade_res = spade.spade(data,
                            binsize=binsize,
                            winlen=winlen,
                            n_surr=n_surr,
                            min_spikes=min_spikes,
                            max_spikes=max_spikes,
                            spectrum=spectrum,
                            alpha=1,
                            min_occ=10,
                            min_neu=10,
                            output_format='concepts',
                            psr_param=None)

    # Storing data
    res_path = '../results/{}/winlen{}'.format(sess_id, winlen)
    spectrum = '3d#'
    # Create path if not already existing
    path_temp = './'
    for folder in split_path(res_path):
        path_temp = path_temp + '/' + folder
        mkdirp(path_temp)

    np.save(res_path + '/data_results.npy', [spade_res, param])
