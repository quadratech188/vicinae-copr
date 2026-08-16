srpm:
	-dnf -y install spectool rpmautospec rpkg
	spectool -g $(spec) --directory $(outdir)
	rpmautospec process-distgit $(spec) $(outdir)/$(notdir $(spec))
	rpkg srpm --spec $(outdir)/$(notdir $(spec)) --outdir $(outdir)
