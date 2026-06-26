# kt-dat

Custom `kt.dat` GeoIP rule set generated from `kt.txt` with the official `v2fly/geoip` generator.

## Download

Latest `kt.dat`:

```text
https://github.com/Van426326/kt-dat/releases/latest/download/kt.dat
```

SHA256 checksum:

```text
https://github.com/Van426326/kt-dat/releases/latest/download/kt.dat.sha256sum
```

## Build Flow

This repository uses GitHub Actions to:

1. Install `github.com/v2fly/geoip@latest`.
2. Generate `kt.dat` from `config.json` and `kt.txt`.
3. Publish `kt.dat` and `kt.dat.sha256sum` to the `latest` GitHub Release.

## Install daed Auto Updater

Run this on the daed server:

```bash
curl -fsSL https://raw.githubusercontent.com/Van426326/kt-dat/main/scripts/install-daed-updater.sh | sudo bash
```

The installer creates:

- `/usr/local/sbin/update-daed-kt-dat.sh`
- `/etc/systemd/system/update-daed-kt-dat.service`
- `/etc/systemd/system/update-daed-kt-dat.timer`

By default it downloads `kt.dat` to:

```text
/usr/local/share/daed/kt.dat
```

The timer checks every 10 minutes. It verifies the SHA256 checksum, replaces `kt.dat` only when the file changes, and then runs:

```bash
systemctl restart daed
```

## Installer Options

You can override defaults with environment variables:

```bash
curl -fsSL https://raw.githubusercontent.com/Van426326/kt-dat/main/scripts/install-daed-updater.sh | sudo env CHECK_INTERVAL=5min bash
```

Available variables:

- `BASE_URL`: release asset base URL
- `TARGET`: local dat file path
- `CHECK_INTERVAL`: systemd timer interval, default `10min`
- `UPDATER_PATH`: updater script path

Example:

```bash
curl -fsSL https://raw.githubusercontent.com/Van426326/kt-dat/main/scripts/install-daed-updater.sh | sudo env TARGET=/usr/local/share/daed/kt.dat CHECK_INTERVAL=5min bash
```

## Operations

Check timer:

```bash
systemctl list-timers update-daed-kt-dat.timer
```

Run update immediately:

```bash
sudo systemctl start update-daed-kt-dat.service
```

View logs:

```bash
journalctl -u update-daed-kt-dat.service -n 50 --no-pager
```

Disable auto update:

```bash
sudo systemctl disable --now update-daed-kt-dat.timer
```

Remove installed unit files:

```bash
sudo systemctl disable --now update-daed-kt-dat.timer
sudo rm -f /etc/systemd/system/update-daed-kt-dat.service /etc/systemd/system/update-daed-kt-dat.timer
sudo rm -f /usr/local/sbin/update-daed-kt-dat.sh
sudo systemctl daemon-reload
```
