make:
	nuitka brutus.py --lto 

clean:
	rm -r brutus.build
	rm brutus.exe
