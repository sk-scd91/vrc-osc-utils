from argparse import ArgumentParser
from sys import argv

from pythonosc.udp_client import SimpleUDPClient

from vrc_osc_utils.tools import watch

def parse_args(tool, argv):
    args = ArgumentParser()
    args.add_argument("--port", "-p", type=int, default=9000, help="The UDP port to send OSC messages to.")
    args.add_argument("--host", "-a", type=str, default="127.0.0.1", help="The IP address to send OSC Messages to.")
    if tool == "watch":
        args.add_argument("--delay", "-d", type=float, default=60.0, help="The interval delay to send the watch time.")
    elif tool == "sign":
        pass
    else:
        args.print_help()
        exit(1)
    return args.parse_args(argv)

def main_watch(args):
    client = SimpleUDPClient(args.host, args.port)
    watch.run_sync(client, args.delay)

def main(argv):
    if len(argv) == 0:
        print("Missing sub command: [watch]")
        parse_args("", argv) # TODO Use subparsers to make more elegant.
    tool = argv[0]
    args = parse_args(tool, argv[1:])
    if tool == "watch":
        main_watch(args)

if __name__ == "__main__":
    main(argv[1:])