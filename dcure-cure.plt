load 'common.plt'
load 'consolidation.gpm'

set key samplen 2 left

set xrange [0:1]
set yrange [0:0.0014]

# set xtics 50
set ytics 0.0002

# set format y '%.1sx10^{%T}'

set xlabel "CURE"
set ylabel "DCURE"

plot  dcure(CtK(100),x) t 'TEMP1xxxx', dcure(CtK(130),x) t 'TEMP2xxxx', dcure(CtK(180),x) t 'TEMP3xxxx'