load 'common.plt'
# load 'consolidation.gpm'

set key autotitle columnheader reverse left bottom

set ylabel "DISP"
set xlabel "FRAME"

set xtics 0.2
set ytics 0.005

set yrange [-0.025:0.001]

datafile="trans_findiff.awk.dat"

plot datafile u "000":"0.00" with lp,'' u "000":"0.10" with lp, '' u "000":"0.20" with lp, '' u "000":"0.40" with lp
