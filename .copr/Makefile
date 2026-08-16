srpm:
	-dnf -y install spectool rpmautospec rpkg
	spectool -g $(spec)
	rpmautospec process-distgit $(spec) $(spec)
	rpkg srpm  --outdir $(outdir)
	# The build system sees a symlink to the tar archive in the outdir and freaks out
	find $(outdir) -type l -delete
