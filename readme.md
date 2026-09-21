This project solves the **Distributed Flexible Job Shop Scheduling Problem (D-FJSSP)** using a SAT model. Each job consists of a sequence of operations with precedence constraints. Each operation may be processed on one or more machines with different processing times. The solver supports multiple parallel factories, symmetry breaking, and `E*` transitive constraints.

## 1. System Requirements

- Linux or macOS.
- Python 3.8 or later.
- `pip` and Python's `venv` module.
- Bash for running the `.sh` scripts.

Check the installed versions:

```bash
python3 --version
pip3 --version
```

## 2. Set Up the Environment

Run the following commands from the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The main packages listed in `requirements.txt` are:

- `python-sat`: builds and solves the SAT model.
- `matplotlib`: generates schedules and result visualizations.

Activate the environment again whenever you open a new terminal:

```bash
cd /path/to/DFJSSP_with_DAG
source venv/bin/activate
```

To leave the virtual environment:

```bash
deactivate
```

## 3. Make the Scripts Executable

Run this once if the shell scripts or `runlim` do not have execute permission:

```bash
chmod +x runlim run.sh 2factories.sh 3factories.sh 4factories.sh auto.sh summary.sh visualize.sh
```

Always run commands from the repository root because the scripts use relative paths such as `datasets/...` and `results/...`.

## 4. Run a Single Instance

Basic command:

```bash
python3 -u main.py \
	--input datasets/fmj/mfjs01 \
	--factories 2 \
	--sb \
	--full_transitive
```

Examples using other datasets:

```bash
# Brandimarte
python3 -u main.py --input datasets/brandimarte/MK01 --factories 2 --sb --full_transitive

# RDATA
python3 -u main.py --input datasets/rdata/la01.txt --factories 2 --sb --full_transitive
```

The solver prints the greedy makespan, SAT makespan, running times, and schedule validation status to the terminal. To save the output to a log file:

```bash
mkdir -p results/2factories/fmj
python3 -u main.py \
	--input datasets/fmj/mfjs01 \
	--factories 2 \
	--sb \
	--full_transitive \
	2>&1 | tee results/2factories/fmj/mfjs01.log
```

### `main.py` Arguments

| Argument | Required | Description |
|---|---:|---|
| `--input`, `-i` | Yes | Path to the input dataset. |
| `--factories`, `-num_f` | No | Number of factories. The default is `2`. |
| `--sb` | No | Enables symmetry breaking. |
| `--half_transitive` | No | Enables transitive constraints for only first operation of each job. |
| `--full_transitive` | No | Enables transitive constraints for all operations . |

Do not use `--half_transitive` and `--full_transitive` together. If both are provided, FULL mode takes precedence.

## 5. Run the Benchmarks with Bash

### Run all datasets with 2, 3, and 4 factories

`run.sh` runs the FMJ, Brandimarte, and RDATA instances for all three factory configurations:

```bash
source venv/bin/activate
./run.sh
```

The script uses `runlim` with:

- a time limit of `1800` seconds (`-r 1800`);
- a memory limit of `14000` MB (`-s 14000`).

Logs are saved under:

```text
results/2factories/
results/3factories/
results/4factories/
```

Each directory is divided by dataset type: `fmj`, `brandimarte`, and `rdata`.

### Run only one factory configuration

```bash
./2factories.sh
./3factories.sh
./4factories.sh
```

These scripts run all configured instances with 2, 3, or 4 factories, respectively. The time and memory limits are defined at the beginning of each script.

### Run the complete automated workflow

`auto.sh` runs the following scripts in order:

1. `run.sh` to generate solver logs.
2. `summary.sh` to generate summary CSV files.
3. `visualize.sh` to verify and visualize the results.

Run it with:

```bash
./auto.sh
```

Since `run.sh` may take a long time, the scripts can also be run separately to inspect the output after each stage.

## 6. Generate Result Summaries

After logs have been generated under `results/`, create the CSV summaries:

```bash
./summary.sh
```

The output files are saved as:

```text
summary/2factories.csv
summary/3factories.csv
summary/4factories.csv
```

To process one result directory directly:

```bash
python3 summary.py results/2factories summary/2factories.csv
```

## 7. Verify and Visualize Results

To verify the logs and generate visualizations for all results:

```bash
./visualize.sh
```

Generated images are saved in the corresponding directories under `visualize/`. To process one log file:

```bash
python3 verify_and_visualize.py --input results/2factories/fmj/mfjs01.log
```

To see the available command-line options:

```bash
python3 verify_and_visualize.py --help
python3 summary.py --help
```

## 8. Datasets

The repository contains three dataset groups:

- `datasets/fmj/`: flexible job shop instances from `mfjs01` to `mfjs10` and `sfjs01` to `sfjs10`.
- `datasets/brandimarte/`: instances from `MK01` to `MK15`.
- `datasets/rdata/`: standard instances such as `la01.txt`, `mt06.txt`, `abz5.txt`, `car1.txt`, and `orb1.txt`.

Each dataset directory contains its own README when additional format information is available. The solver currently supports files with a linear operation sequence for each job.

## 9. Result Directory Structure

```text
results/
	2factories/
		fmj/
		brandimarte/
		rdata/
	3factories/
	4factories/

summary/
	2factories.csv
	3factories.csv
	4factories.csv

visualize/
	2factories/
	3factories/
	4factories/
```

## 10. Troubleshooting

### `pysat` package not found

Make sure the virtual environment is active, then reinstall the dependencies:

```bash
source venv/bin/activate
python -m pip install -r requirements.txt
```

### `Permission denied` when running a script or `runlim`

```bash
chmod +x runlim *.sh
```

### Dataset not found

Run the command from the repository root and check the path passed to `--input`:

```bash
pwd
ls datasets/fmj/mfjs01
```

### Stop a batch run

Press `Ctrl+C`. Logs written before the interruption are preserved under `results/`.


