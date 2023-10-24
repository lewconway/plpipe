
cat example_01 | tr - ' ' | awk '{print $2, $5}' | sort | pl-line 

mv out.png example_01.png
rm out.*

cat example_01 | tr - ' ' | awk '{print $2, $5}' | sort | pl-line  -R 100

mv out.png example_01_interpolated.png
rm out.*
