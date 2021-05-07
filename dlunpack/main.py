import os
import sys
import shutil
import pathlib
import datetime
import patoolib
import argparse

if sys.version_info < (3, 6):
	sys.exit('python version must be 3.6 or higher')

REQUIRED_AGE = datetime.timedelta(minutes=2)


def main():
	args = get_args()

	path_7z = shutil.which('7z')
	if path_7z is None:
		sys.exit('7z is not found')

	for root, _, filenames in os.walk(args.dir):
		for filename in filter(lambda x: os.path.splitext(x)[1] == '.rar', filenames):
			filepath = os.path.join(root, filename)
			flagpath = os.path.splitext(filepath)[0] + '.isunpacked'
			if os.path.exists(flagpath):
				continue
			fname = pathlib.Path(filepath)
			mtime = datetime.datetime.fromtimestamp(fname.stat().st_mtime)
			now = datetime.datetime.now()
			age = now - mtime
			if age < REQUIRED_AGE:
				continue
			with open(flagpath, 'w') as f:
				f.write('unpacking\n')
				patoolib.extract_archive(filepath, outdir=root, program=path_7z)
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

	if not os.path.exists(args.dir):
		argparser.error(f'Target directory does not exists : {args.dir}')

	if not os.path.isdir(args.dir):
		argparser.error(f'Target is not a directory : {args.dir}')

	return args


if __name__ == '__main__':
	main()