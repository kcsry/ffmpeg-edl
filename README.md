# ffmpeg-edl

Split (and optionally transcode) video using ffmpeg with

* a TSV EDL (Edit Decision List)
* a CUE file

## Example usage

For instance, given the recording of a cosplay show from an entirely fictitious convention,
stored in `2024-06-15_17-26-44.mp4`, and a TSV file `cosplay-edl.txt` (see the example in this repo),
the following command will generate a script `d24.sh` that will split the video into clips in the `d24`
folder, using the given ffmpeg conversion arguments. The script can be inspected, and then executed
to have ffmpeg do its thing.

```
python3 generate_script.py -c="-c copy -movflags +faststart" --tab-separated -i 2024-06-15_17-26-44.mp4 cosplay-edl.txt -o d24 > ./d24.sh
bash -x ./d24.sh
```

## Additional tools

### save-current-time.lua

The enclosed `save-current-time.lua` script can be used with the [mpv](https://mpv.io/)
video player to save time-in/time-out pairs to a file (`time.txt`).

This can be then refined to a TSV-based EDL by hand.
