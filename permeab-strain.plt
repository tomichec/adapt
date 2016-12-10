load 'common.plt'
load 'consolidation.gpm'

set key off

xmax = Va - 0.03
set xrange [V0:xmax]

set xrange [-0.154:0]

set xtics 0.05 
set ytics 1e-6

set format y "%.0s{I}10^{%T}"

set xlabel "STRAIN"
set ylabel "PERMEAB"

plot K(vf(x))
