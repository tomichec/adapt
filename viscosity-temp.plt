load 'common.plt'
load 'consolidation.gpm'

set key samplen 2

set xrange [20:200]

set xtics 50
set ytics 5

set xlabel "TEMP"
set ylabel "VISCOS"

plot log10(mu(CtK(x),0.02)) t 'CURE1', log10(mu(CtK(x),0.2)) t 'CURE2', log10(mu(CtK(x),0.4)) t 'CURE3'