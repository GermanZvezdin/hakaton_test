import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import time
import dash_html_components as html
import dash_daq as daq
import dash_table as dt
import pandas as pd

app = dash.Dash(__name__)

df = pd.read_csv('/home/alex/Downloads/notifications.csv')
print(df.columns)
app.layout = html.Div(
    className="frame-84",
    children=[
        html.Div(className="rectangle-108"),
        html.Div(className="rectangle-109"),
        html.H1("Отслеживание государственных закупок",className="otslezhiva-upok-10114 montserrat-bold-white-24px border-class-1"),
       	html.Div(className="releases-110",
       				children=[
       				html.Div(
       					className="Menu-bar",
       					children=[
       						html.Span(
       						className="Input-1",
		       				children=[
		       					dcc.Input(className="basic-slide"),
		       					html.Label("->")
		       				]),
		       				html.Div(className="params",
		       					children=[
		       						html.Div(className="multi-button",
		       							children=[
		       								html.Button("участник",id='Participant',className="button", n_clicks=0),
		       								html.Button("победитель",id='win',className="button",n_clicks=0),
		       								html.Button("история",id='hist',className="button",n_clicks=0)
		       							]),
		       					])
       					]),
       			]),
       	html.Div(id='Image_area', className="Image"),
       	html.Div(className="rectangle-111"),
        html.Div(className="rectangle-112"),
        html.Img(className="track-2", src="https://anima-uploads.s3.amazonaws.com/projects/5fdd53490136fca9d0284658/releases/5fddd6dfc90a83f6a684ae47/img/track-2@2x.svg"),
        ])

@app.callback(Output('Image_area', 'children'),
	[Input('Participant', 'n_clicks')])
def update_are(bt1):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'Participant' in changed_id:
		ret = html.Div(
			dt.DataTable(
                id="table-line",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                style_header={
                    "textDecoration": "underline",
                    "textDecorationStyle": "dotted",
                },
                tooltip_delay=0,
                tooltip_duration=None,
                row_deletable=True,
                column_selectable=True,
                style_table={"overflowY": "scroll"},
                fixed_rows={"headers": False, "data": 0},
                style_cell={"width": "85px"},
            ),className="frame-84 rectangle-121")
	else:
		ret = html.Div(
        	children=[
        		html.Div(className="rectangle-120"),
        		html.H1("Здравствуйте!",className="zdravstvuite-11135 montserrat-bolditalic-bold-white-48px border-class-1"),
        		html.Div("Мы привествуем Вас на нашем портале “Остлеживание государственных закупок”. Для начала работы  нажмитекнопку “Выберите регион”",className="my-privest-gion-11134 montserrat-bold-white-18px border-class-1"),
        		html.Div(className="clip-programming")
        	])
	return ret


if __name__ == '__main__':
    app.run_server(debug=False)