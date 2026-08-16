srpm:
	dnf -y install spectool rpmautospec rpkg
	spectool -g $(spec)
	rpmautospec process-distgit $(spec) $(spec)
	rpkg srpm  --outdir $(outdir)
