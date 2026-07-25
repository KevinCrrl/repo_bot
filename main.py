"""
Copyright 2026 KevinCrrl

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import argparse
import json
import os
import sys
import repo_bot as rb


def main():
    parser = argparse.ArgumentParser(
        prog="RepoBot",
        description="Update PKGBUILDs automatically",
        epilog="RepoBot - Copyright (C) 2026 KevinCrrl; Apache 2.0 License")

    parser.add_argument("repopath", help="Path to the repository containing the PKGBUILDs")
    parser.add_argument("logdest", help="Path to save the log")
    parser.add_argument("-o", "--nobuild", action="store_true",
                        help="Skip the build test")

    args = parser.parse_args()
    log = ""

    # Paths
    current = os.getcwd()
    try:
        repo = args.repopath
    except IndexError:
        repo = input(">> Input the repo path: ")

    rb.init_nvc()
    if not os.path.exists(repo):
        print(">> ERROR: repo path not found!")
        sys.exit(1)

    with open(os.path.join(current, "new_version.json"), "r", encoding="utf-8") as file:
        content = json.load(file)

    for package, data in content["data"].items():
        if rb.update_pkgbuild(package, data, repo, args.nobuild):
            log += f"{package}\n"

    try:
        log_dest = args.logdest
    except IndexError:
        log_dest = "repo_bot_log.txt"

    with open(log_dest, "a", encoding="utf-8") as log_file:
        log_file.write(log)


try:
    if __name__ == "__main__":
        main()
except KeyboardInterrupt:
    print()  # \n for shell
