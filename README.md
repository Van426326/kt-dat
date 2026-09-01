# kt-dat

Custom IP rule sets generated from `kt.txt` for V2Ray/daed and sing-box 1.14.

## Download

### V2Ray/daed

```text
https://github.com/Van426326/kt-dat/releases/latest/download/kt.dat
https://github.com/Van426326/kt-dat/releases/latest/download/kt.dat.sha256sum
```

### sing-box 1.14

Source rule-set:

```text
https://github.com/Van426326/kt-dat/releases/latest/download/kt.json
https://github.com/Van426326/kt-dat/releases/latest/download/kt.json.sha256sum
```

Binary rule-set:

```text
https://github.com/Van426326/kt-dat/releases/latest/download/kt.srs
https://github.com/Van426326/kt-dat/releases/latest/download/kt.srs.sha256sum
```

## Build Flow

This repository uses GitHub Actions to:

1. Validate the sing-box source generator with unit tests.
2. Generate `kt.dat` with the official `v2fly/geoip` generator.
3. Convert `kt.txt` to a sing-box version 5 source rule-set (`kt.json`).
4. Compile `kt.json` to `kt.srs` with the pinned sing-box 1.14.0 compiler.
5. Publish all rule sets and SHA256 checksum files to the `latest` GitHub Release.

The V2Ray DAT and sing-box SRS formats are not interchangeable. Use `kt.dat` with daed/V2Ray and `kt.srs` with sing-box.

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
