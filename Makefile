# Makefile for POSCO Steel Decarbonization Optimization Model

.PHONY: all test clean setup single help

# Default target
all: outputs/series_all_scenarios.csv outputs/figs/scope1_by_scenario.png

help:
	@echo "Available targets:"
	@echo "  make all      - Run all scenarios and generate plots"
	@echo "  make test     - Run all unit tests"
	@echo "  make single   - Run single scenario (NetZero2050)"
	@echo "  make clean    - Clean outputs"

setup:
	@echo "Creating conda environment..."
	conda env create -f environment.yml -y

test:
	@echo "Running unit tests..."
	python -m pytest tests/ -v

single: outputs/summary_NGFS_NetZero2050.json

outputs/summary_NGFS_NetZero2050.json: data/posco_parameters_consolidated.xlsx src/*.py
	@echo "Running NGFS NetZero2050 scenario..."
	@mkdir -p outputs
	python -m src.run \
		--params data/posco_parameters_consolidated.xlsx \
		--carbon_scenario NGFS_NetZero2050 \
		--discount 0.05 --util 0.90 --solver glpk --solve --outdir outputs

outputs/series_NGFS_Below2C.csv: data/posco_parameters_consolidated.xlsx src/*.py
	@echo "Running NGFS Below2C scenario..."
	@mkdir -p outputs
	python -m src.run \
		--params data/posco_parameters_consolidated.xlsx \
		--carbon_scenario NGFS_Below2C \
		--discount 0.05 --util 0.90 --solver glpk --solve --outdir outputs

outputs/series_NGFS_NDCs.csv: data/posco_parameters_consolidated.xlsx src/*.py
	@echo "Running NGFS NDCs scenario..."
	@mkdir -p outputs
	python -m src.run \
		--params data/posco_parameters_consolidated.xlsx \
		--carbon_scenario NGFS_NDCs \
		--discount 0.05 --util 0.90 --solver glpk --solve --outdir outputs

outputs/series_all_scenarios.csv: outputs/summary_NGFS_NetZero2050.json outputs/series_NGFS_Below2C.csv outputs/series_NGFS_NDCs.csv
	@echo "Aggregating scenarios..."
	python -c "import pandas as pd; df1=pd.read_csv('outputs/series_NGFS_NetZero2050.csv'); df1['scenario']='NGFS_NetZero2050'; df2=pd.read_csv('outputs/series_NGFS_Below2C.csv'); df2['scenario']='NGFS_Below2C'; df3=pd.read_csv('outputs/series_NGFS_NDCs.csv'); df3['scenario']='NGFS_NDCs'; pd.concat([df1,df2,df3]).to_csv('outputs/series_all_scenarios.csv',index=False)"

outputs/figs/scope1_by_scenario.png: outputs/series_all_scenarios.csv
	@echo "Generating visualizations..."
	@mkdir -p outputs/figs
	python -c "from src.viz import *; plot_scope1_by_scenario('outputs/series_all_scenarios.csv','outputs/figs/scope1_by_scenario.png'); plot_ets_cost_by_scenario('outputs/series_all_scenarios.csv','outputs/figs/ets_cost_by_scenario.png')"

clean:
	@echo "Cleaning outputs..."
	rm -rf outputs/ __pycache__/ src/__pycache__/ tests/__pycache__/ .pytest_cache/
	status:
	@echo "POSCO Model Status:"
	@ls -la data/ outputs/ 2>/dev/null || echo "Directories not found"