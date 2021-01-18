# mseed2wa
Miniseed to WoodAnderson

## Build
```
docker build --tag mseed2wa .
```

## Run
```
docker run -it --rm -v $(pwd)/input:/tmp/input -v $(pwd)/output:/tmp/output mseed2wa bash
```
