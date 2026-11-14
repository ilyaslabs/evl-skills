#!/usr/bin/env sh
# Makes the EVL CLI available. Prints the command to run it.
# Usage: ensure-evl.sh [version]   (default: the version in EVL_VERSION or 2.0.0)
set -eu
VERSION="${1:-${EVL_VERSION:-2.0.0}}"
if command -v evl >/dev/null 2>&1; then
  echo "evl"
  exit 0
fi
command -v java >/dev/null 2>&1 || { echo "Java 17+ is required to run the EVL CLI." >&2; exit 2; }
DIR="${HOME}/.evl"
JAR="${DIR}/evl-cli-${VERSION}-all.jar"
if [ ! -f "$JAR" ]; then
  URL="https://github.com/ilyaslabs/evl-lib/releases/download/v${VERSION}/evl-cli-${VERSION}-all.jar"
  echo "Downloading the EVL CLI ${VERSION} from ${URL} to ${JAR}" >&2
  mkdir -p "$DIR"
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL -o "${JAR}.part" "$URL"
  else
    wget -q -O "${JAR}.part" "$URL"
  fi
  mv "${JAR}.part" "$JAR"
fi
echo "java -jar ${JAR}"
