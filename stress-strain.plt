load 'common.plt'
load 'consolidation.gpm'

set key off

set xrange [-0.154:0]

set xtics 0.05

set xlabel "STRAIN"
set ylabel "STRESS"

plot stress(vf(x))
