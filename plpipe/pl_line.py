#! /usr/bin/env python
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
        try:
            y_interpolated = np.linspace(np.min(fields._fields[0]._y),
                                         np.max(fields._fields[0]._y), resolution[1])
        except AttributeError:
            y_interpolated = np.arange(np.shape(fields._fields[0]._v)[1])

        fields_interpolated = fields.interpolate_all(
            x_interpolated, y_interpolated)
        fields_out = fields_interpolated

    template_list = ['basic']
    [template_list.append(_) for _ in args.template]
    template_string = '+'.join(template_list)
    fig = None
    i = 0
    for f in fields_out._fields:
        fig = f.print_strips(show_legend=args.legend, mode=args.mode, filename='out' + str(i),
                             xlim=args.xlim, ylim=args.ylim, fig=fig,
                             template=template_string)
        if not args.append:
            fig = None
            i += 1

    if args.dump is not None:
        fields_out.write_all(args.dump)


if __name__ == "__main__":
    main()
