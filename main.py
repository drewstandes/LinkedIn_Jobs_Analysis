import processing 
# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import utils

skills_list = utils.get_list_from_file('resources/skills_list.txt')
keywords_and_phrases_list = utils.get_list_from_file('resources/keywords_list.txt')

skills_dataframes_list = []
phrases_dataframes_list = []
totals_df = pd.DataFrame(columns=['Country', 'Total Jobs', 'Data Science Jobs Total', 'Machine Learning Jobs Total'])

for country in ['Germany', 'Japan', 'Singapore', 'China', 'United-Kingdom']:
    skills_df, phrases_df, total_jobs, data_science_jobs_count, ml_jobs_count = processing.get_dataframes(country)
    skills_dataframes_list.append(skills_df)
    phrases_dataframes_list.append(phrases_df)
    totals_dict = {'Country': country,'Total Jobs': total_jobs, 'Data Science Jobs Total': data_science_jobs_count, 'Machine Learning Jobs Total': ml_jobs_count}
    totals_df = totals_df.append(totals_dict, ignore_index=True)

skills_df = pd.concat(skills_dataframes_list)
phrases_df = pd.concat(phrases_dataframes_list)

print(skills_df)
print(phrases_df)

# Create a dash application
app = dash.Dash(__name__)
                               
app.layout = html.Div(id='big-app-container',
                        children=[ # build_banner(),
                                html.H1('LinkedIn Data Science Job Insights Dashboard', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 40}),
                                html.Div([html.P("The data in this dashboard has been scraped from a linked in jobs " + 
                                                " search for 'Data Scientist Junior' with experience level = Entry Level. Filtering with " +  
                                                "'Select a Job Title' searches the recorded titles for any occurence of the filter word in the job title. ")]),
                                html.Div(["Select a Job Title: ", dcc.Dropdown(id='job-title',
                                                options=[
                                                    {'label': 'Data Science', 'value': 'DATA SCIENCE'},
                                                    {'label': 'Machine Learning', 'value': 'MACHINE LEARNING'},
                                                ],
                                                value='DATA SCIENCE',
                                                placeholder="place holder here"
                                                ),], 
                                style={'font-size': 20}),  
                                html.Div(["Select a Country: ", dcc.Dropdown(id='country',
                                                options=[
                                                    {'label': 'Germany', 'value': 'Germany'},
                                                    {'label': 'Japan', 'value': 'Japan'},
                                                    {'label': 'Singapore', 'value': 'Singapore'},
                                                    {'label': 'United Kingdom', 'value': 'United-Kingdom'},
                                                    {'label': 'China', 'value': 'China'},
                                                ],
                                                value='Germany',
                                                placeholder="place holder here"
                                                ),], 
                                style={'font-size': 20}),                               
                                html.Br(),
                                html.Br(),
                                html.Div(html.P(id='total-jobs')),
                                html.Div(html.P(id='total-data-science')),
                                html.Div(html.P(id='total-ml')),
                                html.Div(children=
                                            [dcc.Graph(id='pie-graph', style={'display':'inline-block'}),
                                             dcc.Graph(id='bar-graph', style={'display':'inline-block'})]),
                                ])

# bar graph callback
@app.callback( [Output(component_id='bar-graph', component_property='figure'),
                Output(component_id='total-jobs', component_property='children'), 
                Output(component_id='total-data-science', component_property='children'),
                Output(component_id='total-ml', component_property='children')],[
                Input(component_id='job-title', component_property='value'),
               Input(component_id='country', component_property='value')])

def get_bar_graph(job_title, country):
    df = phrases_df[phrases_df['COUNTRY'] == country].drop('COUNTRY', axis=1)
    fig = px.bar(df.loc[job_title,:], labels={'index':'Skills', 'value':'Percentage'})
    temp_df = totals_df.set_index('Country')
   
    total_jobs = temp_df.loc[country, 'Total Jobs']
    data_science_jobs_count = temp_df.loc[country, 'Data Science Jobs Total']
    ml_jobs_count = temp_df.loc[country, 'Machine Learning Jobs Total']

    total_jobs_str = "Total jobs scraped: " + str(total_jobs)
    total_data_sci_str = "Total jobs with Data Science or Data Scientist in the title: " + str(data_science_jobs_count)
    total_ml_str = "Total jobs with Machine Learning and not Data Scientist or Data Science in the title : " + str(ml_jobs_count)

    return [fig, total_jobs_str, total_data_sci_str, total_ml_str]


# pie graph callback
@app.callback( Output(component_id='pie-graph', component_property='figure'),[
                Input(component_id='job-title', component_property='value'),
               Input(component_id='country', component_property='value')])

def get_pie_graph(job_title, country):
    df = skills_df[skills_df['COUNTRY'] == country].drop('COUNTRY', axis=1)
    df = df.transpose().reset_index().rename(columns={'index':'Technology', job_title: 'PERCENTAGE'})
    print(df)
    fig = px.pie(df, values='PERCENTAGE',names='Technology')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()