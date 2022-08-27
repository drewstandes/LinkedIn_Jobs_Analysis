import pandas as pd 
# import Scraping_LinkedIn_Jobs

# Get jobs data if necessary
# Scraping_LinkedIn_Jobs.scrape_and_generate_csv()

def clean_csv_to_new():
    jobs_df = pd.read_csv('LinkedIn_DataScience_Germany_raw.csv')

    jobs_df.drop('Unnamed: 0', inplace=True, axis=1)
    jobs_df['Company Name'] = jobs_df['Company Name'].str.replace('\n', '')
    jobs_df['Company Name'] = jobs_df['Company Name'].str.strip()

    jobs_df.to_csv('LinkedIn_DataScience_Germany.csv')