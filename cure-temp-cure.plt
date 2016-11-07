load 'common.plt'
load 'consolidation.gpm'

set key samplen 2 left

set xrange [0:2*60]
# set yrange [-5:18]
set y2range [20:200]

set xtics 30
set ytics nomirror 0.2

set y2tics 50

set format y2 ""


set xlabel "TIME"
set ylabel "CURE"
# set y2label "TEMP"

plot 'cure.dat' u ($1/60.):3  w l t 'CURE', '' u ($1/60.):2 w l t 'TMPR' axes x1y2
