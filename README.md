# mseed2wa
Miniseed to WoodAnderson

## Clone
```
$ git clone git@github.com:INGV/mseed2wa.git
```

## Build
```
$ cd mseed2wa
$ docker build --tag mseed2wa .
```

## Run
```
$ cd mseed2wa
$ docker run -it --rm -v $(pwd)/input:/tmp/input -v $(pwd)/output:/tmp/output mseed2wa bash
```

## Example
```
$ cd mseed2wa
$ docker run -it --rm -v $(pwd)/input:/tmp/input -v $(pwd)/output:/tmp/output mseed2wa bash
(base) root@a4c8d6de4cbc:/#
(base) root@a4c8d6de4cbc:/#
(base) root@a4c8d6de4cbc:/# /opt/mseed2wa.py /tmp/input/IV.BRIS..HHN.mseed /tmp/input/IV.BRIS..HHE.mseed --outdir /tmp/output/ --inxml /tmp/input/ --outwavalsobtain the station info from the stored stationxml file
/opt/conda/lib/python3.8/site-packages/obspy/io/mseed/core.py:790: UserWarning: The encoding specified in trace.stats.mseed.encoding does not match the dtype of the data.
A suitable encoding will be chosen.
  warnings.warn(msg, UserWarning)
E: 22.7927 N: 21.6225
(base) root@a4c8d6de4cbc:/#
```
