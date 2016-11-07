load 'common.plt'
load 'consolidation.gpm'

# set key left 
set pm3d map
set palette gray
unset colorbox 

set lmargin 7

set xrange [20:200]
set yrange [0:0.45]

set contours
set cntrparam levels incremental 0,3,9

set isosamples 50

set xlabel 'TEMP'
set ylabel 'CURE'

set xtics 50

splot log10(mu(CtK(x),y)) t 'VISC'
