
.PHONY: tests
tests: tests.txt

tests.txt:
	./mktests.sh

.PHONY: run
run: tests
	./runtests.sh

.PHONY: all
all: tests run
