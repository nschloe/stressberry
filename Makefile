default:
	@echo "make rpi4?"

rpi4:
	stressberry-plot rpi4b-* -o all.svg
	svgo all.svg
	stressberry-plot rpi4b-* -o all.png
	optipng all.png
