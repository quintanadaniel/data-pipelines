import pandas as pd
import os


def extract(filename: str, file_csv):
    df_parquet = pd.read_parquet(f"imput_files/{filename}")
    df_grocery_sales = pd.read_csv(f"imput_files/{file_csv}")
    
    merged_df = pd.merge(df_grocery_sales, df_parquet, on="index", how="inner")
    
    return merged_df

def transform(df_merged):
    df_merged.fillna(
      {
          'CPI': df_merged['CPI'].mean(),
          'Weekly_Sales': df_merged['Weekly_Sales'].mean(),
          'Unemployment': df_merged['Unemployment'].mean(),
      }, inplace = True
    )
    df_merged["Date"] = pd.to_datetime(df_merged["Date"], format = "ISO8601")
    df_merged["Month"] = df_merged['Date'].dt.month
    clean_data = df_merged.loc[df_merged["Weekly_Sales"] > 10000, :]
    clean_data = clean_data.drop(["index", "Temperature", "Fuel_Price", "MarkDown1", "MarkDown2", "MarkDown3", "MarkDown4", "MarkDown5", "Type", "Size", "Date"], axis = 1)
    
    return clean_data

def avg_monthly_sales(cleaned_data):
    monthly_sales = cleaned_data[["Month", "Weekly_Sales"]]
    agg_data = monthly_sales.groupby("Month").agg(Avg_Sales=("Weekly_Sales","mean")).reset_index().round(2)
    return agg_data

def load(clean_data, clean_data_file_path, agg_data, agg_data_file_path):
    clean_data.to_csv(f"output_files/{clean_data_file_path}", index=False)
    agg_data.to_csv(f"output_files/{agg_data_file_path}", index=False)

def validation(file_path):
    # Here we use the absolute path, in jupyter note don-t exist __file__ variable, el se we use os.getcwd() to get the actual directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_in_path = os.path.join(current_dir,"output_files", file_path)
    file_exists = os.path.exists(file_in_path)
    
    if not file_exists:
        raise Exception(f"File not exists in the path {file_path}.")

if __name__ == "__main__":
    merged_df = extract("extra_data.parquet", "grocery_sales.csv")
    clean_data = transform(merged_df)
    agg_data = avg_monthly_sales(clean_data)
    load(clean_data, "clean_data.csv", agg_data, "agg_data.csv")
    validation("clean_data.csv")
    validation("agg_data.csv")
