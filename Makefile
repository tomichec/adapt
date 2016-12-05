# modified implicit rule for the .tex files
TEX=latex

PYTHON=python3

# figures used in the process
FIGURES = consolidation.pdf heat.pdf permeab.pdf viscosity.pdf dcure.pdf cure.pdf fibre_bed.pdf error.pdf

# as pdf generation uses latex, the target are logfiles -- the pdf is side product
LOG = report.log slides.log

.PHONY: all aux

all: aux $(LOG)

aux: $(FIGURES) element.out galerkin.out 

# output from python scripts
%.out: %.py
	$(PYTHON) $< > $@

# datafiles from python scripts
%.dat: %.py
	$(PYTHON) $< > $@

# findiff file, which requires command line arguments -- DOES IT WORK?
findiff%.dat: findiff.py
	$(PYTHON) $< $(subst _, ,$*) > $@

# transpose of the datafile
trans_%.awk.dat: trans.awk %.dat
	awk -f $+ > $@

# datafile for the convergence study
.PRECIOUS: $(DATDT) $(DATN)
# findiff-t_1e-6_-n_100.dat -- takes real time 1m1.576s
DATDT = $(foreach t, 1e-7 1e-6 1e-4 1e-3, findiff-t_$t.dat)
DATN = $(foreach n, 1000 300 100 30 10, findiff-t_1e-7_-n_$n.dat)

# norm for the convergence study
norm_dt.dat norm_dx.dat: norm.awk
# datafile are order rule as it require a lot of time to compute them
norm_dt.dat: | $(DATDT)
	bash -c 'for i in $(DATDT);\
		do \
			DT=`echo $$i | sed -e "s/findiff-t_//" -e "s/.dat//"`;\
			echo -ne "$$DT\t";\
			awk -f norm.awk findiff-t_1e-7.dat $$i;\
		done' > $@

norm_dx.dat: | $(DATN)
	bash -c 'for i in $(DATN);\
		do\
			N=`echo $$i | sed -e "s/findiff-t_1e-7_-n_//" -e "s/.dat//"`;\
			echo print\(1/$$N,end=\"\\t\"\) | $(PYTHON);\
			awk -f norm.awk findiff-t_1e-7_-n_1000.dat $$i;\
		done' > $@

#  prerequisites for the EPS figure pannels
cure-temp-cure.eps cure-temp-viscos.eps: cure.dat
deform_frameX.eps: trans_findiff.awk.dat
deform_tX_map.eps deform_time.eps: findiff.dat
norm_dx.eps: norm_dx.dat
norm_dt.eps: norm_dt.dat

%.eps: %.plt common.plt consolidation.gpm
	gnuplot $< > $@


# prerequisites for DVI files
%.dvi: psfrags.tex
consolidation.dvi: vf-strain.eps stress-strain.eps stress-vf.eps
cure.dvi: cure-temp-cure.eps cure-temp-viscos.eps
dcure.dvi: dcure-temp.eps dcure-cure.eps dcure-map.eps
error.dvi: stability.eps norm_dt.eps norm_dx.eps
heat.dvi: deform_frameX.eps deform_tX_map.eps deform_time.eps
permeab.dvi: permeab-vf.eps permeab-strain.eps 
viscosity.dvi: viscosity-temp.eps viscosity-cure.eps viscosity-map.eps

# rule for DVI figures
%.pdf: %.dvi
	dvipdf $*.dvi
	pdfcrop $@ $@

$(LOG): nots.tex $(FIGURES)
%.log: %.tex
	pdflatex $<


# ANIMATIONS
%.mp4: %/
	ffmpeg -framerate 4 -i $*/movie%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p $@

# DOWNLOAD AND UPLOAD OF EXPENSIVE SIMULATION RESULTS
TGZ = simulations.tar.gz
$(TGZ): $(DATN) $(DATDT)
	tar czvf $@ $+

.PHONY: download upload

download:
	-rm $(TGZ)
	wget http://wiener.ex.ac.uk/~tom/adapt/$(TGZ)
	tar xzvf $(TGZ) 
	tar tf $(TGZ) | xargs touch

upload: $(TGZ)
	scp $< wiener:~/Sites/adapt/

# REMOVE UNNECESSARY FILES
.PHONY: clean veryclean

clean:
	-rm *.eps *.dvi *.out *.mp4

clear:
	-rm *.aux *.bbl *.blg *.fdb_latexmk *.fls *.lof *.log *.lot *.nav *.out *.snm *.toc

veryclean: clear clean
	-rm *.dat
	-rm *.pdf *~
