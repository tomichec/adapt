load 'common.plt'
load 'consolidation.gpm'

set key off

xmax = Va - 0.03
set xrange [V0:xmax]

set xtics 0.025

set xlabel "VFRAC"
set ylabel "STRESS"

plot stress(x)
