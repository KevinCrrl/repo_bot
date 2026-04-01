# Repo Bot by KevinCrrl

Bot for update PKGBUILDs using `nvchecker` and `pkgbuild-parser`.

## Usage

```
$ python main.py <repo_path> <log_dest>
```

repo_path: folder with the PKGBUILD following this structure:

```
repo_path
    - package_1
        - PKGBUILD
    - package_2
        - PKGBUILD
    - package_3
        - PKGBUILD
```

log_dest: path for write a log file, default: ./repo_bot_log.txt

## Configuration

Create a software.toml for nvchecker:

```toml
[__config__]
oldver = "old_version.json"
newver = "new_version.json"

# Your software list here
```

## License

MIT License
