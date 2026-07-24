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

import subprocess as sb
import os
import pkgbuild_parser as pp


def init_nvc():
    if not os.path.exists("software.toml"):
        print(">> ERROR: software.toml not found!")
    else:
        try:
            sb.run(["nvchecker", "-c", "software.toml"], check=True)
            sb.run(["nvtake", "-c", "software.toml", "--all"], check=True)
        except sb.CalledProcessError as e:
            print(f">> ERROR: {e}")


def update_pkgbuild(package: str, pdata: dict, repo: str) -> bool:
    os.chdir(os.path.join(repo, package))
    pkg = pp.Parser()
    # Get PKGBUILD version
    old_version = pkg.get_pkgver()
    new_version = pdata["version"]
    if old_version != new_version:
        print(f">> New version found for: {package}")
        print(f"> Old version: {old_version}, new version: {new_version}")
        with open("PKGBUILD", "r+", encoding="utf-8") as pkg_content:
            pkgbuild = pkg_content.read()
            original = pkgbuild  # backup
            pkgbuild = pkgbuild.replace(f"pkgver={old_version}", f"pkgver={new_version}")
            if int(pkg.get_pkgrel()) > 1:
                # Reset pkgrel
                pkgbuild = pkgbuild.replace(f"pkgrel={pkg.get_pkgrel()}", "pkgrel=1")
            print("PKGBUILD updated, writing...")
            pkg_content.seek(0)
            pkg_content.write(pkgbuild)
            pkg_content.truncate()
            try:
                sb.run(["updpkgsums"], shell=False, check=True)
                sb.run(["makepkg", "-s"], shell=False, check=True)
            except sb.CalledProcessError as e:
                print(f"ERROR: {e}\nAborting!")
                pkg_content.seek(0)
                pkg_content.write(original)
                pkg_content.truncate()
            else:
                return True
    else:
        print(f">> {package} is up-to-date!")
    return False
