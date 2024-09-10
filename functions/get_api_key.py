# %%
def get_api_key(project_id):
    """Get API Key. Returns the RedCap API Key/Token from a credentials file according to a RedCap Project ID.
    """
    import pandas as pd
    creds = pd.read_csv("C:/Users/rodrica2/OneDrive - The University of Colorado Denver/Documents/redcap_credentials/credentials")
    api_key = creds[creds['project_id'] == project_id]["token"].iloc[0]
    return(api_key)
