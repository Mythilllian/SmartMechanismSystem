from wpimath.units import volts, radians, radians_per_second, amperes


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

    def get_mechanism_supply_voltage() -> volts:
        pass

    def get_mechanism_stator_voltage() -> volts:
        pass

    def set_mechanism_stator_voltage(volts: volts) -> None:
        pass

    def get_mechanism_position() -> radians:
        """
        Get the mechanism position in radians.

        :return: mechanism angle.
        """
        pass

    def set_mechanism_position(position: radians) -> None:
        """
        Set the mechanism position in radians.

        :param position: Position of the mechanism.
        """
        pass

    def get_rotor_position() -> radians:
        """
        Get the rotor position in radians.

        :return: rotor position.
        """
        pass

    def get_mechanism_velocity() -> radians_per_second:
        """
        Get the mechanism velocity in radians per second.

        :return: Mechanism velocity in radians per second.
        """
        pass

    def set_mechanism_velocity(velocity: radians_per_second) -> None:
        """
        Set the mechanism velocity in radians per second.

        :param velocity: Mechanism velocity in radians per second.
        """
        pass

    def get_rotor_velocity() -> radians_per_second:
        """
        Gets the rotor velocity in radians per second.

        :return: Rotor velocity.
        """
        pass

    def get_current_draw() -> amperes:
        """
        Gets the current draw of from the sim in amperes.

        :return: Current draw.
        """
        pass
