load 'common.plt'
# load 'consolidation.gpm'

set key autotitle columnheader reverse left bottom

set ylabel "DISP"
set xlabel "FRAME"

set xtics 0.2
set ytics 0.005

set yrange [-0.025:0.001]

datafile="findiff_trans.dat"

plot datafile u "000":"0.000" with lp,'' u "000":"0.100" with lp, '' u "000":"0.200" with lp, '' u "000":"0.400" with lp
