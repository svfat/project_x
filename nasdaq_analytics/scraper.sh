#!/usr/bin/env bash
script_dir=$(dirname "$0")

python "$script_dir/historical_prices.py"
python "$script_dir/insider_trades.py"
