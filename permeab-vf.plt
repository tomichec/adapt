load 'common.plt'
load 'consolidation.gpm'

set key off

xmax = Va - 0.03
set xrange [V0:xmax]

set xtics 0.025
set ytics 1e-6

set format y "%.0s{I}10^{%T}"

# '%.0s*10^%T'

set xlabel "VFRAC"
set ylabel "PERMEAB"

plot K(x)
