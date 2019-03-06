import argparse
import re


def main():

    parser = argparse.ArgumentParser(
        description="Confirm valid port use\
        for COSC1179 Network Programming"
    )

    parser.add_argument('--snum', type=str, nargs=1, required=True)
    parser.add_argument('--ports', type=int, nargs=2, required=True)

    args = parser.parse_args()
    if not validate_args(args):
        exit()


def validate_args(args):
    if not (re.match(r"^s[0-9]{7}$", args.snum[0])):
        print("%s is not a valid student number" % args.snum[0])
        return False
    elif (args.ports[0] < 61000) or (args.ports[0] > 61999):
        print("Port argument 1 is out of the specified range. Please specify a port in the range 61000 - 61999")
        return False
    elif (args.ports[1] < 61000) or (args.ports[1] > 61999):
        print("Port argument 2 is out of the specified range. Please specify a port in the range 61000 - 61999")
        return False
    elif (args.ports[0] == args.ports[1]):
        print("Please specify two different ports.")
        return False

    return True


if __name__ == "__main__":
    main()
