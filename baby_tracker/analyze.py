import io
import pandas as pd
from matplotlib import pyplot as plt
from datetime import timedelta

TIMESTAMP_COLUMNS = ["from_time", "to_time", "created_at", "updated_at"]

def total_duration_per_day(db_conn, table, offset="6Hours"):
    df = df_from_db_table(db_conn, table)
    agg = df.resample('D', on='from_time', offset=offset)[["duration"]].sum()
    return agg

def latest_daily_total_duration(db_conn, table):
    df_agg_tot = total_duration_per_day(db_conn, table)
    last_date = df_agg_tot.index[-1]
    last_duration = timedelta(seconds=df_agg_tot.duration[-1])
    return last_date, last_duration

def avg_duration_per_day(db_conn, table, offset="6Hours"):
    df = df_from_db_table(db_conn, table)
    agg = df.resample('D', on='from_time', offset=offset)[["duration"]].mean()
    return agg


def df_from_db_table(db_conn, table):
    return pd.read_sql_query(f"SELECT * FROM {table};", db_conn, parse_dates=TIMESTAMP_COLUMNS, index_col="id")


def duration_plot(df, title=None, scale=1/60, kind="bar", ylabel="Duration (minutes)"):
    df.duration *= scale
    fig, ax = plt.subplots()
    df.plot(title=title, kind=kind, ax=ax)
    ax.set_ylabel(ylabel)
    ax.set_xticklabels([x.strftime("%m-%d %a") for x in df.index], rotation=90)
    plt.tight_layout()
    return plot_to_buffer(fig)


def plot_to_buffer(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf
