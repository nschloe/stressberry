default:
	@echo "make rpi4?"

rpi4:
	stressberry-plot rpi4b-argon-one.dat rpi4b-armor.dat rpi4b-coolipi-fan-off.dat rpi4b-flirc.dat rpi4b-flyingferret-fans-off.dat rpi4b-icetower-fan-off.dat rpi4b-JohBod-kksb.dat rpi4b-stock.dat -o 4b-passive.svg
	stressberry-plot rpi4b-coolipi-fan-on.dat rpi4b-flyingferret-fans-on.dat rpi4b-hex-wrench.dat rpi4b-icetower-fan-on.dat -o 4b-active.svg
	svgo 4b-passive.svg 4b-active.svg
