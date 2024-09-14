# %%
def get_api_key(project_id):
    """ Returns the RedCap token for a given project ID
    Keyword arguments:
    project_id -- 
    Set the creds file to the credentials file containing all of the RedCap Project urls and tokens
    """
    import pandas as pd
    creds = pd.read_csv("C:/Users/rodrica2/OneDrive - The University of Colorado Denver/Documents/redcap_credentials/credentials")
    api_key = creds[creds['project_id'] == project_id]["token"].iloc[0]
    return(api_key)


# %%
# Generate a horizontal table
# pd.crosstab(
#     df.question, 
#     columns = [df.timepoint, df.response]).apply(
#         lambda row: round((row/row.sum())*100, 2).astype(str) +'%', 
#         axis = 1)

# q1 = df[df['question'] == 'q1']

# pd.crosstab(
#     q1.response,
#     columns = [df.timepoint])

# (pd.crosstab(
#     q1.response,
#     q1.timepoint,
#     normalize = 'index'
#     ) * 100).round(2).astype(str) + "%"