#!/usr/bin/env bash
set -euo pipefail

REPO_OWNER="${REPO_OWNER:-Van426326}"
REPO_NAME="${REPO_NAME:-kt-dat}"
BASE_URL="${BASE_URL:-https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/latest/download}"
TARGET="${TARGET:-/usr/local/share/daed/kt.dat}"
CHECK_INTERVAL="${CHECK_INTERVAL:-10min}"
UPDATER_PATH="${UPDATER_PATH:-/usr/local/sbin/update-daed-kt-dat.sh}"
SERVICE_PATH="${SERVICE_PATH:-/etc/systemd/system/update-daed-kt-dat.service}"
TIMER_PATH="${TIMER_PATH:-/etc/systemd/system/update-daed-kt-dat.timer}"

if [ "$(id -u)" -ne 0 ]; then
  echo "Please run as root, for example: curl -fsSL ... | sudo bash" >&2
  exit 1
fi

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Required command not found: $1" >&2
    exit 1
  fi
}

require_command curl
require_command sha256sum
require_command cmp
require_command install
require_command systemctl
require_command flock

install -d -m 0755 "$(dirname "$TARGET")"
install -d -m 0755 "$(dirname "$UPDATER_PATH")"

cat > "$UPDATER_PATH" <<UPDATER
#!/usr/bin/env bash
set -euo pipefail

BASE_URL="\${BASE_URL:-${BASE_URL}}"
TARGET="\${TARGET:-${TARGET}}"
TMP_DIR="\$(mktemp -d)"
LOCK_FILE="/tmp/update-daed-kt-dat.lock"

exec 9>"\$LOCK_FILE"
flock -n 9 || exit 0

cleanup() {
  rm -rf "\$TMP_DIR"
}
trap cleanup EXIT

curl -fsSL "\$BASE_URL/kt.dat" -o "\$TMP_DIR/kt.dat"
curl -fsSL "\$BASE_URL/kt.dat.sha256sum" -o "\$TMP_DIR/kt.dat.sha256sum"

cd "\$TMP_DIR"
sha256sum -c kt.dat.sha256sum

if [ -f "\$TARGET" ] && cmp -s "\$TMP_DIR/kt.dat" "\$TARGET"; then
  echo "kt.dat unchanged, skip restart"
  exit 0
fi

install -m 0644 "\$TMP_DIR/kt.dat" "\$TARGET"

systemctl restart daed
echo "kt.dat updated and daed restarted"
UPDATER

chmod 0755 "$UPDATER_PATH"

cat > "$SERVICE_PATH" <<SERVICE
[Unit]
Description=Update daed kt.dat from GitHub Release
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
Environment=BASE_URL=${BASE_URL}
Environment=TARGET=${TARGET}
ExecStart=${UPDATER_PATH}
SERVICE

cat > "$TIMER_PATH" <<TIMER
[Unit]
Description=Check kt.dat updates for daed

[Timer]
OnBootSec=1min
OnUnitActiveSec=${CHECK_INTERVAL}
Persistent=true

[Install]
WantedBy=timers.target
TIMER

systemctl daemon-reload
systemctl enable --now update-daed-kt-dat.timer
systemctl start update-daed-kt-dat.service

cat <<EOF
daed kt.dat updater installed.

Updater: ${UPDATER_PATH}
Service: ${SERVICE_PATH}
Timer:   ${TIMER_PATH}
Target:  ${TARGET}
Source:  ${BASE_URL}/kt.dat

Useful commands:
  systemctl list-timers update-daed-kt-dat.timer
  systemctl status update-daed-kt-dat.service --no-pager
  journalctl -u update-daed-kt-dat.service -n 50 --no-pager
EOF
