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
