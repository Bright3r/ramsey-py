from subprocess import call

tests = ["20 4 6", "25 4 6", "30 4 6", "20 3 3 4", "28 3 3 4", "16 3 3 3"]
location = "./tassat/tests2"

def main():
    for test in tests:
        # Get filename for test case
        filename = "my2-R-"
        for word in test.split(' '):
            filename += word + '-'
        filename += ".cnf"

        # Create commandline args to run test case
        args = ["python3", "ramsey.py", filename]
        for word in test.split(' '):
            args.append(word)

        # Create test case cnf and move to test folder
        call(args)
        call(["mv", filename, location])


if __name__ == "__main__":
    main()
