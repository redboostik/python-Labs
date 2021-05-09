#!usr/bin/python3
import argparse
from dump_library import dump_service
parser_args = argparse.ArgumentParser(description='Redboostik\'s serializer')
parser_args.add_argument('file_path', type=str, help='Enter path to file')
parser_args.add_argument('format', type=str, help='Enter format')
parser_args.add_argument('-o', '--old_format', type=str, help='old file format', default=None)
parser_args.add_argument('-t', '--to_file', type=str, help='path to file write', default=None)

args = parser_args.parse_args()

if args.old_format is None:
    point = args.file_path.rfind('.')
    if point == -1:
        raise ValueError('Unknown format file')
    else:
        args.old_format = args.file_path[point + 1:]

if args.to_file is None:
    args.to_file = args.file_path

obj = dump_service.load(args.file_path, args.old_format)
dump_service.dump(obj, args.format, args.file_path)
