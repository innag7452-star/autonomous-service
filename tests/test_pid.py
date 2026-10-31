from pid_service.controller import PID


def test_proportional_term():
    pid = PID(kp=2.0, ki=0.0, kd=0.0)
    assert pid.update(setpoint=1.0, measurement=0.0, dt=0.01) == 2.0


def test_integral_accumulates():
    pid = PID(kp=0.0, ki=1.0, kd=0.0)
    u1 = pid.update(1.0, 0.0, 0.1)
    u2 = pid.update(1.0, 0.0, 0.1)
    assert u2 > u1


def test_output_is_saturated():
    pid = PID(kp=100.0, ki=0.0, kd=0.0, u_min=-5.0, u_max=5.0)
    assert pid.update(10.0, 0.0, 0.01) == 5.0
    assert pid.update(-10.0, 0.0, 0.01) == -5.0


def test_anti_windup_stops_integration_when_saturated():
    pid = PID(kp=100.0, ki=1.0, kd=0.0, u_max=5.0)
    for _ in range(100):
        pid.update(10.0, 0.0, 0.01)
    assert pid.integral == 0.0


def test_reset_clears_state():
    pid = PID(kp=1.0, ki=1.0, kd=1.0)
    pid.update(1.0, 0.0, 0.1)
    pid.reset()
    assert pid.integral == 0.0
