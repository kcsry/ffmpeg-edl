import argparse

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
		atom = int(atom)
		seconds = seconds * 60 + atom
	return seconds

def main():
	ap = argparse.ArgumentParser()
	ap.add_argument('filename')
	ap.add_argument('-v', '--video', required=True)
	args = ap.parse_args()
	with open(args.filename) as infp:
		data = list(read_tsv(infp))
	for datum in data:
		start = ts_to_seconds(datum['start'])
		end = ts_to_seconds(datum['end'])
		duration = end - start
		cmd = 'ffmpeg -ss {start} -i {video} -t {duration} -crf 23 -vf yadif -preset medium -tune film -ac 2 {output}'.format(
			video=args.video,
			start=start,
			duration=duration,
			output=('%s.mp4' % datum['title']),
		)
		print(cmd)


if __name__ == '__main__':
	main()