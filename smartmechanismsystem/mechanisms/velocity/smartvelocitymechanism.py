from abc import ABC, abstractmethod
from wpilib import MechanismRoot2d, MechanismLigament2d
from wpimath.units import volts, seconds
from commands2 import Command
from commands2.button import Trigger
from smartmechanismsystem.mechanisms.smartmechanism import SmartMechanism
from smartmechanismsystem.motorcontrollers.smartmotorcontroller import (
    SmartMotorController,
)


class SmartVelocityMechanism(SmartMechanism, ABC):
    _mechanism_root: MechanismRoot2d
    _mechanism_ligament: MechanismLigament2d

    @abstractmethod
    def max(self) -> Trigger: ...
    @abstractmethod
    def min(self) -> Trigger: ...
    @abstractmethod
    def sys_id(
        self, maximum_voltage: volts, step: volts, duration: seconds
    ) -> Command: ...

    def get_mechanism_ligament(self) -> MechanismLigament2d:
        return self._mechanism_ligament

    def get_mechanism_root(self) -> MechanismRoot2d:
        return self._mechanism_root

    def get_motor(self) -> SmartMotorController:
        return self._smc
