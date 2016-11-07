load 'common.plt'
load 'consolidation.gpm'

set key bottom

set xrange [20:200]
# set yrange [-5:18]

set xtics 50
# set ytics 0.0005

set logscale y
set format y "%h"

set xlabel "TEMP"
set ylabel "DCURE"

plot  dcure(CtK(x),0.02) t 'CURE1', dcure(CtK(x),0.2) t 'CURE2', dcure(CtK(x),0.4) t 'CURE3'