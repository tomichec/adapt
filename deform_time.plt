load 'common.plt'
load 'consolidation.gpm'

datafile="findiff.dat"

set xlabel "TIME"
set ylabel "DISP"

set key autotitle columnheader reverse left bottom

set lmargin 10
set rmargin 2

set xtics 0.1
set ytics 0.005

set yrange [-0.025:0.001]

plot datafile u 1:"0.000" w l, '' u 1:"0.200" w l, '' u 1:"0.500" w l, '' u 1:"1.000" w l