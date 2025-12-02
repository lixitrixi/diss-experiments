
.PHONY: run
run: tests.txt
	./runtests.sh

tests.txt: mktests.sh
	./mktests.sh

.PHONY: all
all: tests.txt run
