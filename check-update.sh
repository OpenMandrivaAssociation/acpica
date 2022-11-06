#!/bin/sh
curl -s -L -A 'Mozilla/5.0 (X11; Linux x86_64)' https://acpica.org/downloads 2>/dev/null |grep -E "href=.*acpica-unix-" |sed -e "s,.*acpica-unix-,,;s,\.tar.*,,"
