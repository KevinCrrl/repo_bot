# KevinCrrl - 2026 - MIT License

import json
import os
import sys
import repo_bot as rb


def main():
    log = ""

    # Paths
    current = os.getcwd()
    try:
        repo = sys.argv[1]
    except IndexError:
        repo = input(">> Input the repo path: ")

    rb.init_nvc()
    if not os.path.exists(repo):
        print(">> ERROR: repo path not found!")
        sys.exit(1)

    with open(os.path.join(current, "new_version.json"), "r", encoding="utf-8") as file:
        content = json.load(file)

    for package, data in content["data"].items():
        if rb.update_pkgbuild(package, data, repo):
            log += f"{package}\n"

    try:
        log_dest = sys.argv[2]
    except IndexError:
        log_dest = "repo_bot_log.txt"

    with open(log_dest, "a", encoding="utf-8") as log_file:
        log_file.write(log)


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print()  # \n for shell
