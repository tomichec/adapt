load 'common.plt'
load 'consolidation.gpm'

set key samplen 2

set xrange [20:200]

set xtics 50
set ytics 5

set xlabel "TEMP"
set ylabel "VISCOS"

plot log(mu(CtK(x),0.1)) t 'CURE1', log(mu(CtK(x),0.2)) t 'CURE2', log(mu(CtK(x),0.4)) t 'CURE3'