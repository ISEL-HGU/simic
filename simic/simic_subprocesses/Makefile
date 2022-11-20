DIR := ${CURDIR}

build:
	cd editscript;gradle build
	unzip $(CURDIR)/editscript/app/build/distributions/app.zip -d ES
	cd poolprocess;gradle build
	unzip $(CURDIR)/poolprocess/app/build/distributions/app.zip -d PP


unzip:
	rm -rf runs
	unzip $(CURDIR)/app/build/distributions/app.zip

es_run:
	./ES/app/bin/app -src $(src) -dst $(dst)

pp_run:
	./PP/app/bin/app -proj $(proj) -pc $(pc) -file $(file) -line $(line)

clean:
	rm -rf ES
	rm -rf PP
