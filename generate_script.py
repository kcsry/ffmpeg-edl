import argparse
import ast
import shlex
import sys
from typing import Optional


def read_tsv(infp, separator=None):
    headers = None
    for i, l in enumerate(infp):
        l = l.strip().split(separator)
        if l[0].startswith("#"):
            continue
        if i == 0:
            headers = l
            continue
        yield dict(zip(headers, l))


def ts_to_seconds(ts) -> float:
    seconds = 0
    for atom in str(ts).split(":"):
        atom = float(atom)
        seconds = seconds * 60 + atom
    return seconds


def read_cue(infp):
    tracks = []
    curr_track = None
    for line in infp:
        line = line.strip()
        word, _, rest = line.partition(" ")
        if word == "TRACK":
            curr_track = {}
            tracks.append(curr_track)
        elif word == "TITLE":
            curr_track["title"] = ast.literal_eval(rest)
        elif word == "INDEX":
            im, _, timestamp = rest.partition(" ")
            if im == "01":
                curr_track["start"] = ts_to_seconds(timestamp)
            else:
                print(f"Warning: ignoring index {im} in {line!r}", file=sys.stderr)
        else:
            print(f"Warning: ignoring CUE line {line!r}", file=sys.stderr)
    for i in range(1, len(tracks)):
        tracks[i - 1]["end"] = tracks[i]["start"]

    return tracks


def get_duration(datum, start: float) -> Optional[float]:
    if "end" in datum:
        end = ts_to_seconds(datum["end"])
        duration = end - start
    elif "duration" in datum:
        duration = int(datum["duration"])
    else:
        duration = None
    return duration


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("filename")
    ap.add_argument("-i", "--input", required=True)
    ap.add_argument("--tab-separated", default=False, action="store_true")
    ap.add_argument(
        "-c",
        "--conversion",
        default="-crf 23 -vf yadif -preset medium -tune film -ac 2 -ab 256k",
    )
    ap.add_argument("-x", "--extension", default="mp4")

    args = ap.parse_args()
    with open(args.filename) as infp:
        if args.filename.endswith(".cue"):
            data = list(read_cue(infp))
        else:
            separator = "\t" if args.tab_separated else None
            data = list(read_tsv(infp, separator=separator))

    conversion_args = shlex.split(args.conversion)
    input_name = args.input
    for datum in data:
        start = ts_to_seconds(datum["start"])
        duration = get_duration(datum, start)
        output_name = f'{datum["title"]}.{args.extension}'
        bits = [
            "ffmpeg",
            "-ss",
            str(start),
            "-i",
            input_name,
        ]
        if duration is not None:
            bits.extend(
                [
                    "-t",
                    str(duration),
                ]
            )
        bits.extend(conversion_args)
        bits.append(output_name)
        cmd = shlex.join(bits)
        print(cmd)


if __name__ == "__main__":
    main()
