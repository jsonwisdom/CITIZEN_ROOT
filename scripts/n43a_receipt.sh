#!/usr/bin/env bash
set -euo pipefail
# N43a: local, unsigned replay; requires jq and sha256sum.
M="${1:?manifest path required}"
DOMAIN="${2:-jason.manifest.v0.hash}"
[ "$DOMAIN" = "jason.manifest.v0.hash" ] || { echo 'N43a requires manifest/0 .hash domain' >&2; exit 2; }
command -v jq >/dev/null && command -v sha256sum >/dev/null || { echo "jq and sha256sum required" >&2; exit 2; }
# Restricted fixture: ASCII-only UTF-8 plus duplicate-key and scalar validation elsewhere.
if LC_ALL=C grep -q '[^ -~[:space:]]' "$M"; then echo 'D004_CANONICALIZATION: non-ASCII unsupported' >&2; exit 3; fi
[ "$(jq -er '.jason' "$M")" = "manifest/0" ] || { echo 'E_SCHEMA' >&2; exit 4; }
BODY=$(jq -Sc 'del(.root)' "$M")
DIGEST=$( { printf '%s' "$DOMAIN"; printf '\\0'; printf '%s' "$BODY"; } | sha256sum | cut -d' ' -f1 )
CLAIMED=$(jq -r '.root // ""' "$M")
jq -n --arg root "sha256:$DIGEST" --arg claimed "$CLAIMED" --arg domain "$DOMAIN" --arg src "$M" '{
  jason:"receipt/0", kind:"manifest_root_receipt", root:$root,
  claimed_root:(if $claimed=="" then null else $claimed end),
  comparison:(if $claimed=="" then "NO_CLAIM" elif $claimed==$root then "MATCH" else "MISMATCH" end),
  domain:$domain, source_path:$src, observed_at_utc:null,
  time_provenance:"UNKNOWN(NEG-SUB-003)", observed_by:"LOCAL_RUNNER",
  signed:false, independent_witness:false, authority_created:false
}'
