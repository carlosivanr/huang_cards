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

# %% freq_prop()
# Define a function that generates frequency and proportions of one column
def freq_prop(df, col_name):
    """ Returns a GT object with the n(%) values sorted descending.
    Keyword arguments:
    df       -- a dataframe
    col_name -- the name of the column in quotes 
    """
    # Get the total sample size from the column
    N = str(df.shape[0])

    return(
        GT(pd.DataFrame(
            (df[col_name].value_counts().astype(str)) +
            ' (' +
            (df[col_name].value_counts(normalize = True).mul(100).round(1).astype(str) + '%)'))
            .reset_index()
            .rename(columns = {0:("N = " + N)}))
            )

# %%
# Define a function to perform independent t-tests from the pre and post dataframes
def test(col_1, col_2, label):
    """ Returns a table with the n, mean, std, of two variables and an 
    independent samples t-test
    
    Keyword arguments:
    col_1   -- pandas series of values in sample of group 1
    col_2   -- pandas series of values in sample of group 2
    label   -- character string of  the label to display in 
               the table
    """
    # Filter out any non numerical values
    x1 = pre[col_1][pre[col_1] != ''].astype(int).to_numpy()
    x2 = post[col_2][post[col_2] != ''].astype(int).to_numpy()
    
    # Collect results from t-test into a data frame
    result = ttest_ind(
        x2,
        x1,
        alternative="two-sided",
        usevar = "pooled",
        weights = (None, None),
        value = 0
        )

    # Return a data frame assembled from results
    return(
        pd.DataFrame.from_dict(
            {
            "Question":     [label],
            "N Pre":        [np.count_nonzero(x1)],
            "Mean Pre":     [x1.mean().round(2)],
            "Std Pre":      [x1.std().round(2)],
            "N Post":       [np.count_nonzero(x2)], 
            "Mean Post":    [x2.mean().round(2)],
            "Std Post":     [x2.std().round(2)],
            "Tstat":        [result[0].round(2)],
            "Pval":         [result[1].round(2)],
            "df":           [result[2]],
            }
        ).set_index("Question")
    )

# %%
# Define a function that generates frequency and proportions of one column
def pre_post_tab(question):
    """ Returns a pandas crosstab in proportions of the response of a 
    categorical variable by timepoint. 
    
    Requires a prepped data frame called df specifically crafted for the
    Huang, Cards 2024 survey 
    Keyword arguments:
    question -- a character string specifying either 'q1' or 'q2'
    """
    temp = df[df['question'] == question]
    return(
    (pd.crosstab(
        temp.response,
        temp.timepoint,
        normalize = 'index'
        ) * 100).round(2).astype(str) + "%"
    )

# %%
# Define a function to stack data, coalese, and rename for plotting
def plot(col_1, col_2):

    # Stack the two data frames
    df = pd.concat([pre[[col_1, "timepoint"]], 
                    post[[col_2, "timepoint"]]])
    
    # Remove nulls
    df = df[df[col_1] != '']
    df = df[df[col_2] != '']

    # Coalese the dependent variable into one column
    df["value"] = df[col_1].combine_first(df[col_2]).astype(int)

    ax = sns.barplot(df, x = "timepoint", y="value", alpha=.8)
    ax.set(xlabel = "Timepoint", ylabel = "Mean Response")
    ax.set(ylim=(1, 4))
    sns.despine(bottom = False, left = False, top = True, right = True)
    plt.show()

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