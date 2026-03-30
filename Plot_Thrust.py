import pandas as pd
import matplotlib.pyplot as plt
import sys

CALIBRATION_OFFSET = 0.2545  # kg (오토 캘리브레이션 값)
IGNITION_TIME_SEC  = 0.0     # 기록 시작 = 점화 직후

def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    # timestamp가 ms 단위인 경우 초로 변환
    if df["timestamp_ms"].max() > 1000:
        df["time_sec"] = df["timestamp_ms"] / 1000.0
    else:
        df["time_sec"] = df["timestamp_ms"]
    df["force_corrected"] = df["force_kg"] + CALIBRATION_OFFSET
    return df

def print_summary(df: pd.DataFrame):
    active = df[df["force_corrected"] >= 0.01]
    peak   = df["force_corrected"].max()
    t_peak = df.loc[df["force_corrected"].idxmax(), "time_sec"]
    total_impulse = (
        df["force_corrected"].clip(lower=0)
        * df["time_sec"].diff().fillna(0)
    ).sum()

    print("=" * 40)
    print("  Thrust Test Summary")
    print("=" * 40)
    print(f"  Peak thrust     : {peak:.3f} kg  ({peak * 9.81:.1f} N)")
    print(f"  Time to peak    : {t_peak:.3f} sec")
    print(f"  Total samples   : {len(df)}")
    print(f"  Recording time  : {df['time_sec'].max():.2f} sec")
    print(f"  Total impulse   : {total_impulse:.2f} kg·s  ({total_impulse * 9.81:.1f} N·s)")
    print("=" * 40)

def plot(df: pd.DataFrame, output: str = None):
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(df["time_sec"], df["force_corrected"], color="#00c9a7", linewidth=1.8, label="Corrected Thrust (kg)")
    ax.axhline(0, color="gray", linewidth=0.7, linestyle="--")
    ax.fill_between(df["time_sec"], df["force_corrected"].clip(lower=0), alpha=0.15, color="#00c9a7")

    peak = df["force_corrected"].max()
    t_peak = df.loc[df["force_corrected"].idxmax(), "time_sec"]
    ax.annotate(
        f"Peak: {peak:.2f} kg @ {t_peak:.2f}s",
        xy=(t_peak, peak),
        xytext=(t_peak + 0.5, peak - 2),
        arrowprops=dict(arrowstyle="->", color="white"),
        color="white", fontsize=9,
    )

    ax.set_xlabel("Time after ignition (sec)", color="white")
    ax.set_ylabel("Thrust (kg)", color="white")
    ax.set_title("Rocket Engine Thrust Profile", color="white", fontsize=13)
    ax.tick_params(colors="white")
    ax.spines[:].set_color("#444")
    ax.set_facecolor("#0d1117")
    fig.patch.set_facecolor("#0d1117")
    ax.legend(facecolor="#1a1a2e", labelcolor="white")
    ax.grid(True, color="#333", linestyle="--", linewidth=0.5)

    plt.tight_layout()
    if output:
        plt.savefig(output, dpi=150, bbox_inches="tight")
        print(f"  Graph saved → {output}")
    else:
        plt.show()

if __name__ == "__main__":
    filepath = sys.argv[1] if len(sys.argv) > 1 else "data/example_thrust_data.csv"
    output   = sys.argv[2] if len(sys.argv) > 2 else None

    df = load_data(filepath)
    print_summary(df)
    plot(df, output)