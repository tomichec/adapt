# ADAPT

## Description

This is a git repository of my notes for the ADAPT project.

## Dependencies

* autotools (make)
* gnuplot
* texlive (latex, pdflatex)
* python3 (+ numpy, scipy and matplotlib libraries -- to install it run `pip3 install --user numpy scipy matplotlib`)
* wget (to download results)

## Compilation

1. To generate all from scratch run:

	```
	make
	```

	This will take a considerable amount of time (hours), as it will
	do expensive simulations. This can be paralelised up by `make -j
	N` option (where N is a number of processors to be used by 'make'.

2. Alternatively, the expensive simulation results can be downloaded from
   online repository by a

	```
	make download
	```

	followed by a step 1. (`make`).

## License

Free software under [GNU GPLv3](http://www.gnu.org/licenses/gpl.txt).

## Contact

Any comments will be greatly appreciated.  Please feel free to get in
touch with me via [email](mailto:T.Stary@exeter.ac.uk).

