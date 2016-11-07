load 'common.plt'
load 'consolidation.gpm'

set key left 
set pm3d map
set palette gray negative
unset colorbox 

set lmargin 5

set xrange [100:200]
set yrange [0:1]
set contours
set isosamples 50

set xlabel 'TEMP'
set ylabel 'CURE'

set xtics 25

splot dcure(CtK(x),y) t 'DCURE'
