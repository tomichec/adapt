load 'common.plt'
datafile = "norm_dt.dat"
f(x) = m*x+b
fit f(x) datafile using 1:2 via m,b
titlefit = sprintf("{ORD}({DX}^{%.2f})",m)

# set xrange [1e-5:1e-1*1.1]

# set logscale x 10
# set logscale y 10
# set format x "10^{%T}" 
# set format y "10^{%T}" 

set ytics 1
set xtics 1

# L for logarithmic
set ylabel "LNORM"
set xlabel "LDT" 

set key bottom spacing 1.3

plot datafile u 1:2 w p ps 2 t "LNORM", f(x) w l t titlefit