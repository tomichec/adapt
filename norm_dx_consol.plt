load 'common.plt'

datafile = 'norm_dx_consol.dat'

# set xrange [1e-5:1e-1*1.1]

# set logscale x 10
# set logscale y 10
# set format x "10^{%T}" 
# set format y "10^{%T}" 

set ytics 0.5
set xtics 0.5

set ylabel "LNORM"
set xlabel "LDX" 

set key bottom spacing 1.3

f(x) = m*x+b
fit f(x) datafile using 1:2 via m,b
titlefit = sprintf("{ORD}({DX}^{%.2f})",m)

plot datafile u 1:2 w p ps 2 t "LNORM", f(x) w l t titlefit