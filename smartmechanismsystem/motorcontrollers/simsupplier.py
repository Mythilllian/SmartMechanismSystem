class SimSupplier:
    def update_sim_state() -> None:
        pass
    def get_updated_sim() -> bool:
        pass
    def feed_update_sim() -> None:
        pass
    def starve_update_sim() -> None:
        pass
    def is_input_fed() -> bool:
        pass
    def feed_input() -> None:
        pass
    def starve_input() -> None:
        pass
    def set_mechanism_stator_duty_cycle(duty_cycle: float) -> None:
        pass
    def get_mechanism_supply_voltage() -> float:
        pass
    def get_mechanism_stator_voltage() -> float:
        pass
    def set_mechanism_stator_voltage(volts: float) -> None:
        pass
    def get_mechanism_position() -> float:
        """
        Get the mechanism position.

        :return: mechanism angle.
        """
        pass
    def set_mechanism_position(position: float) -> None:
        """
        Set the mechanism position.

        :param position: Position of the mechanism.
        """
        pass
    def get_rotor_position() -> float:
        """
        Get the rotor position.

        :return: rotor position.
        """
        pass
    def get_mechanism_velocity() -> float:
        pass
    def set_mechanism_velocity(velocity: float) -> None:
        pass
    def get_rotor_velocity() -> float:
        pass
    def get_current_draw() -> float:
        pass