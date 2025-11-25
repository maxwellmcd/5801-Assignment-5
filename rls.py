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
def run_tests():
    print("Running RLS Tests...\n")
    
    reset_states()
    result = pad_test(100, 'CLOSED')
    print("Pad Test Success:", "PASS" if result == "READY" else "FAIL")
    
    reset_states()
    result = pad_test(50, 'OPEN')
    print("Pad Test Fail:", "PASS" if result == "TEST_FAIL" else "FAIL")
    
    reset_states()
    pad_test(100, 'CLOSED')
    result = pad_enable()
    print("Pad Enable Success:", "PASS" if result == "ENABLED" else "FAIL")
    
    reset_states()
    result = pad_enable()
    print("Pad Enable Blocked:", "PASS" if result == "BLOCKED" else "FAIL")
    
    reset_states()
    pad_test(100, 'CLOSED')
    pad_enable()
    result = control_ready()
    print("Control Ready Success:", "PASS" if result == "READY_ACK" else "FAIL")
    
    reset_states()
    result = control_ready()
    print("Control Ready Fail:", "PASS" if result == "COMM_ERROR" else "FAIL")
    
    reset_states()
    pad_test(100, 'CLOSED')
    pad_enable()
    control_ready()
    result = control_launch()
    print("Control Launch Success:", "PASS" if result == "LAUNCH_SUCCESS" else "FAIL")
    
    reset_states()
    result = control_launch()
    print("Control Launch Fail:", "PASS" if result == "LAUNCH_FAIL" else "FAIL")
    
    print("\nAll tests completed.")

# --- Main Command-Line Interface ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--unit', choices=['pad','control'])
    parser.add_argument('--action', choices=['test','enable','ready','launch'])
    parser.add_argument('--battery', type=int, default=100)
    parser.add_argument('--circuit', choices=['OPEN','CLOSED'], default='CLOSED')
    parser.add_argument('--run-tests', action='store_true', help='Run internal tests')
    args = parser.parse_args()
    
    if args.run_tests:
        run_tests()
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
