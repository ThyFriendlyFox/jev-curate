#!/usr/bin/env bash
# Gate: the example rubric parses and lists its gates (README "Development").
set -euo pipefail
cd "$(dirname "$0")/../.."
jev-curate validate-rubric --rubric examples/rubric.yaml
