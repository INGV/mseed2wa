#!/usr/bin/env python
# coding: utf-8
#
# this simple routine converts from provided mseed files to WA using the
# standard values for Wood-Anderson
#
import os
import argparse
import sys

from math import log10

from obspy.clients.fdsn import Client
from obspy.core import UTCDateTime
from obspy import Stream, Trace, read
from obspy import read_inventory
#
paz_wa = {'sensitivity': 2800, 'zeros': [0j], 'gain': 1,
          'poles': [-6.2832 - 4.7124j, -6.2832 + 4.7124j]}



def remove_response(st, pre_filt, invstacha, plot=False):

    # preprocessing in the time-domain
    stccNZ = st.copy()
    # print stcc[0].data
    stccNZ.detrend(type="linear")
    stccNZ.detrend(type="demean")
    stccNZ.taper(max_percentage=0.05, type='cosine')

    # store the data
    stccvelNZ = stccNZ.copy()
    stccvelNZ.remove_response(inventory=invstacha, pre_filt=pre_filt, output='VEL')
    return stccvelNZ

def WA_amplitudes(st):
    amp_dict = {}

    tr_n = st.select(component="N")[0]
    ampl_n_max = max(tr_n.data)
    ampl_n_min = min(tr_n.data)
    ampl_n_half_max_min = (abs(ampl_n_max) + abs(ampl_n_min))/2.
    amp_dict['N'] = ampl_n_half_max_min
    # print ("N comp -\t max %.4f\tmin %.4f\tmean of abs. values: %.4f" % (ampl_n_min, ampl_n_max, ampl_n_half_max_min))

    tr_e = st.select(component="E")[0]
    ampl_e_max = max(tr_e.data)
    ampl_e_min = min(tr_e.data)
    ampl_e_half_max_min = (abs(ampl_e_max) + abs(ampl_e_min))/2.
    amp_dict['E'] = ampl_e_half_max_min
    # print ("E comp -\t max %.4f\tmin %.4f\tmean of abs. values: %.4f" % (ampl_e_min, ampl_e_max, ampl_e_half_max_min))
    return amp_dict

def t_or_f(arg):
    ua = str(arg).upper()
    if 'TRUE'.startswith(ua):
       return True
    elif 'FALSE'.startswith(ua):
       return False
    else:
       pass  #error condition maybe?

if __name__ == "__main__":

    pre_filt = (0.01, 0.04, 25, 40)
    outdir = '.'

    parser = argparse.ArgumentParser()

    parser.add_argument("mseed_E", help="provide the name of the E-component input mseed file (e.g., 'IV.BRIS..HHE.mseed')")
    parser.add_argument("mseed_N", help="provide the name of the N-component input mseed file (e.g., 'IV.BRIS..HHN.mseed')")
    parser.add_argument("--outdir", help="provide the name of the output directory (default, '.')")
    parser.add_argument("--inxml", help="provide the name of the xml directory (default, '.')")
    parser.add_argument('--outwavals', dest='outwavals', action='store_true',
                        help="output half peak-2-peak  (default: False)")
    # parser.add_argument('--no-outwavals', dest='feature', action='store_false')
    #
    parser.set_defaults(outwavals=False)

    args = parser.parse_args()
    #
    # print (t_or_f(args.outwavals))
    out_flag = t_or_f(args.outwavals)
    #
    E_mseed = args.mseed_E
    N_mseed = args.mseed_N
    #
    if args.outdir is None:
        outdir = '.'
    else:
        outdir = args.outdir
        if not os.path.isdir(outdir):
            os.mkdir(outdir)

    ###### NEEDED ONLY WITH THE PROCEDURE THAT READS THE XML FILE ###########
    if args.inxml is None:
        # skip. The response will be obtained from the web webservices
        pass
        # STAXML_DIR = '.'
    else:
        STAXML_DIR = args.inxml
        # if not os.path.isdir(STAXML_DIR):
        #     os.mkdir(STAXML_DIR)
    ###### END ONLY WITH THE PROCEDURE THAT READS THE XML FILE ###########


    # Read the  2 input mseed files
    ST = Stream()
    try:
        ST = read(E_mseed)
        ST += read(N_mseed)
    except:
        print ("ERROR: wrong address or incorrect  mseed data\nEXIT")
        sys.exit(1)
    #
    # get the start and end times from the header of the stream
    starttime = ST[0].stats.starttime
    endtime = ST[0].stats.endtime
    #
    # get the informtion about station and network from the mseed
    net = ST[0].stats.network
    sta = ST[0].stats.station
    loc = ST[0].stats.location
    staname = "%s_%s.xml" % (net,sta)
    #
    # get the response function in xml format from the webservices
    if args.inxml is None:
        print ('obtain the station info from the webservices ')
        client = Client("INGV")
    # station_resp = client.get_stations(network=net, station=sta, channel="*", level="response")
        inv = client.get_stations(network=net, station=sta, starttime=starttime, endtime=endtime, level="response")
    #
    #### START aALTERNATIVE WAY TO GET THE STATION from  the downloaded 'response' directory containing the
    # stationxml files
    else:
    # check if the directory exists
        print ('obtain the station info from the stored stationxml file')
        if not os.path.isdir(STAXML_DIR):
            print ("ERROR: the directory with the stationxml files does not exist - exit(1)")
            exit(1)
        else:
            # compose the name of tha stationxml file
            # print (net, sta)
            station_xml = os.path.join(STAXML_DIR,staname)
            if os.path.isfile(station_xml):
                try:
                    inv = read_inventory(station_xml)
                except:
                    print ("ERROR: problems in reding the stationxml file - exit(1)")
                    exit(1)
            else:
                print ("ERROR: the stationxml files does not exist - exit(1)")
                exit(1)

    # ##################### OLD STUFF ALTERNATIVE WAY TO GET THE STATION ######
    # command = 'curl -X GET "http://webservices.ingv.it/fdsnws/station/1/query?network=%s&station=%s&channel=*&level=response&includerestricted=true&format=xml&formatted=false&nodata=204&visibility=only&authoritative=only" -H "accept: application/xml" > %s/%s_%s.xml ' % (net,sta,STAXML_DIR,net,sta)
    # # print (command)
    # os.system(command)
    # station_xml = os.path.join(STAXML_DIR,staname)
    # inv = read_inventory(station_xml)
    #
    # ################## END ALTERNATIVE WAY TO GET THE STATION ################
    #
    stccvelNZ = remove_response(ST, pre_filt, inv)
    #
    # apply Wood-Anderson
    stccvelNZ.simulate(paz_remove=None, paz_simulate=paz_wa, water_level=10)
    #
    # convert to mm
    for s in stccvelNZ:
        s.data = s.data * 1000
    # write out the WA records
    for s in stccvelNZ:
#     print (s.stats.network, s.stats.station, s.stats.location,  s.stats.channel)
        out_mseedfile = "%s.%s.%s.%s_WA.mseed" % (s.stats.network, s.stats.station, s.stats.location,  s.stats.channel)
        out_mseedfile = os.path.join(outdir,out_mseedfile)
    #     print (out_mseedfile)
        s.write(out_mseedfile, format="MSEED")
    #
    # write out the max half amplitudes for moth componenets
    if out_flag:
        wa_amps = WA_amplitudes(stccvelNZ)
        print ("E: %.4f N: %.4f" % (wa_amps['E'], wa_amps['N']))
