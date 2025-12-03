#!/bin/bash

mock --no-clean --buildsrpm --spec vicinae.spec --sources .
cp /var/lib/mock/fedora-43-x86_64/result/*.src.rpm .

mock --no-clean *.src.rpm --addrepo=https://download.copr.fedorainfracloud.org/results/quadratech188/cmark-gfm/fedora-43-x86_64/ --enable-network
