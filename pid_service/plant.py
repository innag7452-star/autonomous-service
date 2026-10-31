class AltitudePlant:
    """Вертикальний канал мультикоптера: m*z'' = F - c*z' + d,  dF/dt = (u - F)/Tm."""

    def __init__(self, mass=1.2, drag=1.5, motor_tau=0.05):
        self.mass, self.drag, self.motor_tau = mass, drag, motor_tau
        self.z = self.v = self.thrust = 0.0

    def step(self, u, disturbance, dt):
        self.thrust += dt * (u - self.thrust) / self.motor_tau
        self.v += dt * (self.thrust - self.drag * self.v + disturbance) / self.mass
        self.z += dt * self.v
        return self.z
