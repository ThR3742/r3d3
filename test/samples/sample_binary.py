import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--do_fail', type=int, default=0)
args, _ = parser.parse_known_args()

print("Hello world")

if args.do_fail > 0:
    raise RuntimeError("Failing")
