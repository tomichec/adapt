load 'common.plt'
load 'consolidation.gpm'

datafile="findiff.dat"

set xlabel "TIME"
set ylabel "DISP"

plot for [i=2:11] datafile u 1:i w l