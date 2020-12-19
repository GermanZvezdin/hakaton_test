import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import time
import dash_html_components as html
import dash_daq as daq

# https://dash.plotly.com/external-resources
app = dash.Dash(__name__)


app.layout = html.Div(
    className="frame-80",
    children=[
        html.Div(className="rectangle-101"),
        html.Div(className="rectangle-103"),
        html.Img(className="track-1", src="https://anima-uploads.s3.amazonaws.com/projects/5fdd53490136fca9d0284658/releases/5fdd5358c90a83f6a684adb0/img/track-1@2x.svg"),
        html.H1("Отслеживание государственных закупок",className="otslezhiva-akupok-416 montserrat-bold-white-24px border-class-1"),
        html.Div(className="rectangle-104"),
        html.Img(className="group-137 smart-layers-pointers", src="https://anima-uploads.s3.amazonaws.com/projects/5fdd53490136fca9d0284658/releases/5fdd5358c90a83f6a684adb0/img/group-137@2x.svg"),
        html.Div("Участник",className="uchastnik-444 montserrat-medium-manatee-14px border-class-1"),
        html.Img(className="group-1",src="https://anima-uploads.s3.amazonaws.com/projects/5fdd53490136fca9d0284658/releases/5fdd5358c90a83f6a684adb0/img/group-1@2x.svg"),
        html.Div("Победитель",className="pobeditel-443 montserrat-bold-blue-14px border-class-1"),
        html.Img(className="rank-1",src="https://anima-uploads.s3.amazonaws.com/projects/5fdd53490136fca9d0284658/releases/5fdd5358c90a83f6a684adb0/img/rank-1@2x.svg"),
        html.Img(className="ellipse-87",src="https://anima-uploads.s3.amazonaws.com/projects/5fdd53490136fca9d0284658/releases/5fdd5358c90a83f6a684adb0/img/ellipse-87@2x.svg")
        ])

if __name__ == '__main__':
    app.run_server(debug=True)