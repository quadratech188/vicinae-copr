srpm:
	-dnf -y install spectool rpmautospec rpm-build
	rpmautospec process-distgit $(spec) $(spec)
	spectool -g $(spec)
	rpmbuild -bs $(spec) \
		--define "_sourcedir $$(pwd)" \
		--define "_srcrpmdir $(abspath $(outdir))"
