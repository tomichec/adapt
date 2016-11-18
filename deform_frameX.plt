load 'common.plt'
# load 'consolidation.gpm'

unset key

set ylabel "DISP"
set xlabel "FRAME"

set ytics 0.01
set xtics 0.2

datafile="findiff.dat"

plot datafile matrix nonuniform every 1:10 with lines