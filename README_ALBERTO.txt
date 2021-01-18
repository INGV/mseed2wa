Instructions of mseed2wa.py script.

(py37) Albertos-MacBook-Air:bin michelini$ ./mseed2wa.py -h
usage: mseed2wa.py [-h] [--outdir OUTDIR] [--outwavals] mseed_E mseed_N

positional arguments:
  mseed_E          provide the name of the E-component input mseed file (e.g.,
                   'IV.BRIS..HHE.mseed')
  mseed_N          provide the name of the N-component input mseed file (e.g.,
                   'IV.BRIS..HHN.mseed')

optional arguments:
  -h, --help       show this help message and exit
  --outdir OUTDIR  provide the name of the output directory (default, '.')
  --outwavals      output half peak-2-peak (default: False)
(py37) Albertos-MacBook-Air:bin michelini$

The script reads the two horizontal components (it does not strictly matter  which component is 
given forst since the components are read from the mseed files). 

It outputs the WA simulated into the current directory (default) or it can be sent into the outdir
directory using the option --outdir.

It also outputs the values (in mm) of the max-min half value for each component if the "--outwavals" option is used (Bool: true or False). By default is False.

Example: for station IV.BRIS.

(py37) Albertos-MacBook-Air:bin michelini$ ./mseed2wa.py ../notebooks/IV.BRIS..HHN.mseed ../notebooks/IV.BRIS..HHE.mseed --outdir ../WA_out --outwavals
E: 22.7927 N: 21.6225
(py37) Albertos-MacBook-Air:bin michelini$

The results of the run is two files 

(py37) Albertos-MacBook-Air:bin michelini$ ls -l ../WA_out
total 512
-rw-r--r--  1 michelini  staff  108032 Jan 15 16:08 IV.BRIS..HHE_WA.mseed
-rw-r--r--  1 michelini  staff  108032 Jan 15 16:08 IV.BRIS..HHN_WA.mseed
(py37) Albertos-MacBook-Air:bin michelini$ 

The files are in mseed format and "_WA" has been added.

The simulation is done using the following WA characteristics

paz_wa = {'sensitivity': 2800, 'zeros': [0j], 'gain': 1,
          'poles': [-6.2832 - 4.7124j, -6.2832 + 4.7124j]}


the deconvolution is done starting from velocity since only 1 zero is provided. the results have been fully cross-checked with those obtained currently using EW.


FOR THE DOCKER:

install miniconda  (see instructions at: https://docs.conda.io/en/latest/miniconda.html)

once conda is installed, install obspy (cf https://anaconda.org/conda-forge/obspy):

conda install -c conda-forge obspy

Insert the script mseed2wa.py script and test it.


 
