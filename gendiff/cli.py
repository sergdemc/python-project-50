import argparse


def parse_cli():
    parser = argparse.ArgumentParser(description='Compares two configuration\
     files and shows a difference.')
    parser.add_argument('first_file', type=str)
    parser.add_argument('second_file', type=str)
    parser.add_argument('-f', '--format',
                        help='set format of output stylish, plane, JSON',
                        default='stylish', type=str)
    args = parser.parse_args()
    return args.first_file, args.second_file


path1, path2 = parse_cli()
