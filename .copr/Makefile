srpm:
	spectool -g $(spec)
	rpmautospec process-distgit $(spec) $(spec)
	rpkg srpm  --outdir $(outdir)
