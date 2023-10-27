# Simple command line tools to make decent looking plots

I often find that i want to do something like:

```
cat <output_of_some_process> | grep 'some matching pattern' | awk '{print $1, $2}'  > data
```

And I want to quickly make a plot of the columned data. I could probably use 

```
cat data | gracebat -hdevice PNG -hardcopy -printfile out.png -pipe -nxy - -fixed 3840 2160
```

But I find xmgrace to be a bit clunky when it comes to doing anything fancy such as adding labels etc.

This python library attempts to make a version of this which 
- Reads data from stdin
- Uses Plotly
- Looks good by default
- Can do some basic interpolation
- Can plot 1D and 2D data
- Can call custom templates [WIP]

## Basic usage:
```
> cat data
####Energy  (eV/C)
###1+c/a 
##Position  (Fractional  Coordinates)
#DATA1           0            1
0           25.0         37.5
1           20.25        20.75625
2           16.0         9.600000000000001
...
```

```
cat data | pl-line'
```

<img src='images/USAGE0.png' width='250'>

### Overwrite axis labels
```
cat data | pl-line -x 'Nice xlabel [ABO<sub>3</sub>]' -v 'Another Nice label' 
```

<img src='images/USAGE1.png' width='250'>

### Interpolate data (along both axes) and plot lines
```
cat data | pl-line -R 100 -m 'lines'
```

<img src='images/USAGE2.png' width='250'>

### Interpolate data (along both axes) and plot surface
```
cat data | pl-surf -R 100 --colorbar
```

<img src='images/USAGE3.png' width='250'>

### Read two gridded fields, interpolate them and plot the lowest  (ie. phase diagram)
```
>cat data
####Energy  (eV/C)
###1+c/a
##Position  (Fractional  Coordinates)
#DATA1      0.00000000      1.00000000
     0.00000000     25.00000000     37.50000000
     1.00000000     20.25000000     20.75625000
    ...
    19.00000000     20.25000000     20.75625000
    20.00000000     25.00000000     37.50000000
#DATA2      0.00000000      1.00000000
     0.00000000     1.00000000     1.00000000
     1.00000000     1.00000000     1.00000000
     2.00000000     1.00000000     1.00000000
    ...
    19.00000000     1.00000000     1.00000000
    20.00000000     1.00000000     1.00000000
```

```
cat data | pl-phase -R 100 --colorbar
```

<img src='images/USAGE4.png' width='250'>

```
cat data | pl-phase -R 100 --colorbar --vector
```

<img src='images/USAGE5.png' width='250'>
