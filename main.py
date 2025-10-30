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

    sp_m = sub_parser.add_parser('merge', help = 'Merges two or more PDF files in to one PDF')
    sp_m.add_argument("-o", "--output", nargs = '?', help = 'Specify output file.')
    sp_m.add_argument("-i", "--input", nargs = '*', help = 'Specify input files (defines the order in which the files are merged)')
    sp_m.set_defaults(func=handle_merge)

    sp_r = sub_parser.add_parser('read', help = 'Reads a PDF File \n -f --file spezifies the input file \n -p --page Specify sides that should be read \n -pass --password For decryption of PDF file if it`s secured')
    sp_r.add_argument("-f", "--file", nargs = '?', help = 'Specify file to read')
    sp_r.add_argument("-p", "--pages", help = 'Specify sides that should be read')
    sp_r.add_argument("-pass", "--password", help = 'For decryption of PDF file if it`s secured')
    sp_r.set_defaults(func=handle_reader)

    return ap

def handle_merge(args: argparse.Namespace) -> int:
    try:
        core.merge_pdf(args.output, args.input)
        print(f"OK: {len(args.input)} files are merged in to {args.output}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file = sys.stderr)
        return 1

def handle_reader(args: argparse.Namespace) -> int:
    read_file= core.read_pdf(args.file, args.pages, args.password)
    print(read_file)
    return 0


if __name__ == '__main__':
    ready()
