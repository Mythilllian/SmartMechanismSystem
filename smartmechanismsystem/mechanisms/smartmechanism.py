from commands2 import Command, Subsystem
from smartmechanismsystem.gearing.gearbox import GearBox
from smartmechanismsystem.gearing.sprocket import Sprocket
from smartmechanismsystem.gearing.mechanismgearing import MechanismGearing
from smartmechanismsystem.motorcontrollers.smartmotorcontroller import (
    SmartMotorController,
)
from smartmechanismsystem.telemetry.telemetry import MechanismTelemetry


class SmartMechanism:
    """
    Generic implementation of a mechanism with advanced telemetry.
    """

    _subsystem: Subsystem
    _smc: SmartMotorController
    _telemetry: MechanismTelemetry = MechanismTelemetry()
    # TODO
