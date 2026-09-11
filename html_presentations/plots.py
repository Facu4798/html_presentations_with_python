import json
from html import escape
from itertools import count

from .elements import Element


_PLOTLY_URL = "https://cdn.plot.ly/plotly-2.35.2.min.js"
_PLOT_IDS = count(1)


def _json(value):
    if hasattr(value, "to_dict"):
        value = value.to_dict(orient="list")
    return value


def _series_data(data):
    data = _json(data)
    if isinstance(data, dict):
        return {"x": list(data.keys()), "y": list(data.values())}
    if isinstance(data, (list, tuple)):
        return {"y": list(data)}
    raise TypeError("Plot data must be a list, tuple, dictionary, or DataFrame")


def _escape_script(value):
    return value.replace("</", "<\\/")


class Plot(Element):
    plot_type = "scatter"

    def __init__(self, data=None, css_class=None, alignment=None, width=None, height=360, **kwargs):
        super().__init__("div", css_class=css_class or "plot-container", alignment=alignment)
        self.plot_id = f"plot-{next(_PLOT_IDS)}"
        self.width = width
        self.height = height
        self.data = data
        self.options = dict(kwargs)
        self.layout = {}
        self.traces = []
        self._build_traces(data)

    def _build_traces(self, data):
        series = _series_data(data)
        trace = dict(series)
        trace["type"] = self.plot_type
        self.traces = [trace]

    def addVLine(self, value, **kwargs):
        self.layout.setdefault("shapes", []).append(
            {
                "type": "line",
                "x0": value,
                "x1": value,
                "y0": 0,
                "y1": 1,
                "yref": "paper",
                **kwargs,
            }
        )
        return self

    def addHLine(self, value, **kwargs):
        self.layout.setdefault("shapes", []).append(
            {
                "type": "line",
                "y0": value,
                "y1": value,
                "x0": 0,
                "x1": 1,
                "xref": "paper",
                **kwargs,
            }
        )
        return self

    def setTitle(self, title):
        self.layout["title"] = title
        return self

    def setLabels(self, x=None, y=None):
        if x is not None:
            self.layout.setdefault("xaxis", {})["title"] = x
        if y is not None:
            self.layout.setdefault("yaxis", {})["title"] = y
        return self

    def _figure(self):
        layout = dict(self.layout)
        options = dict(self.options)
        layout.update(options.pop("layout", {}))
        return {"data": self.traces, "layout": layout, "config": options}

    def render(self):
        style = []
        if self.width is not None:
            width = f"{self.width}px" if isinstance(self.width, (int, float)) else str(self.width)
            style.append(f"width:{escape(width, quote=True)}")
        if self.height is not None:
            height = f"{self.height}px" if isinstance(self.height, (int, float)) else str(self.height)
            style.append(f"height:{escape(height, quote=True)}")
        style_attr = f' style="{";".join(style)}"' if style else ""
        class_attr = escape(self._render_class(), quote=True)
        figure = _escape_script(json.dumps(self._figure(), separators=(",", ":"), default=str))
        return (
            f'<div id="{escape(self.plot_id, quote=True)}" class="{class_attr}"{style_attr}></div>'
            f'<script src="{_PLOTLY_URL}"></script>'
            f'<script>Plotly.newPlot({json.dumps(self.plot_id)}, {figure}.data, '
            f'{figure}.layout, {figure}.config);</script>'
        )


class Line(Plot):
    plot_type = "scatter"

    def _build_traces(self, data):
        series = _json(data)
        if isinstance(series, dict) and all(isinstance(value, (list, tuple)) for value in series.values()):
            self.traces = [
                {"type": "scatter", "mode": "lines", "name": name, "y": list(values)}
                for name, values in series.items()
            ]
            return
        trace = _series_data(data)
        trace.update({"type": "scatter", "mode": "lines+markers"})
        self.traces = [trace]


class Bar(Plot):
    plot_type = "bar"


class Box(Plot):
    plot_type = "box"

    def _build_traces(self, data):
        series = _json(data)
        if isinstance(series, dict):
            self.traces = [
                {"type": "box", "name": name, "y": list(values)}
                for name, values in series.items()
            ]
            return
        super()._build_traces(data)
        self.traces[0]["type"] = "box"


class Hist(Plot):
    plot_type = "histogram"


class Pie(Plot):
    plot_type = "pie"

    def _build_traces(self, data):
        series = _json(data)
        if not isinstance(series, dict):
            raise TypeError("Pie data must be a dictionary of labels to values")
        self.traces = [{"type": "pie", "labels": list(series.keys()), "values": list(series.values())}]


__all__ = ["Plot", "Line", "Bar", "Box", "Hist", "Pie"]
