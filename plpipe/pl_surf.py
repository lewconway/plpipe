#! /usr/bin/env python3.9
from .plpipe_core import parse, parse_stdin
import numpy as np


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """

    args = parse()

    fields = parse_stdin()

    if args.transpose:
        fields = fields.transpose_all()

    fields_out = fields
    if args.dump is not None:
        fields.write_all(args.dump)

    if args.resolution is not None:
        resolution = (args.resolution, args.resolution)
        x_interpolated = np.linspace(np.min(fields._fields[0]._x),
                                     np.max(fields._fields[0]._x),
                                     resolution[0])
        y_interpolated = np.linspace(np.min(fields._fields[0]._y),
                                     np.max(fields._fields[0]._y),
                                     resolution[1])
        fields_interpolated = fields.interpolate_all(x_interpolated, y_interpolated)
        fields_out = fields_interpolated

    for i, field in enumerate(fields_out._fields):
        if args.text:
            field.print_int_field_cli()
        else:
            field.print_field_img(fields_out.get_names(), args.vector,
                                  show_legend=args.legend,
                                  show_colorbar=args.colorbar,
                                  filename='out' + str(i))

    if args.dump is not None:
        fields.write_all(args.dump)


if __name__ == "__main__":
    main()
