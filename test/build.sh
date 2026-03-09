#!/bin/bash

mock -r fedora-43-x86_64 --no-clean --buildsrpm --spec vicinae-test.spec --sources .
cp /var/lib/mock/fedora-43-x86_64/result/*.src.rpm .

mock -r fedora-43-x86_64 --no-clean *.src.rpm --addrepo=https://download.copr.fedorainfracloud.org/results/quadratech188/cmark-gfm/fedora-43-x86_64/ --enable-network
