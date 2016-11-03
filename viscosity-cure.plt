load 'common.plt'
load 'consolidation.gpm'

set key samplen 2 left

set xrange [0:0.4]
# set yrange [-5:18]

set xtics 0.1
set ytics 5

set xlabel "CURE"
set ylabel "VISCOS"

plot log(mu(CtK(100),x)) t 'TEMP1xxxx', log(mu(CtK(130),x)) t 'TEMP2xxxx', log(mu(CtK(180),x)) t 'TEMP3xxxx'