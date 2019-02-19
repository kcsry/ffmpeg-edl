import argparse
import shlex


def read_tsv(infp):
    headers = None
    for i, l in enumerate(infp):
        l = l.strip().split()
        if i == 0:
            headers = l
            continue
        yield dict(zip(headers, l))


def ts_to_seconds(ts):
    seconds = 0
    for atom in ts.split(':'):
        atom = float(atom)
        seconds = seconds * 60 + atom
    return seconds


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('filename')
    ap.add_argument('-i', '--input', required=True)
    ap.add_argument(
        '-c',
        '--conversion',
        default='-crf 23 -vf yadif -preset medium -tune film -ac 2',
    )
    ap.add_argument('-x', '--extension', default='mp4')

    args = ap.parse_args()
    with open(args.filename) as infp:
        data = list(read_tsv(infp))
    for datum in data:
        start = ts_to_seconds(datum['start'])
        end = ts_to_seconds(datum['end'])
        cmd = 'ffmpeg -ss {start} -i {input} -t {duration} {conversion} {output}'.format(
            input=shlex.quote(args.input),
            start=start,
            duration=duration,
            conversion=args.conversion,
            output=shlex.quote('%s.%s' % (datum['title'], args.extension)),
        )
        print(cmd)


if __name__ == '__main__':
    main()
