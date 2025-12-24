import sys, os, random, tempfile, pandas as pd, multiprocessing
from timeit import timeit

QUARTILES = 4
TEMPLATE_STRING = """\
language Essence 1. 3
$ total time: {{time}}

letting s be 0
find x : set (minSize 1) of int({values})

such that s = sum([i | i <- x])
"""


def generate_list():
    nums = set()
    for _ in range(100):
        candidate = random.randint(-1000, 1000)
        if (-candidate) not in nums and candidate != 0:
            nums.add(candidate)

    return sorted(list(nums))


def generate_essence():
    values = generate_list()
    domain_str = ", ".join(map(str, values))
    essence_instance = TEMPLATE_STRING.format(values=domain_str)
    return essence_instance


def run_instance(essence: str):
    prev_dir = os.getcwd()
    os.chdir(tempfile.mkdtemp())

    with open("instance.essence", "w") as f:
        f.write(essence)

    cmd = lambda: os.system("conjure solve instance.essence")
    dur = timeit(cmd, number=1)

    solved = os.path.exists("instance.solution")
    essence = essence.format(time=dur)

    os.system("conjure solve instance.essence")
    os.chdir(prev_dir)

    return essence, solved, dur


# def generate_and_time(essence):
#     essence = generate_essence()
#     dur, solved = run_instance(essence)
#     essence = essence.format(time=dur)
#     return essence, dur, solved


# Generate and organise into 4 folders by quartiles of time taken
def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)

    instances = [generate_essence() for _ in range(1000)]
    with multiprocessing.Pool(80) as p:
        results = p.map(run_instance, instances)

    df = pd.DataFrame(results, columns=["essence", "solved", "time"])

    # Add unsolved instances to a separate folder
    unsolved_dir = os.path.join(outdir, "unsolved")
    os.makedirs(unsolved_dir, exist_ok=True)
    unsolved = df[~df["solved"]]
    for idx, row in unsolved.iterrows():
        with open(os.path.join(unsolved_dir, f"inst-{idx}.essence"), "w") as f:
            f.write(row["essence"])

    df = df[df["solved"]]

    quartiles = pd.qcut(df["time"], QUARTILES, labels=False)
    for quartile in range(QUARTILES):
        quartile_dir = os.path.join(outdir, f"quartile-{quartile + 1}")
        os.makedirs(quartile_dir, exist_ok=True)
        subset = df[quartiles == quartile]
        for idx, row in subset.iterrows():
            with open(os.path.join(quartile_dir, f"inst-{idx}.essence"), "w") as f:
                f.write(row["essence"])


if __name__ == "__main__":
    main()
