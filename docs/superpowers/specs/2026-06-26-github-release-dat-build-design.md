# GitHub Release DAT Build Design

## Goal

Generate `kt.dat` from the repository's `kt.txt` and `config.json` using the official open-source `v2fly/geoip` generator whenever repository code changes, then publish the generated file to a stable GitHub Release download URL.

## Inputs

- `kt.txt`: plaintext IP and CIDR source list.
- `config.json`: `v2fly/geoip` configuration. It reads `kt.txt` as a `text` input named `kt` and writes `kt.dat` as a `v2rayGeoIPDat` output.

## Build Flow

1. GitHub Actions runs on pushes to `main` and on manual `workflow_dispatch`.
2. The workflow checks out this repository.
3. The workflow installs Go and the official generator with `go install github.com/v2fly/geoip@latest`.
4. The workflow runs `geoip -c config.json`.
5. The workflow verifies `output/dat/kt.dat` exists.
6. The workflow creates `kt.dat.sha256sum`.
7. The workflow uploads both files to a GitHub Release attached to tag `latest`.

## Published Artifact

The stable artifact URL is:

`https://github.com/Van426326/kt-dat/releases/latest/download/kt.dat`

The checksum URL is:

`https://github.com/Van426326/kt-dat/releases/latest/download/kt.dat.sha256sum`

## Repository Setup

The local folder should be initialized as a git repository and associated with:

`git@github.com:Van426326/kt-dat.git`

## Notes

- The workflow uses GitHub's built-in `GITHUB_TOKEN` with `contents: write` permission to create or update the release.
- The release tag is intentionally named `latest`, so the GitHub `/releases/latest/download/...` URL remains stable.
- Generated `output/` files are build artifacts and should not be committed.
