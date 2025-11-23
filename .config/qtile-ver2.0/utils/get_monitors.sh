#!/usr/bin/env bash
set -euo pipefail

# Get xrandr --listmonitors output
out=$(xrandr --listmonitors 2>/dev/null) || { echo "error: xrandr failed" >&2; exit 1; }

# Print each monitor as CSV: <id>,<width>,<height>
# id is 1-based (first monitor = 1)
awk '
/^[[:space:]]*[0-9]+:/ {
  # Try to match formats like: 1920/309x1080/174+0+0 (captures 1920 and 1080)
  if (match($0, /([0-9]+)\/[0-9]+x([0-9]+)\/[0-9]+/, m)) {
    w = m[1]; h = m[2];
  }
  # Fallback to simple WxH if present: 1920x1080
  else if (match($0, /([0-9]+)x([0-9]+)/, m)) {
    w = m[1]; h = m[2];
  } else {
    next
  }
  printf("%d,%s,%s\n", ++c, w, h)
}
' <<<"$out"

