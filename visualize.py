import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import sys

available_mems = [[], []]
virt_reclaimed_mems = [[], []]
user_test_starts = []
loop_starts = []
loop_ends = []
program_starts = []
python_starts = []

data_dir = sys.argv[1]

all_log = open(f"{data_dir}/all-log.txt", "r")
if all_log is None:
    exit(1)

for line in all_log:
    cells = line.split()
    if len(cells) == 5 and cells[2] == "MemAvailable:":
        available_mems[0].append(int(cells[0]))
        available_mems[1].append(int(cells[3]))
    elif len(cells) == 3 and cells[2] == "/host/root/gtest":
        user_test_starts.append(int(cells[0]))
    elif "Entering infinite loop" in line:
        loop_starts.append(int(cells[0]))
    elif "Finished infinite loop" in line:
        loop_ends.append(int(cells[0]))
    elif "Freed a merge reclaimed page" in line:
        virt_reclaimed_mems[0].append(int(cells[0]))
        virt_reclaimed_mems[1].append(int(cells[9]))
    elif (
        'Type "help", "copyright", "credits" or "license" for more information.' in line
    ):
        python_starts.append(int(cells[0]))
    elif "Starting a program" in line:
        program_starts.append(int(cells[0]))


plt.figure(figsize=(10, 6))
plt.plot(
    available_mems[0],
    available_mems[1],
    # marker="x",
    # markersize=5,
    linestyle="-",
    color="b",
    label="Available Memory",
)
# plt.plot(
#    virt_reclaimed_mems[0],
#    [y + 1456000 for y in virt_reclaimed_mems[1]],
#    # marker="x",
#    # markersize=5,
#    linestyle="-",
#    color="r",
#    label="Expected Available Memory",
# )
for user_test_start in user_test_starts:
    plt.axvline(
        x=user_test_start,
        color="lightskyblue",
        linestyle="--",
        linewidth=1,
        label="Test User Program Start",
    )
for loop_start in loop_starts:
    plt.axvline(
        x=loop_start,
        color="teal",
        linestyle="--",
        linewidth=1,
        label="Inifinite Loop Start",
    )
for loop_end in loop_ends:
    plt.axvline(
        x=loop_end,
        color="teal",
        linestyle="--",
        linewidth=1,
        label="Inifinite Loop End",
    )
for program_start in program_starts:
    plt.axvline(
        x=program_start,
        color="green",
        linestyle="--",
        linewidth=1,
        label="Program Start",
    )
for python_start in python_starts:
    plt.axvline(
        x=python_start,
        color="green",
        linestyle="--",
        linewidth=1,
        label="Python Start",
    )

plt.gca().yaxis.set_major_formatter(FuncFormatter(lambda y, pos: f"{int(y):,}"))
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{int(x/1000000):,}"))

plt.title("Merging 32MB of memory between 2 VMs")
plt.xlabel("Timestamp (s)")
plt.ylabel("Available Memory (kB)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45, ha="right")

plt.tight_layout()
plt.savefig(f"{data_dir}/mem-available.png")
