# rls.py
from datetime import datetime

# --- Global State ---
pad_state = {
    'battery': 100,
    'circuit': 'CLOSED',
    'green_light': False,
    'red_light': False,
    'enabled': False,
}

control_state = {
    'red_light': False,
    'green_light': False,
    'ready': False,
}

# --- Pad Functions ---
def pad_test(battery, circuit):
    pad_state['battery'] = battery
    pad_state['circuit'] = circuit
    if battery >= 75 and circuit == 'CLOSED':
        pad_state['green_light'] = True
        pad_state['red_light'] = False
        return 'READY'
    else:
        pad_state['green_light'] = False
        pad_state['red_light'] = False
        return 'TEST_FAIL'

def pad_enable():
    if pad_state['green_light']:
        pad_state['red_light'] = True
        pad_state['enabled'] = True
        return 'ENABLED'
    return 'BLOCKED'

# --- Control Functions ---
def control_ready():
    if pad_state['enabled']:
        control_state['red_light'] = True
        control_state['ready'] = True
        return 'READY_ACK'
    return 'COMM_ERROR'

def control_launch():
    if pad_state['enabled'] and control_state['ready']:
        print(f"{datetime.now()} - LAUNCH_STARTED")
        print(f"{datetime.now()} - LAUNCH_SUCCESS")
        control_state['green_light'] = True
        return 'LAUNCH_SUCCESS'
    else:
        return 'LAUNCH_FAIL'

# --- Reset states helper for tests ---
def reset_states():
    pad_state.update({'battery':100,'circuit':'CLOSED','green_light':False,'red_light':False,'enabled':False})
    control_state.update({'red_light':False,'green_light':False,'ready':False})

# --- Built-in Tests ---
def run_tests(tester_name=None, execution_time=None):
    print("========================================")
    print("        RLS TEST EXECUTION REPORT       ")
    print("========================================")

    # Handle defaults if not provided
    if tester_name is None:
        tester_name = "UNKNOWN_TESTER"
    if execution_time is None:
        execution_time = datetime.now()

    print(f"Executed by: {tester_name}")
    print(f"Execution time: {execution_time}")
    print("========================================\n")

    # Test numbering
    test_number = 1

    def record_test(description, expected, actual):
        nonlocal test_number
        test_id = f"TC-{test_number:02d}"
        test_number += 1

        result = "PASS" if expected == actual else "FAIL"

        print(f"Test Case: {test_id}")
        print(f"Description: {description}")
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        print(f"Result:   {result}")
        print("----------------------------------------\n")

    # --- Test Cases ---

    reset_states()
    result = pad_test(100, 'CLOSED')
    record_test("Pad passes test with 100% battery and CLOSED circuit",
                "READY", result)

    reset_states()
    result = pad_test(50, 'OPEN')
    record_test("Pad fails test with low battery and OPEN circuit",
                "TEST_FAIL", result)

    reset_states()
    pad_test(100, 'CLOSED')
    result = pad_enable()
    record_test("Pad successfully enables after ready state",
                "ENABLED", result)

    reset_states()
    result = pad_enable()
    record_test("Pad enable blocked when green_light is False",
                "BLOCKED", result)

    reset_states()
    pad_test(100, 'CLOSED')
    pad_enable()
    result = control_ready()
    record_test("Control ready succeeds when pad is enabled",
                "READY_ACK", result)

    reset_states()
    result = control_ready()
    record_test("Control ready fails when pad not enabled",
                "COMM_ERROR", result)

    reset_states()
    pad_test(100, 'CLOSED')
    pad_enable()
    control_ready()
    result = control_launch()
    record_test("Launch succeeds when pad enabled and control ready",
                "LAUNCH_SUCCESS", result)

    reset_states()
    result = control_launch()
    record_test("Launch fails when pad disabled or control not ready",
                "LAUNCH_FAIL", result)

    print("All tests completed.")

# --- Main Command-Line Interface ---
if __name__ == "__main__":
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser()
    parser.add_argument('--unit', choices=['pad','control'])
    parser.add_argument('--action', choices=['test','enable','ready','launch'])
    parser.add_argument('--battery', type=int, default=100)
    parser.add_argument('--circuit', choices=['OPEN','CLOSED'], default='CLOSED')
    parser.add_argument('--run-tests', action='store_true', help='Run internal tests')

    args = parser.parse_args()

    # --- If running test report execution ---
    if args.run_tests:
        # Ask tester for their first name
        tester_name = input("Enter your first name (tester): ").strip()

        # Capture execution timestamp
        execution_time = datetime.now()

        # Pass into test suite
        run_tests(
            tester_name=tester_name,
            execution_time=execution_time
        )

    # --- Normal CLI mode ---
    else:
        if args.unit == 'pad':
            if args.action == 'test':
                status = pad_test(args.battery, args.circuit)
                print(f"Pad Test: {status}, Green Light: {pad_state['green_light']}, Red Light: {pad_state['red_light']}")
            elif args.action == 'enable':
                status = pad_enable()
                print(f"Pad Enable: {status}, Red Light: {pad_state['red_light']}")
        elif args.unit == 'control':
            if args.action == 'ready':
                status = control_ready()
                print(f"Control Ready: {status}, Red Light: {control_state['red_light']}")
            elif args.action == 'launch':
                status = control_launch()
                print(f"Control Launch: {status}, Green Light: {control_state['green_light']}")

