# modified implicit rule for the .tex files
TEX=latex

PYTHON=python3

# figures used in the process
FIG = consolidation\
	heat\
	permeab\
	viscosity\
	dcure\
	cure\
	error\
	consol

FIGURES = $(foreach f, $(FIG), $f_fig.pdf) fibre_bed_diag.pdf

# as pdf generation uses latex, the target are logfiles -- the pdf is side product
AUX = report.aux slides.aux

.PHONY: all aux

all: aux $(AUX)

aux: $(FIGURES) element.out galerkin.out 

# output from python scripts
%.out: %.py
	$(PYTHON) $< > $@

# datafiles from python scripts
%.dat: %.py
	$(PYTHON) $< > $@

# findiff file, which requires command line arguments
.PRECIOUS: findiff%.dat consol%.dat
findiff%.dat: findiff.py
	$(PYTHON) $< $(subst _, ,$*) > $@

consol%.dat: findiff_consol.py
	$(PYTHON) $< $(subst _, ,$*) > $@

# transpose of the datafile
trans_%.awk.dat: trans.awk %.dat
	awk -f $+ > $@

# datafile for the convergence study
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

# simulation results for the "realistic simulations"
CONSOL = $(foreach n, 10 70 100, consol-t_1e-4_-n_$n.dat)

consol%.eps: consol%.dat common.plt consol_tX_map.plt
	echo 'datafile="$<"' | cat - $(lastword $+) | gnuplot > $@

#  prerequisites for the EPS figure pannels
cure-temp-cure.eps cure-temp-viscos.eps: cure.dat
deform_frameX.eps: trans_findiff.awk.dat
deform_tX_map.eps deform_time.eps: findiff.dat
norm_dx.eps: norm_dx.dat
norm_dt.eps: norm_dt.dat

# technicaly the consolidation is a dependency only for some plots (see `grep consolidation.gpm *.plt`)
cure-temp-viscos.eps dcure-cure.eps dcure-map.eps dcure-temp.eps permeab-strain.eps permeab-vf.eps stress-strain.eps stress-vf.eps vf-strain.eps viscosity-cure.eps viscosity-map.eps viscosity-temp.eps : consolidation.gpm
%.eps: %.plt common.plt
	cat $< | gnuplot > $@

consolidation_fig.tex: vf-strain.eps stress-vf.eps stress-strain.eps
cure_fig.tex: cure-temp-cure.eps cure-temp-viscos.eps
dcure_fig.tex: dcure-temp.eps dcure-cure.eps dcure-map.eps
error_fig.tex: stability.eps norm_dt.eps norm_dx.eps
heat_fig.tex: deform_time.eps deform_frameX.eps deform_tX_map.eps
permeab_fig.tex: permeab-vf.eps permeab-strain.eps 
viscosity_fig.tex: viscosity-temp.eps viscosity-cure.eps viscosity-map.eps
consol_fig.tex: $(CONSOL:.dat=.eps)

# TODO: the _fig.tex are not removed -- why?
%_fig.tex: | tablemacro.pl figure_template.text
	perl $(firstword $|) $+ | cat - $(lastword $|) > $@

# prerequisites for DVI files
%.dvi: %.tex psfrags.tex

# rule for DVI figures
# is psfrags.tex needed as dependency?
%_fig.pdf: %_fig.dvi
	dvipdf $<
	pdfcrop $@ $@
# TODO: duplicated recipe -- can be made more concise?
%_diag.pdf: %_diag.dvi
	dvipdf $<
	pdfcrop $@ $@

$(AUX): nots.tex $(FIGURES)
%.aux: %.tex
	pdflatex $<
	bibtex $@
	pdflatex $<


# ANIMATIONS
%.mp4: %/
	ffmpeg -framerate 4 -i $*/movie%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p $@

# DOWNLOAD AND UPLOAD OF EXPENSIVE SIMULATION RESULTS
TGZ = simulations.tar.gz
$(TGZ): $(DATN) $(DATDT) $(CONSOL)
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
	-rm *.eps *.dvi *.out *.mp4 *_fig.tex

clear:
	-rm *.aux *.bbl *.blg *.fdb_latexmk *.fls *.lof *.log *.lot *.nav *.out *.snm *.toc

veryclean: clear clean
	-rm *.dat
	-rm *.pdf *~
