import pandas as pd


def generate_table(filter_df):
    final_df = []
    for id in filter_df.columns:
        df = filter_df[id].reset_index().rename(
            columns={'index': 'seen', id: 'new_value'})
        df = df.assign(jittaStockId=id)
        final_df.append(df)
    last = pd.concat(final_df)
    print(last.shape)

    return last


def export_sandbox(dataVersion, last, table, cnx):
    # Insert the data into the table
    df2 = last.copy()
    df2[table] = df2["new_value"].round(5)
    df2["value"] = df2[table]
    df2.drop(columns="new_value", inplace=True)
    df2 = df2.reset_index()
    df2.to_sql(f"{dataVersion}_{table}", cnx, if_exists="replace", index=False)