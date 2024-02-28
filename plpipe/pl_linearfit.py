#! /usr/bin/env python
from .plpipe_core import parse, parse_stdin, Fields
import numpy as np
import sys


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """

    args = parse()

    if args.xlim is not None:
        print(
            f'only fitting between {args.xlim[0]} and {args.xlim[1]}', file=sys.stderr)

    new_fields = Fields()
    fields = parse_stdin()

    for field in fields._fields:

        if args.xlim is not None:
            filt = (field._x < args.xlim[1]) * (field._x > args.xlim[0])
            a = np.polyfit(field._x[filt], field._v[filt], 1)
        else:
            a = np.polyfit(field._x, field._v, 1)

        v_fit = []
        for x in field._x:
            v_fit.append(a[0] * x + a[1])

        y_fit = ['_' + _ + '-fit' for _ in field._y]

        # Convoluted way to interlace fitted and raw
        y_new = [val for pair in zip(field._y, y_fit) for val in pair]

        v_tmp = np.hstack([field._v, v_fit]).T

        v = 0 * v_tmp

        n = np.shape(v_tmp)[0]

        v[0::2] = v_tmp[0:int(n/2)]
        v[1::2] = v_tmp[int(n/2):]

        v = v.T

        field.set_data(x=field._x, y=y_new, v=v, name='DATA')
        new_fields.add_field(field)
        print(f'M={a[0][0]:15.8f}; C={a[1][0]:15.8f}', file=sys.stderr)

    new_fields.write_all()


if __name__ == "__main__":
    main()
