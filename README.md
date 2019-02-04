The purpose of this python program is to demonstrate how a very simple cache coherency protocol (MSI) works.

You can just clone this repo and do the following:

$ python test_msi.py | less

You may want to pipe it to a file (e.g. logfile.txt) and view it.

What happens in the test_msi.py file is 3 processors each with its own cache are generated, as well as the bus that connects these processors and helps each processor maintain coherency by sending global events like BusRd and BusRdX. 

The log file should be fairly self-explanatory and after each randomized comment I dump out the contents of the processors and bus. 

Enjoy and let me know if you have any comments or issues!

This was mainly inspired by the nice lecture by David Henty located here: https://www.youtube.com/watch?v=S3kg_zCz_PA&t=1356s