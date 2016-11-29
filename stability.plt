load 'common.plt'

# instability estimate
Dmax = 1
dt(dx) = dx*dx/Dmax

set xrange [1e-3:1e-1*1.1]

set logscale x 10
set logscale y 10
set format x "10^{%T}" 
set format y "10^{%T}" 

set ytics 0.01
# set ytics 0.01

set xlabel "DX"
set ylabel "DT" 

set key off

plot dt(x)

