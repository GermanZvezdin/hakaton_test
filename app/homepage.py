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
import dash_daq as daq
import os 
import base64

app = dash.Dash(__name__,suppress_callback_exceptions=True)

df = pd.read_csv('/home/alex/Downloads/notifications.csv')
print(df.columns)
df = df.dropna()

def dectode_svg(svg_file):
	encoded = base64.b64encode(open(svg_file,'rb').read()) 
	svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode()) 
	return svg

app.layout = html.Div(
    className="frame-84",
    children=[
        html.Div(className="rectangle-108"),
        html.Div(className="rectangle-109"),
        html.H1("Отслеживание государственных закупок",className="otslezhiva-upok-10114 montserrat-bold-white-48px border-class-1"),
       	html.Div(className="releases-110",
       				children=[
       				html.Div(
       					className="Menu-bar",
       					children=[
       						html.Span(
       						className="Input-1",
		       				children=[
		       					dcc.Input(className="basic-slide"),
		       					html.Label("РЕГИОН")
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

"""
dt.DataTable(
                id="table-line",
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                style_header={
                    "textDecoration": "underline",
                    "textDecorationStyle": "dotted",
                })
                row_deletable=True,
                column_selectable=True,
                style_table={"overflowY": "scroll", 'width': 400, 'height': 400},
                fixed_rows={"headers": True, "data": 0},
            )
 """
    #return 'The switch is {}.'.format(on)

@app.callback(Output('Image_area', 'children'),
  [Input('Participant', 'n_clicks')])
def update_are(bt1):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'Participant' in changed_id:
		ret = html.Div(
    			className="frame-82",
    			children=[
    				html.Div(className="rectangle-108"),
        			html.Div(className="rectangle-109"),
    				html.H1("Отслеживание государственных закупок",className="otslezhiva-akupok-721 montserrat-bold-white-48px border-class-1"),
    				html.Div(className="frame-110",
       				children=[
       				html.Div(
       					className="Menu-bar",
       					children=[
       						html.Span(
       						className="Input-1",
		       				children=[
		       					dcc.Input(className="basic-slide"),
		       					html.Label("РЕГИОН")
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
    				html.Div("Выберите интерисующие параметры",className="pobeditel-10247 montserrat-bold-gray-24px border-class-1"),
    				html.Div(className="rectangle-113-C61RwL"),
    				html.Div("ИНН",className="frame-82 param montserrat-bold-gray-24px border-class-1"),
    				daq.BooleanSwitch(id="inn",on=True,color="#1875f0", className="frame-82 switch_param"),
    				html.Div(id='bs1'),
    				html.Div("ФЗ",className="frame-82 param montserrat-bold-gray-24px border-class-1"),
    				daq.BooleanSwitch(id="fz",on=True,color="#1875f0", className="switch_param"),
    				html.Div(id='bs2'),
    				html.Div("EMAIL",className="frame-82 param montserrat-bold-gray-24px border-class-1"),
    				daq.BooleanSwitch(id="email",on=True,color="#1875f0", className="switch_param"),
    				html.Div(id='bs3'),
    				html.Div("Телефон",className="frame-82 param montserrat-bold-gray-24px border-class-1"),
    				daq.BooleanSwitch(id="phone",on=True,color="#1875f0", className="switch_param"),
    				html.Div(id='bs4'),
    				print(df['maxprice'].values),
    				html.Div(className="rectangle-115", children=[
				  			dcc.Graph(id='price', config={'displayModeBar': False},
	                        figure={
		                        'data': [{'y': df['maxprice'].values, 'type': 'bar', 'name': 'prices'}],
		                        'layout': {
		                            'title': 'Гистограмма изменения цен'
                    			}})
                    		]),
    				html.Div(className="rectangle-115-2",
    					children=[
    					html.A(
                            html.Img(
                            	src=dectode_svg("/home/alex/PyProjects/hakaton_test/app/assets/csv_logo.svg"),
                            	style={'height':"80px", "text-align": "center", "width": "auto", "left":"1000px", "top":"30px", "position": "absolute"}
                            ),
                            href=os.path.join('assets', 'style', '.css'),
                            download="style.css",
                        ),
    					])
				])			
	else:
		ret = html.Div(
        	children=[
        		html.Div(className="rectangle-120"),
        		html.H1("Здравствуйте!",className="zdravstvuite-11135 montserrat-bolditalic-bold-white-48px border-class-1"),
        		html.Div("Мы привествуем Вас на нашем портале “Остлеживание государственных закупок”. Для начала работы  впишите регион",className="my-privest-gion-11134 montserrat-bold-white-18px border-class-1"),
        		html.Div(className="clip-programming"),
        		html.Div(className="rectangle-111"),
        		html.Div(className="rectangle-112"),
        		html.Img(className="track-2", src="https://anima-uploads.s3.amazonaws.com/projects/5fdd53490136fca9d0284658/releases/5fddd6dfc90a83f6a684ae47/img/track-2@2x.svg"),
        	])
	return ret

@app.callback(
    dash.dependencies.Output('bs1', 'children'),
    [dash.dependencies.Input('inn', 'on')])
def update_output(on):
  print(on)
  return 'The switch is {}.'.format(on)

if __name__ == '__main__':
    app.run_server(debug=True)