import pandas as pd

def preprocess(df, region_df):
    # Keep only Summer Olympics data
    df = df[df['Season'] == 'Summer']
    
    # Merge with region data to get country names
    df = df.merge(region_df, on='NOC', how='left')
    
    # Remove duplicate records
    df.drop_duplicates(inplace=True)
    
    # One-hot encode the 'Medal' column: creates separate columns for Gold, Silver, Bronze
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    
    return df
