default:
	@echo "make rpi4?"

rpi4:
	stressberry-plot rpi4b-* -o 4b.svg
	svgo 4b.svg
