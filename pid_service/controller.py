class PID:
    """PID-регулятор з похідною за вимірюванням (з фільтром) та захистом інтегратора від насичення."""

    def __init__(self, kp, ki, kd, u_min=-30.0, u_max=30.0, d_filter=0.05):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.u_min, self.u_max, self.d_filter = u_min, u_max, d_filter
        self.reset()

    def reset(self):
        self.integral = 0.0
        self._prev_meas = None
        self._d = 0.0

    def update(self, setpoint, measurement, dt):
        error = setpoint - measurement
        if self._prev_meas is not None:
            raw = -(measurement - self._prev_meas) / dt          # похідна за вимірюванням
            self._d += dt / (self.d_filter + dt) * (raw - self._d)
        self._prev_meas = measurement
        u_unsat = self.kp * error + self.ki * self.integral + self.kd * self._d
        u = min(max(u_unsat, self.u_min), self.u_max)
        if u == u_unsat:                                         # anti-windup: не інтегруємо в насиченні
            self.integral += error * dt
        return u
