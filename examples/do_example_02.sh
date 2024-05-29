cat data | pl-line

mv out0.png example_02.png
rm out0.*

cat data | pl-line -R 16

mv out0.png example_02_interpolated.png
rm out0.*

cat data | pl-surf -R 128

mv out0.png example_02_interpolated_surf.png
rm out0.*
