import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go
from plotly.tools import make_subplots
import pandas as pd
import datetime

app = dash.Dash()

# Reading  the csv file with purchase data from 2018 and 2019
purchase_df = pd.read_csv('Purchase_Orders_2018_2019.csv', parse_dates=['Order Date', 'Order Date (month,day)', 'Delivery Date', 'Receipt Date', 'Completed Date'])

# Separating the data for the two years to be able to compare them easily
purchase_df_2018 = purchase_df[purchase_df['Order Date (year)']==2018].copy()
purchase_df_2018.reset_index(drop=True,inplace=True)
purchase_df_2019 = purchase_df[purchase_df['Order Date (year)']==2019].copy()
purchase_df_2019.reset_index(drop=True,inplace=True)

# Adding a new column to both dataframes, where the cumulative spending total (GDP) is calculated for each supplier
def cumulative_list(df, cat_column, value_column):
	column_copy_list = list(df[cat_column].copy())
	for unique_item in df[cat_column].unique():
		subtotal_list = []
		for i,item in enumerate(df[cat_column]):
			if item == unique_item:
				subtotal_list.append(df.loc[i,value_column])
				column_copy_list[i] = sum(subtotal_list)
	return column_copy_list

purchase_df_2018.loc[:,'Cumulative Total Suppliers'] = cumulative_list(purchase_df_2018, 'Supplier Code', 'SubTotal (GBP)')
purchase_df_2019.loc[:,'Cumulative Total Suppliers'] = cumulative_list(purchase_df_2019, 'Supplier Code', 'SubTotal (GBP)')

# Creating the list for the dropdown menu
supplier_dropdown_dictlist = []
for item in purchase_df['Supplier Code'].unique():
	mydict = {}
	mydict['label'] = item
	mydict['value'] = item
	supplier_dropdown_dictlist.append(mydict)

# Adding another column to both dataframes where the cumulative spending total (GBP) is calculated for the year
purchase_df_2018.loc[:,'Cumulative Total (GBP)'] = [sum(list(purchase_df_2018['SubTotal (GBP)'])[0:i+1]) for i in range(len(purchase_df_2018['SubTotal (GBP)']))]
purchase_df_2019.loc[:,'Cumulative Total (GBP)'] = [sum(list(purchase_df_2019['SubTotal (GBP)'])[0:i+1]) for i in range(len(purchase_df_2019['SubTotal (GBP)']))]

# Creating new dataframes with the complete purchase orders only
purchase_df_2018_with_lateearly = purchase_df_2018[purchase_df_2018['Order Status'] == 'Complete'].copy()
purchase_df_2019_with_lateearly = purchase_df_2019[purchase_df_2019['Order Status'] == 'Complete'].copy()

# Adding new column to both where early/late deliveries are noted by the number of days they differed from the promised date by the supplier
purchase_df_2018_with_lateearly.loc[:,'Early/Late'] = (pd.to_datetime(purchase_df_2018_with_lateearly['Receipt Date']) - pd.to_datetime(purchase_df_2018_with_lateearly['Delivery Date'])).dt.days
purchase_df_2019_with_lateearly.loc[:,'Early/Late'] = (pd.to_datetime(purchase_df_2019_with_lateearly['Receipt Date']) - pd.to_datetime(purchase_df_2019_with_lateearly['Delivery Date'])).dt.days

# Creating the lists for the dropdown menus on the second tab for supplier delivery performance
supplier_dropdown_dictlist_2018_complete = []
for item in purchase_df_2018_with_lateearly['Supplier Code'].unique():
	mydict = {}
	mydict['label'] = item
	mydict['value'] = item
	supplier_dropdown_dictlist_2018_complete.append(mydict)

supplier_dropdown_dictlist_2019_complete = []
for item in purchase_df_2019_with_lateearly['Supplier Code'].unique():
	mydict = {}
	mydict['label'] = item
	mydict['value'] = item
	supplier_dropdown_dictlist_2019_complete.append(mydict)

# Creating the traces for the second (not interactive) chart with cumulative totals for each year
total_traces = []
total_traces.append(go.Scatter(
				x=purchase_df_2018['Order Date (month,day)'],
				y=purchase_df_2018['Cumulative Total (GBP)'],
				mode='lines',
				fill='tozeroy',
				#text='Total spent: {}'.format(year_dfs[0][year_dfs[0]['Supplier Code']==supplier_picker]['Cumulative Total Suppliers']),
				name='Total spend in GBP (2018)'
				))
total_traces.append(go.Scatter(
				x=purchase_df_2019['Order Date (month,day)'],
				y=purchase_df_2019['Cumulative Total (GBP)'],
				mode='lines',
				fill='tozeroy',
				#text='Total spent: {}'.format(year_dfs[1][year_dfs[1]['Supplier Code']==supplier_picker]['Cumulative Total Suppliers']),
				name='Total spend in GBP (2019)'
				))

# Creating the labels, values, and text for each year's pie chart
def pie_charter(df, cat_column, value_column):
	pie_labels = df[cat_column].unique()
	pie_values = [df[df[cat_column]==cat].iloc[-1][value_column] for cat in df[cat_column].unique()]
	pie_text = [None if (x/sum(pie_values))*100 < 2.5 else str(round(x/sum(pie_values)*100,2))+'%' for x in pie_values]
	return pie_labels, pie_values, pie_text

pie_labels_2018, pie_values_2018, text_2018 = pie_charter(purchase_df_2018, 'Supplier Code', 'Cumulative Total Suppliers')
pie_labels_2019, pie_values_2019, text_2019 = pie_charter(purchase_df_2019, 'Supplier Code', 'Cumulative Total Suppliers')

# Creating the traces for the pie charts
pie_fig = make_subplots(rows=1, cols=2)
pie_fig.add_trace(go.Pie(labels=pie_labels_2018, values=pie_values_2018, hole=.4, text=text_2018, textinfo='text', hoverinfo='label+percent+value', domain=dict(x=[0,0.5])))
pie_fig.add_trace(go.Pie(labels=pie_labels_2019, values=pie_values_2019, hole=.4, text=text_2019, textinfo='text', hoverinfo='label+percent+value', domain=dict(x=[0.5,1.0])))

# Creating the app layout with both tabs
app.layout = html.Div([
				dcc.Tabs(id='tabs', children=[
					dcc.Tab(label='Supplier Spend', children=[
						html.Div([
							html.H1('Supplier Spend- 2018/2019')],style={'horizontal-align' : 'center', 'text-align' : 'center'}),
						html.Div([
							html.H3('Enter supplier code:'),
							dcc.Dropdown(id='my_supplier_picker',
									options=supplier_dropdown_dictlist,
									value='Company40',
									multi=False
							)]),
						dcc.Graph(id='my_supplier_graph'),
						html.Div([
							html.H1('Total Spend - 2018/2019')],style={'horizontal-align' : 'center', 'text-align' : 'center'}),
						dcc.Graph(id='my_total_graph',
							figure={'data':total_traces,
									'layout':go.Layout(title='Cumulative Spend Total with all Suppliers (GBP)',
														xaxis={'title':'Order Date','tickformat': '%B'},
														yaxis={'title':'Cumulative Total'},
														hovermode='closest')},
							),
						html.Div([
							html.H1('Total Spend by Supplier - 2018/2019')],style={'horizontal-align' : 'center', 'text-align' : 'center'}),
						html.Div([
							html.H2('2018')],
							style={'display' : 'inline-block', 'width' : '50%', 'text-align' : 'center'}),
						html.Div([
							html.H2('2019')],
							style={'display' : 'inline-block', 'width' : '30%', 'text-align' : 'center'}),
						dcc.Graph(id='my_pie_graphs',
							figure={'data':pie_fig,
									'layout':go.Layout(hovermode='closest')}			
							)
						]),
					dcc.Tab(label='Supplier Deliveries', children=[
						html.Div([
							html.H1('Supplier Deliveries - 2018/2019')],style={'horizontal-align' : 'center', 'text-align' : 'center'}),
						html.Div([
							html.H2('2019')],style={'horizontal-align' : 'center', 'text-align' : 'center'}),
						html.Div([
							html.H3('Enter supplier code:'),
							dcc.Dropdown(id='my_supplier_picker_deliveries_2019',
									options=supplier_dropdown_dictlist_2019_complete,
									value='Company40',
									multi=False
							)]),
						dcc.Graph(id='my_supplier_delivery_graph_2019'),
						html.Div([
							html.H2('2018')],style={'horizontal-align' : 'center', 'text-align' : 'center'}),
						html.Div([
							html.H3('Enter supplier code:'),
							dcc.Dropdown(id='my_supplier_picker_deliveries_2018',
									options=supplier_dropdown_dictlist_2018_complete,
									value='Company40',
									multi=False
							)]),
						dcc.Graph(id='my_supplier_delivery_graph_2018')
						]),
					],style={'fontFamily':'Verdana','textAlign': 'center', 'color': '#1E90FF', 'font-weight': 'bold'})
				],style={'fontFamily':'Verdana'})

# Adding the callbacks to make the dropdowns work on the first tab
# Error handling factored in for missing values (no spending with a supplier in one of the years)
@app.callback(Output('my_supplier_graph','figure'),
			[Input('my_supplier_picker','value')])
def update_graph(supplier_picker):	
	traces = []
	try:
		traces.append(go.Scatter(
						x=purchase_df_2018[purchase_df_2018['Supplier Code']==supplier_picker]['Order Date (month,day)'],
						y=purchase_df_2018[purchase_df_2018['Supplier Code']==supplier_picker]['Cumulative Total Suppliers'],
						mode='lines',
						fill='tozeroy',
						name='Total spend in {} (2018): {}'.format(purchase_df_2018[purchase_df_2018['Supplier Code']==supplier_picker].iloc[0]['Currency'],supplier_picker)
						))
	except IndexError:
		traces.append(go.Scatter(
						x=purchase_df_2018[purchase_df_2018['Supplier Code']==supplier_picker]['Order Date (month,day)'],
						y=purchase_df_2018[purchase_df_2018['Supplier Code']==supplier_picker]['Cumulative Total Suppliers'],
						mode='lines',
						fill='tozeroy',
						name='Total spend (2018): {}'.format(supplier_picker)
						))
	try:
		traces.append(go.Scatter(
						x=purchase_df_2019[purchase_df_2019['Supplier Code']==supplier_picker]['Order Date (month,day)'],
						y=purchase_df_2019[purchase_df_2019['Supplier Code']==supplier_picker]['Cumulative Total Suppliers'],
						mode='lines',
						fill='tozeroy',
						name='Total spend in {} (2019): {}'.format(purchase_df_2018[purchase_df_2018['Supplier Code']==supplier_picker].iloc[0]['Currency'],supplier_picker)
						))
	except IndexError:
		traces.append(go.Scatter(
						x=purchase_df_2019[purchase_df_2019['Supplier Code']==supplier_picker]['Order Date (month,day)'],
						y=purchase_df_2019[purchase_df_2019['Supplier Code']==supplier_picker]['Cumulative Total Suppliers'],
						mode='lines',
						fill='tozeroy',
						name='Total spend (2019): {}'.format(supplier_picker)
						))
	try:
		fig = {'data':traces,
				'layout':go.Layout(title='Cumulative Spend Total ({}) - {}'.format(purchase_df_2018[purchase_df_2018['Supplier Code']==supplier_picker].iloc[0]['Currency'],supplier_picker),
									xaxis={'title':'Order Date','tickformat': '%B'},
									yaxis={'title':'Cumulative Total'},
									hovermode='closest')}
	except IndexError:
		fig = {'data':traces,
				'layout':go.Layout(title='Cumulative Spend Total ({}) - {}'.format(purchase_df_2019[purchase_df_2019['Supplier Code']==supplier_picker].iloc[0]['Currency'],supplier_picker),
									xaxis={'title':'Order Date','tickformat': '%B'},
									yaxis={'title':'Cumulative Total'},
									hovermode='closest')}
	return fig

# Adding the callbacks to make the dropdowns work on the second tab
@app.callback(Output('my_supplier_delivery_graph_2019','figure'),
			[Input('my_supplier_picker_deliveries_2019','value')])
def update_graph(supplier_picker):	
	data = [go.Scatter(x=purchase_df_2019_with_lateearly[purchase_df_2019_with_lateearly['Supplier Code']==supplier_picker]['Order Date (month,day)'],
				y=purchase_df_2019_with_lateearly[purchase_df_2019_with_lateearly['Supplier Code']==supplier_picker]['Early/Late'],
				mode='lines',
				line=dict(color='firebrick', width=4),
				name=supplier_picker
				)]
	fig = {'data':data,
			'layout':go.Layout(title='Early/Late Deliveries (2019): {}'.format(supplier_picker),
								xaxis={'title':'Order Date','tickformat': '%B'},
								yaxis={'title':'Early(-)/Late(+) Delivery (Days)'},
								hovermode='closest')}
	return fig

@app.callback(Output('my_supplier_delivery_graph_2018','figure'),
			[Input('my_supplier_picker_deliveries_2018','value')])
def update_graph(supplier_picker):	
	data = [go.Scatter(x=purchase_df_2018_with_lateearly[purchase_df_2018_with_lateearly['Supplier Code']==supplier_picker]['Order Date (month,day)'],
				y=purchase_df_2018_with_lateearly[purchase_df_2018_with_lateearly['Supplier Code']==supplier_picker]['Early/Late'],
				mode='lines',
				line=dict(color='firebrick', width=4),
				name=supplier_picker
				)]
	fig = {'data':data,
			'layout':go.Layout(title='Early/Late Deliveries (2018): {}'.format(supplier_picker),
								xaxis={'title':'Order Date','tickformat': '%B'},
								yaxis={'title':'Early(-)/Late(+) Delivery (Days)'},
								hovermode='closest')}
	return fig

if __name__ == '__main__':
	app.run_server(debug=True)
