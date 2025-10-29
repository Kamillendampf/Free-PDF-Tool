import argparse
import sys
import core


def ready(argv = sys.argv) -> None:
    argv = argv if len(argv) < 1 else argv[1:]
    args_parser = build_args_parser()
    args = args_parser.parse_args(argv)

    print(args)
    return args.func(args)

def build_args_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog = 'PDF_reader',
        description = 'A CLI PDF handler',)

    sub_parser = ap.add_subparsers(dest="cmd", required =False,)

    sp_m = sub_parser.add_parser('merge', help = 'Start PDF merge')
    sp_m.add_argument("-m", "--merge",
                      dest = 'merge_pdf',
                      action='store_true',
                      help = 'Merge PDF Files in given order.')
    sp_m.add_argument("-o", "--output", nargs = '?', help = 'Specify output file.')
    sp_m.add_argument("-i", "--input", nargs = '*', help = 'Specify input files (defines the order in which the files are merged)')
    sp_m.set_defaults(func=handle_merge)

    return ap

def handle_merge(args: argparse.Namespace) -> int:
    try:
        core.merge_pdf(args.output, args.input)
        print(f"OK: {len(args.input)} files are merged in to {args.output}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file = sys.stderr)
        return 1


if __name__ == '__main__':
    ready()
