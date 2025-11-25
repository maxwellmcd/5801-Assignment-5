# 5801-Assignment-5
# RLS Launch Control System
# Group Members: Max McDaniel, Sid McDaniel, Jason Sourivong, and Ayub Mohamoud

A simplified **Rocket Launch System (RLS)** simulation with two major components:

- **Pad Unit** — performs battery/circuit testing and enables launch hardware.
- **Control Unit** — verifies pad readiness and initiates launch.

This repository contains a single file:
rls.py

which includes:
- Full system logic  
- Built-in automated tests  
- Command-line interface (CLI)

---

## Requirements
- **Python 3.8+**
- Uses only the Python standard library

Check your Python version:

python3 --version

---

## Installation & Setup
Clone or download the repository:

git clone <(https://github.com/maxwellmcd/5801-Assignment-5)>
Or simply place rls.py anywhere you like.

---

### Running the Launch System (CLI)
The program supports direct command-line operation using the following structure:

python3 rls.py --unit <pad|control> --action <test|enable|ready|launch> [options]

---

### PAD COMMANDS
Run a pad test


python3 rls.py --unit pad --action test --battery 100 --circuit CLOSED
Enable the pad (requires successful test)

python3 rls.py --unit pad --action enable

---

## CONTROL COMMANDS
Mark control unit as ready
(only if pad is already enabled)


python3 rls.py --unit control --action ready
Launch
(only if pad enabled and control ready)


python3 rls.py --unit control --action launch

---

## Running the Automated Test Suite
Run all built-in system tests with:
python3 rls.py --run-tests

You will be prompted:
Enter your first name (tester):

A fully formatted PASS/FAIL test report will print, including:
- Test ID
- Description
- Expected output
- Actual output
- PASS/FAIL result
- Timestamp

---

### System Overview
**Pad State**
- Battery %
- Circuit status (OPEN/CLOSED)
- Green light
- Red light
- Enabled flag

**Control State**
- Red light
- Green light
- Ready flag

---

## Core Functions
Component	Function	Purpose
Pad	pad_test()	Runs diagnostic test (battery + circuit)
Pad	pad_enable()	Enables pad if green light is on
Control	control_ready()	Marks control ready if pad enabled
Control	control_launch()	Launches if pad & control ready

---

Example Full Launch Sequence
python3 rls.py --unit pad --action test --battery 100 --circuit CLOSED
python3 rls.py --unit pad --action enable
python3 rls.py --unit control --action ready
python3 rls.py --unit control --action launch

If successful, output will include:
YYYY-MM-DD HH:MM:SS - LAUNCH_STARTED
YYYY-MM-DD HH:MM:SS - LAUNCH_SUCCESS
Control Launch: LAUNCH_SUCCESS, Green Light: True

---

## Resetting Runtime State
State resets automatically during tests.

To reset manually:
from rls import reset_states
reset_states()

---

File Structure
rls.py
└── Contains:
    • Pad logic
    • Control logic
    • Global state
    • Test suite
    • CLI interface
