# Rocket Launch System v0.1 - User Stories

## Scenario
We are testing a rocket launch sequence. The operator wants to:  
1. Check that battery, circuit, and communication are all working.  
2. Enable the launch system.  
3. Try launching with failures to see that it blocks the launch.  
4. Successfully launch when everything is okay.

## User Stories

### Story 1: Pre-launch checks
- **Who:** Test operator  
- **What:** Run checks for battery, circuit, and communication before enabling launch.  
- **Acceptance Criteria:**  
  1. Battery >= threshold → pass; else → `BATTERY_LOW`.  
  2. Circuit closed → pass; else → `CIRCUIT_OPEN`.  
  3. Communication connected → pass; else → `COMMS_FAILURE`.  
  4. If all pass → `SYSTEM READY`.  
  5. If any fail → show which check failed and don’t allow enable.  
- **Tests:** TC-01, TC-02

### Story 2: Enable system
- **Who:** Test operator  
- **What:** Enable the launch system only if checks pass.  
- **Acceptance Criteria:**  
  1. Pressing `ENABLE` runs checks again.  
  2. If all pass → system state = `ENABLED`.  
  3. If any fail → `LAUNCH_BLOCKED` and reason.  
- **Tests:** TC-03, TC-04

### Story 3: Launch with failures
- **Who:** Test operator  
- **What:** Attempt a launch while simulating failures.  
- **Acceptance Criteria:**  
  1. If any failure exists → `LAUNCH_BLOCKED` and reason.  
  2. If no failure → `LAUNCH_STARTED`.  
- **Tests:** TC-05, TC-06

### Story 4: Successful launch
- **Who:** Test operator  
- **What:** Run a full successful launch.  
- **Acceptance Criteria:**  
  1. Pre-launch checks pass → `ENABLED`.  
  2. Launch command → `LAUNCH_SUCCESS`.  
  3. Logs show steps with timestamps.  
- **Tests:** TC-07
