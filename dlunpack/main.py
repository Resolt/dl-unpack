import sys
import shutil
import patoolib
import argparse
import datetime as dt
from pathlib import Path


REQUIRED_AGE = dt.timedelta(minutes=2)


def main():
	args = get_args()

	path_7z = shutil.which('7z')
	if path_7z is None:
		sys.exit('7z is not found')

	for x in args.dir.glob('**/*.rar'):
		flag = x.parent.joinpath(f'{x.stem}.isunpacked')
		couch = x.parent.joinpath(f'{x.stem}.extracted.ignore')
		if flag.exists() or couch.exists():
			continue
		age = dt.datetime.now() - dt.datetime.fromtimestamp(x.stat().st_mtime)
		if age < REQUIRED_AGE:
			continue
		with flag.open('w') as f:
			f.write('unpacking\n')
			patoolib.extract_archive(str(x), outdir=x.parent, program=path_7z, interactive=False)
			f.write('unpacked\n')


def get_args():
	argparser = argparse.ArgumentParser(
		prog='dl-unpack',
		description='Script for unrar recursively'
	)

	argparser.add_argument('--dir', type=str, help='Target directory')

	args = argparser.parse_args()

	if args.dir is None:
		argparser.error('--dir must be provided')

	args.dir = Path(args.dir)

	if not args.dir.exists():
		argparser.error(f'Target directory does not exists : {args.dir}')

	if not args.dir.is_dir():
		argparser.error(f'Target is not a directory : {args.dir}')

	return args


if __name__ == '__main__':
	if sys.version_info < (3, 6):
		sys.exit('python version must be 3.6 or higher')
	main()
