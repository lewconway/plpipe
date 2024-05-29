
cat example_01 | tr - ' ' | awk '{print $2, $5}' | sort | pl-line 

mv out0.png example_01.png
rm out0.*

cat example_01 | tr - ' ' | awk '{print $2, $5}' | sort | pl-line  -R 100

mv out0.png example_01_interpolated.png
rm out0.*
