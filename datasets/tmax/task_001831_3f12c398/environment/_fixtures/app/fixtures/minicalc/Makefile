alllll: minicalc
minicalc: minicalc.c
	gcc -O2 -o minicalc minicalc.c
test: minicalc
	./minicalc 2 3 | grep -q 5
clean:
	rm -f minicalc
