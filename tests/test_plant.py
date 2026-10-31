from pid_service.plant import AltitudePlant


def test_no_input_no_motion():
    plant = AltitudePlant()
    for _ in range(200):
        plant.step(u=0.0, disturbance=0.0, dt=0.005)
    assert plant.z == 0.0


def test_positive_thrust_raises_altitude():
    plant = AltitudePlant()
    for _ in range(400):
        plant.step(u=5.0, disturbance=0.0, dt=0.005)
    assert plant.z > 0.0


def test_negative_disturbance_lowers_altitude():
    plant = AltitudePlant()
    for _ in range(400):
        plant.step(u=0.0, disturbance=-3.0, dt=0.005)
    assert plant.z < 0.0
