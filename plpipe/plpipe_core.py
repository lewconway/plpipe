#! /usr/bin/env python
import sys
import numpy as np
import argparse
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from scipy.ndimage import gaussian_filter
import plotly.graph_objects as go
import re
from termcolor import colored
from .spg import spg_dict_html as spg_dict
from . import plpipe_templates
from itertools import cycle

xlabel = None
ylabel = None
vlabel = None


def parse():
    """Parse using argparse
    :returns: TODO

    """

    global xlabel, ylabel, vlabel

    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--resolution", default=None, type=int,
                        help="Resolution of image via interpolation")
    parser.add_argument("--text", action="store_true",
                        default=False, help="print a text/ascii plot")
    parser.add_argument("--vector", action="store_true",
                        default=False, help="attempt to convert to a vector image")
    parser.add_argument("--transpose", action="store_true",
                        default=False, help="transpose data")
    parser.add_argument("--dump", default=None, type=str,
                        help="dump interolated data to a file")
    parser.add_argument("-x", "--xlabel", default=None, type=str,
                        help="X label text")
    parser.add_argument("-y", "--ylabel", default=None, type=str,
                        help="y label text")
    parser.add_argument("--xlim", default=None, type=float, nargs=2,
                        help="xaxis limits")
    parser.add_argument("--ylim", default=None, type=float, nargs=2,
                        help="yaxis limits")
    parser.add_argument("-v", "--vlabel", default=None, type=str,
                        help="v label text [for surfaces]")
    parser.add_argument("--legend", action="store_true", default=False,
                        help="Show legend")
    parser.add_argument("--colorbar", action="store_true", default=False,
                        help="Show colorbar")
    parser.add_argument("-m", "--mode", default=None, type=str, nargs='*',
                        help="scatter plot mode for Plotly (markers, lines, markers + lines...)")
    parser.add_argument("--template", default=['basic'], type=str, nargs='*',
                        help="template[s] for plotting theme")
    parser.add_argument("--append", const=True, default=False, action='store_const',
                        help="make one figure with all data")
    args = parser.parse_args()

    xlabel = args.xlabel
    ylabel = args.ylabel
    vlabel = args.vlabel

    return args


def string_to_chem(string):
    string = re.sub(r'([0-9]+)', r'<sub>\1</sub>', string)
    return string


def setup_plotly(template='basic', fig=None):
    """TODO: sets up plotly with sensible layout
    :returns: TODO

    """
    if fig is None:
        fig = go.Figure()

    extras = {}
    for t in template.split('+'):
        try:
            extras.update(plpipe_templates.template_extras[t])
        except KeyError:
            pass
#
#    try:
#        extras = template.pop('extra')
#    except KeyError:
#        extras = None

    fig.update_layout(template=template)

    return fig, extras


fig = go.Figure()


def parse_stdin():
    """TODO: Docstring for parse_stdin.
    :returns: TODO

    """
    global xlabel, ylabel, vlabel
    with sys.stdin as f:
        fields = Fields()
        x = []
        v = []
        y = None
        tmp_field = Field(x=x)
        for line in f:
            splitline = line.split()
            if line.startswith('####') and vlabel is None:
                vlabel = line.strip('#').strip()
            elif line.startswith('###') and ylabel is None:
                ylabel = line.strip('#').strip()
            elif line.startswith('##') and xlabel is None:
                xlabel = line.strip('#').strip()
            elif line.startswith('#'):
                if len(tmp_field._x) > 0:
                    tmp_field.set_data(x=np.array(x), v=np.array(v))
                    fields.add_field(tmp_field)
                    tmp_field = Field()
                x = []
                v = []

                try:
                    y = np.array([float(i) for i in splitline[1:]])
                except ValueError:
                    y = splitline[1:]

                tmp_field.set_data(name=splitline[0][1:], y=y)
            else:
                x.append(float(splitline[0]))
                v.append([float(i) for i in splitline[1:]])
                tmp_field.set_data(x=np.array(x), v=np.array(v))
        fields.add_field(tmp_field)

    return fields


def overwrite_axes(fig, xlim, ylim):

    fig.update_layout({
        'xaxis': {'range': xlim},
        'yaxis': {'range': ylim}, })
    return fig


def write_plotly_image(fig, string='out'):
    """write plotly image to file

    :fig: TODO
    :string: TODO
    :returns: TODO

    """

    fig.write_image(string + '.png', scale=4)
    fig.write_image(string + '.svg', scale=4)
    fig.write_image(string + '.pdf', scale=4)
    fig.write_html(string + '.html')


class Field():

    """A class for 2d array data and metadata"""

    def __init__(self, name=None, x=None, y=None, v=None):
        """Initialize the field object with a name.

        :name: The name of the field.
        """
        self.set_data(name, x, y, v)

    def set_data(self, name=None, x=None, y=None, v=None):
        """Set data for the field.

        :name: The name of the field.
        :x: The x value.
        :y: The y value.
        :z: The z value.
        """

        if name is not None:
            self._name = name
        if x is not None:
            self._x = x
        if y is not None:
            self._y = y
        if v is not None:
            self._v = v

        if not hasattr(self, '_y') and hasattr(self, '_v'):
            self._y = ['data'] * np.shape(self._v)[1]

    def write_data(self, file=None):
        """for Debugging, write out data
        :returns: TODO

        """
        print(f'#{self._name}', end=' ', file=file)
        for i in self._y:
            print(f'{i}', end=' ', file=file)
        print(file=file)
        for i, j in zip(self._x, self._v):
            print(f'{i:15.8f}', end=' ', file=file)
            for jj in j:
                print(f'{jj:15.8f}', end=' ', file=file)
            print(file=file)

    def interpolate(self, xv, yv):
        """Interpolate field onto grid given by xv,yv

        :x: TODO
        :y: TODO
        :v: TODO
        :xv: TODO
        :yv: TODO
        :returns: TODO

        """
        from sklearn import preprocessing
        kernel = RBF()

        # Create the Gaussian Process Regressor
        gp = GaussianProcessRegressor(
            kernel=kernel, alpha=0.1, n_restarts_optimizer=0, normalize_y=True)

        X = []

        x = self._x
        try:
            y = self._y
        except AttributeError:
            y = [0]
        try:
            name = self._name
        except AttributeError:
            name = ''

        for xx in x:
            if len(y) > 1:
                for yy in y:
                    X.append([xx, yy])
            else:
                X.append(xx)

        V = self._v.flatten()
        if len(y) == 1:
            X = np.array(X).reshape(-1, 1)

        scaler = preprocessing.StandardScaler().fit(X)
        X = scaler.transform(X)

        # Fit the Gaussian Process Regressor to the data
        gp.fit(X, V)

        X_pred = []
        for xx in xv:
            if len(y) > 1:
                for yy in yv:
                    X_pred.append([xx, yy])
            else:
                X_pred.append(xx)

        if len(y) == 1:
            X_pred = np.array(X_pred).reshape(-1, 1)

        X_pred = scaler.transform(X_pred)

        # Predict values for the entire grid
        v_pred = gp.predict(X_pred)
        v_pred = np.reshape(v_pred, (np.size(xv), np.size(yv)))

        return Field(name=name + '[interpolated]', x=xv, y=yv, v=v_pred)

    def transpose(self):
        """Swap x and y
        :returns: TODO

        """
        return Field(name=self._name + '[transposed]',
                     x=self._y, y=self._x, v=self._v.T)

    def print_strips(self, filename='out', show_legend=False, mode='lines',
                     xlim=None, ylim=None, template='basic', fig=None):
        """Print each column as an individual line
        :returns: TODO

        """

        fig, extras = setup_plotly(template, fig)

        dash = ['solid']
        if extras is not None and mode is None:
            try:
                mode = extras['mode_list']
                dash = extras['dash_list']
            except KeyError:
                pass

        if mode is not None:
            mode_cycler = cycle(mode)
        if dash is not None:
            dash_cycler = cycle(dash)

        for i, column in enumerate(self._v.T):
            try:
                name = str(self._y[i])
                name = convert_labels_for_AIRSS([name])[0]
            except AttributeError:
                name = 'list'

            dash = next(dash_cycler)
            mode = next(mode_cycler)
            fig.add_trace(go.Scatter(x=self._x, y=column,
                                     mode=mode, name=name, line={'dash': dash},
                          showlegend=(show_legend and '-fit' not in name)))

        fig.update_layout(
            xaxis_title=xlabel, yaxis_title=vlabel,
            xaxis={'range': [np.min(self._x), np.max(self._x)]})

        fig = overwrite_axes(fig, xlim, ylim)
        write_plotly_image(fig, filename)

        return fig

    def print_field_img(self, labels=[], vector=False,
                        filename='out', show_legend=False, show_colorbar=False):
        """Prints array using plotly

        :data: TODO
        :returns: TODO

        """

        labels = convert_labels_for_AIRSS(labels)

        data = self._v.T

        fig, extras = setup_plotly()

        fig.update_layout(
            xaxis_title=xlabel, yaxis_title=ylabel)

        fig.update_layout({
            'colorway': ['#00b945', 'LemonChiffon'],
        })

        if show_legend:
            fig.update_layout({
                'legend': dict(x=0.025, y=1-0.025, xanchor='left', yanchor='top', bgcolor='White', borderwidth=1, bordercolor='Black')
            })

        colormap = 'sunset_r'

        mode_cycler = cycle(['markers', 'markers + lines'])
        for i, label in enumerate(labels):
            mode = next(mode_cycler)
            fig.add_trace(go.Scatter(x=[None], y=[None], mode=mode,
                                     showlegend=show_legend, name=label,
                                     marker={'color': [i],
                                             'symbol': 'square',
                                             'colorscale': colormap,
                                             'cmin': 0,
                                             'cmax': np.max(data)}),)

        if vector:
            data_blur = gaussian_filter(data, 2, output=float, mode="nearest")
            fig.add_trace(go.Contour(x=self._x, y=self._y, z=data_blur, showscale=False,
                                     line_smoothing=0, colorscale=colormap,
                                     contours=dict(showlabels=False, start=np.min(data_blur)+0.5,
                                                   end=np.max(data_blur), size=1, coloring='fill'),
                                     line_width=2))
        else:
            fig.add_trace(go.Heatmap(x=self._x, y=self._y, z=data,
                          showscale=show_colorbar, colorscale=colormap,
                                     colorbar=dict(
                                         title=vlabel,
                                         titleside="right",
                                         ticks="inside"
                                     )))

        write_plotly_image(fig, filename)

    def print_int_field_cli(self, labels=[],
                            color_mapping={0: 'red',
                                           1: 'green',
                                           2: 'yellow',
                                           3: 'blue',
                                           4: 'magenta',
                                           5: 'cyan'
                                           },
                            symbol_mapping={0: '@',
                                            1: '#',
                                            2: '$',
                                            3: '%',
                                            4: '*',
                                            5: '#'
                                            }):
        """Prints coloured symbols for each point to stdout

        :data: TODO
        :returns: TODO

        """
        for i, label in enumerate(labels):
            color = color_mapping.get(
                int(i*max(symbol_mapping))/max(symbol_mapping), 'white')
            print(colored(label, color), end=' ')
        print()

        data = np.flip(self._v.T, axis=0)

        data = data * max(symbol_mapping)
        data = data.astype(int) / max(symbol_mapping)

        for row in data:
            for value in row:
                # Default to white if value not found
                color = color_mapping.get(value, 'white')
                print(colored(symbol_mapping.get(value, 'X'), color), end=' ')
            print()  # Move to the next line

        # Reset color to default (optional)
        print(colored("", "white"))


class Fields(object):

    """A class containing several fields to be compared"""

    def __init__(self):
        """Sets up the empty list """
        self._fields = []

    def add_field(self, field):
        """Adds a field to the list

        :field: TODO
        :returns: TODO

        """
        self._fields.append(field)

    def update_field(self, name=None, x=None, y=None, v=None, index=-1):
        """Update a field at a given index

        :x: TODO
        :y: TODO
        :v: TODO
        :index: TODO
        :returns: TODO

        """
        self._fields[index].set_data(name=None, x=x, y=y, v=v)

    def get_names(self):
        """get names of each field
        :returns: TODO

        """
        return [i._name for i in self._fields]

    def get_min_field(self):
        """Returns the index of the field with the lowest value in each coordinate

        :returns: numpy integer array

        """
        stacked_array = np.stack([f._v for f in self._fields], axis=0)
        min_field = Field(name='min_field', x=self._fields[0]._x, y=self._fields[0]._y,
                          v=np.argmin(stacked_array, axis=0))

        return min_field

    def get_relative_field(self):
        """Returns the field values relative to the first

        :returns: list of numpy arrays

        """
        tmpfields = Fields()
        for f in self._fields:
            tmpfield = Field(name=f._name,
                             x=f._x,
                             y=f._y,
                             v=f._v - self._fields[0]._v)
            tmpfields.add_field(tmpfield)
        return tmpfields

    def write_all(self, file_name=sys.stdout):
        """for Debugging

        :f: TODO
        :returns: TODO

        """

        global xlabel, ylabel, vlabel

        if type(file_name) is str:
            with open(file_name, 'w') as file:
                print(f'####{vlabel}', file=file)
                print(f'###{ylabel}', file=file)
                print(f'##{xlabel}', file=file)
                for i in self._fields:
                    i.write_data(file)
        else:
            file = file_name
            print(f'####{vlabel}', file=file)
            print(f'###{ylabel}', file=file)
            print(f'##{xlabel}', file=file)
            for i in self._fields:
                i.write_data(file)

    def interpolate_all(self, xv, yv):
        """ Use Gaussian regression to interpolate data onto grid

        :x: TODO
        :y: TODO
        :v: TODO
        :returns: TODO

        """

        fields_interpolated = Fields()
        for field in self._fields:
            f = field.interpolate(xv, yv)
            fields_interpolated.add_field(f)

        return fields_interpolated

    def transpose_all(self):
        """transpose all fields
        :returns: TODO

        """

        global xlabel, ylabel, vlabel

        fields_transposed = Fields()
        for field in self._fields:
            f = field.transpose()
            fields_transposed.add_field(f)

        tmp = xlabel
        xlabel = ylabel
        ylabel = tmp

        return fields_transposed


def convert_labels_for_AIRSS(labels):
    """TODO: Docstring for convert_labels_for_AIRSS.

    :labels: a list of strings of the form <N>-<FORMULA>-<SPACEGROUP>
    as used in airss by the 'name' function. eg. 1-C-Fd-3c
    :returns: A Formatted HTML string that looks like <Formula> [<Spacegroup>] with the correct subscripts and overbars.

    """
    labels_new = []
    for label in labels:
        try:
            label = label.split('[')[0]
            labeltmp = string_to_chem(label.split('-')[1].split('*')[-1]) + r' '
            if '-' in label:
                label = labeltmp + \
                    r'[<i>' + spg_dict['-'.join(label.split('-')[2:])] + r'</i>] '
        except KeyError:
            label = label
        except IndexError:
            label = label
        labels_new.append(label)

    return labels_new
