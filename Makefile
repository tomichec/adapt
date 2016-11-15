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

all: consolidation.pdf permeab.pdf viscosity.pdf dcure.pdf cure.pdf fibre_bed.pdf galerkin.out element.out findiff.out cons_viscos.mp4

# also creates a plot
%.out: %.py
	python3 $< > $@

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

heat.dvi: heat.tex
	latex $<

cure.dat: cure.py
	python3 $< > $@

%.pdf: %.dvi
	dvipdf $*.dvi
	pdfcrop $@ $@

%.eps: %.plt common.plt consolidation.gpm cure.dat
	gnuplot $< > $@

%.mp4: %/
	ffmpeg -framerate 4 -i $*/movie%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p $@
