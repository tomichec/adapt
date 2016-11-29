load 'common.plt'

# set xrange [1e-5:1e-1*1.1]

set logscale x 10
set logscale y 10
set format x "10^{%T}" 
set format y "10^{%T}" 

# set ytics 0.01
# # set ytics 0.01

set ylabel "NORM"
set xlabel "DT" 

set key off

plot "norm_dt.dat" u 1:2 w p ps 2 t "DTNORM"