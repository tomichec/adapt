load 'common.plt'
load 'consolidation.gpm'

set key off

set xrange [-0.154:0]

xmax = Va - 0.03
set yrange [V0:xmax]


set xtics 0.05
set ytics 0.025

set xlabel "STRAIN"
set ylabel "VFRAC"

plot vf(x)
