import argparse
import sys
import time

from dft import dft


def parse_args():
    parser = argparse.ArgumentParser(description='preforms image compression '
                                     'using DFT reduction on a given image')
    parser.add_argument('path', help='path to the target image')
    parser.add_argument('--epsilon', type=float, default=None,
                        help='truncate all values in specter that are '
                        'less than epsilon')
    parser.add_argument('--bw', action='store_true',
                        help='convert image to grayscale before '
                        'reduction')
    parser.add_argument('--conv', action='store_true',
                        help='convert image to jpg')

    args = parser.parse_args()

    if not args.epsilon and not args.conv:
        print('Specify one of the --epsion or --conv', file=sys.stderr)
        sys.exit(1)

    return args


def main():
    args = parse_args()

    if args.conv:
        dft.to_image(args.path, args.path[:args.path.rfind('.')] + '.jpg')
        return

    start = time.time()
    print('Opening image...', end=' ')

    if args.bw:
        image = dft.rgb_to_grayscale(dft.open_image(args.path))
        convert_fn = dft.convert
    else:
        image = dft.open_image(args.path)
        convert_fn = dft.convert_rgb

    print('Done, took: {:0.02f} s'.format(time.time() - start))

    start = time.time()
    print('Calculating DFT...', end=' ')

    convert_fn(image, args.epsilon, args.path[:args.path.rfind('.')] + '.aaa')

    print('Done, took: {:0.02f} s'.format(time.time() - start))


if __name__ == "__main__":
    main()
