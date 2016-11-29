# %.pdf: %.eps
# 	epstopdf --autorotate=All $<
# # %.dvi: %.tex nots_TS.tex macros_TS.tex
# # 	${COMMENT}
# # 	latex $<
# %.raweps: %.dvi
# 	${COMMENT}
# 	dvips -E -i -p 1 -o $* $<
# #       $(DVIPS) -E -i -K -p 1 -o $* $< # -K options seems to make %.raweps +non-readable
# 	mv $*001 $@
# %.eps: %.raweps
# 	${COMMENT}
# 	epstool --copy --bbox $< $@
# ###################

# all: galerkin.out finel.pdf

# findiff-t_1e-6_-n_100.dat -- takes real time 1m1.576s
DATDT = $(foreach t, 1e-7 1e-6 1e-4 1e-3, findiff-t_$t.dat)
DATN = $(foreach n, 1000 300 100 30 10, findiff-t_1e-7_-n_$n.dat)

.PRECIOUS: $(DATDT) $(DATN)

all: consolidation.pdf permeab.pdf viscosity.pdf dcure.pdf cure.pdf fibre_bed.pdf galerkin.out element.out findiff.dat cons_viscos.mp4 error.pdf

# also creates a plot
%.out: %.py
	python3 $< > $@

trans_%.dat: %.dat
	awk -f transpose.awk $< > $@

findiff%.dat: findiff.py
	python3 $< $(subst _, ,$*) > $@

%.dat: %.py
	python3 $< > $@

norm_dt.dat: $(DATDT)
	bash -c 'for i in $+;\
		do \
			DT=`echo $$i | sed -e "s/findiff-t_//" -e "s/.dat//"`;\
			echo -ne "$$DT\t";\
			awk -f findiff_norm.awk findiff-t_1e-7.dat $$i;\
		done' > $@

norm_dx.dat: $(DATN)
	bash -c 'for i in $+;\
		do\
			N=`echo $$i | sed -e "s/findiff-t_1e-7_-n_//" -e "s/.dat//"`;\
			echo print\(1/$$N,end=\"\\t\"\) | python;\
			awk -f findiff_norm.awk findiff-t_1e-7_-n_1000.dat $$i;\
		done' > $@

# report.pdf: notes.tex galerkin.out
# 	pdflatex $<

# slides.pdf: slides.tex
# 	pdflatex $<

# %.pdf: %.tex $(PLT)
# 	latex $<

consolidation.dvi: consolidation.tex vf-strain.eps stress-strain.eps stress-vf.eps 
	latex $<

permeab.dvi: permeab.tex permeab-vf.eps permeab-strain.eps 
	latex $<

viscosity.dvi: viscosity.tex viscosity-temp.eps viscosity-cure.eps viscosity-map.eps
	latex $<

dcure.dvi: dcure.tex dcure-temp.eps dcure-cure.eps dcure-map.eps
	latex $<

cure.dvi: cure.tex cure-temp-cure.eps cure-temp-viscos.eps
	latex $<

fibre_bed.dvi: fibre_bed.tex
	latex $<

heat.dvi: heat.tex deform_frameX.eps deform_tX_map.eps deform_time.eps
	latex $<

error.dvi: error.tex stability.eps norm_dt.eps norm_dx.eps norm_dt.dat norm_dx.dat
	latex $<

%.pdf: %.dvi
	dvipdf $*.dvi
	pdfcrop $@ $@

%.eps: %.plt common.plt consolidation.gpm cure.dat findiff.dat trans_findiff.dat norm_dt.dat
	gnuplot $< > $@

# %.mp4: %/
# 	ffmpeg -framerate 4 -i $*/movie%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p $@
