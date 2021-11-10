reset

set term qt

set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb "black" behind

unset key                                

set title "Axis Plot" font ",15" tc rgb "white"
set xlabel "X coordinates" font ",12" tc rgb "white"
set ylabel "Y coordinates" font ",12" tc rgb "white"

set xrange[-1.85e11:1.85e11]
set yrange[-1.85e11:1.85e11]
set grid back ls 0 lc rgb "white"
set border lw 3 lc rgb "white"

plot "Position_cord.txt" u 2:3 lc 10 lw 3 w l title "Orbit","Sun.txt" u 3:4 lt 7 lc 22 ps 3 w p title "Earth",\
"Sun.txt" u 1:2 lt 7 lc 4 ps 6 w p title "Sun","Major.txt" u 1:2 lw 3 lt rgb "#F7E3AF" w l,"Minor.txt" u 1:2 lw 3 lt rgb "#F7E3AF" w l
#c9a8ce
