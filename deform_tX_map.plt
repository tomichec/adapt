load 'common.plt'

# set key center top outside title ""

set pm3d map interpolate 0,0
set palette gray
set colorbox front
set cbtics 0.01

set contours

set lmargin 7
set rmargin at screen 0.78

set ylabel "TIME"
set xlabel "FRAME"

set xtics 0.2
set ytics 0.1

splot "findiff.dat" matrix nonuniform t ''