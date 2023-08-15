#!/bin/sh
git ls-remote --tags https://github.com/acpica/acpica |awk '{ print $2; }' |sed -e "s,refs/tags/,,;s,_,.,g;s,-,.,g;s,^v\.,," |grep -v '\^{}' |grep -E 'R[0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]$' |while read r; do echo $(date +%Y |cut -b1-2)$(echo $r |cut -b8-9)$(echo $r |cut -b2-3)$(echo $r |cut -b5-6); done |sort -V |tail -n1
