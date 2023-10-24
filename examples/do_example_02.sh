cat example_02 | pl-line

mv out.png example_02.png
rm out.*

cat example_02 | pl-line -R 16

mv out.png example_02_interpolated.png
rm out.*

cat example_02 | pl-surf -R 128

mv out0.png example_02_interpolated_surf.png
rm out0.*
