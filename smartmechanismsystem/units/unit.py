from smartmechanismsystem.exceptions import UnitException

__all__ = ["Unit", "UnitValue"]

class Unit():
    """
    Base class for units of measurement.

    Used for the unit itself, not the value of a unit.
    """

    base_value: float # how many of a base unit this unit is worth

    name: str # the name of the unit, i.e. "meters", "seconds", "kilograms"
    abbreviation: str # the abbreviation of the unit, i.e. "m", "s", "kg"

    def __init__(self, base_value: float = 1.0, name: str = "unit", abbreviation: str = "u") -> None:
        self.base_value = base_value
        self.name = name
        self.abbreviation = abbreviation

    def conversion_factor_to(self, other: "Unit") -> float:
        """
        Factor needed to convert from this unit to the other unit. 
        Multiply this unit by the conversion factor to get the other unit.

        :param other: The unit to convert to
        :return: The conversion factor from this unit to the other unit
        """
        if(type(self) != type(other)):
            raise UnitException("Cannot convert between different types of units", "Cannot convert from " + str(type(self)) + " (" + self.name + ") to " + str(type(other)) + " (" + other.name + ")", "conversion_factor_to")

        return self.base_value / other.base_value
    
    def conversion_factor_from(self, other: "Unit") -> float:
        """
        Factor needed to convert from the other unit to this unit. 
        Multiply the other unit by the conversion factor to get this unit.

        :param other: The unit to convert from
        :return: The conversion factor from the other unit to this unit
        """
        if(type(self) != type(other)):
            raise UnitException("Cannot convert between different types of units", "Cannot convert from " + str(type(self)) + " (" + self.name + ") to " + str(type(other)) + " (" + other.name + ")", "conversion_factor_to")

        return other.base_value / self.base_value
    
    def __str__(self) -> str:
        return self.name + " (" + self.abbreviation + ")"

class UnitValue():
    """
    Base class for a value of a unit of measurement.

    Used for the value of a unit, not the unit itself.
    """
    unit: Unit
    magnitude: float

    def __init__(self, magnitude: float, unit: Unit = Unit()) -> None:
        self.magnitude = magnitude
        self.unit = unit

    def convert(self, other_unit: Unit) -> "UnitValue":
        """
        Convert this UnitValue to another Unit of the same unit type.

        :param other_unit: The unit to convert to
        :return: A new UnitValue with the converted magnitude and the other unit
        """
        conversion_factor = self.unit.conversion_factor_to(other_unit)
        return UnitValue(self.magnitude * conversion_factor, other_unit)
    
    def add(self, other: "UnitValue") -> "UnitValue":
        """
        Add this UnitValue to another UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to add
        :return: A new UnitValue with the sum of the UnitValues in the unit as this UnitValue
        """
        
        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude + converted_other.magnitude, self.unit)
    
    def subtract(self, other: "UnitValue") -> "UnitValue":
        """
        Subtract another UnitValue from this UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to subtract
        :return: A new UnitValue with the difference of the UnitValues in the unit as this UnitValue
        """

        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude - converted_other.magnitude, self.unit)
    
    def multiply(self, other: "UnitValue") -> "UnitValue":
        """
        Multiply this UnitValue by another UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to multiply by
        :return: A new UnitValue with the product of the UnitValues and a compound unit
        """
        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude * converted_other.magnitude, self.unit)
    
    def divide(self, other: "UnitValue") -> "UnitValue":
        """
        Divide this UnitValue by another UnitValue of the same unit type, and returns them in the Unit of this UnitValue.

        :param other: The UnitValue to divide by
        :return: A new UnitValue with the quotient of the UnitValues and a compound unit
        """
        converted_other = other.convert(self.unit)
        return UnitValue(self.magnitude / converted_other.magnitude, self.unit)

    def __str__(self) -> str:
        return str(self.magnitude) + " " + self.unit.abbreviation

# angular acceleration
radians_per_second_squared = float
degrees_per_second_squared = float
turns_per_second_squared = float

# angular velocity
radians_per_second = float
degrees_per_second = float
turns_per_second = float
revolutions_per_minute = float
milliarcseconds_per_year = float

# area
square_meters = float
square_feet = float
square_inches = float
square_miles = float
square_kilometers = float
hectares = float
acres = float

# capacitance
farads = float
nanofarads = float
microfarads = float
millifarads = float
kilofarads = float

# compound types
radians_per_meter = float
radians_per_second_per_volt = float
units_per_second = float
units_per_second_squared = float
volt_seconds = float
volt_seconds_squared = float
volt_seconds_per_meter = float
volt_seconds_squared_per_meter = float
volt_seconds_per_feet = float
volt_seconds_squared_per_feet = float
volt_seconds_per_radian = float
volt_seconds_squared_per_radian = float
unit_seconds_squared_per_unit = float
meters_per_second_squared_per_volt = float

# charge
coulombs = float
nanocoulombs = float
microcoulombs = float
millicoulombs = float
kilocoulombs = float
ampere_hours = float
nanoampere_hours = float
microampere_hours = float
milliampere_hours = float
kiloampere_hours = float

# concentration
parts_per_million = float
parts_per_billion = float
parts_per_trillion = float
percent = float

# conductance
siemens = float
nanosiemens = float
microsiemens = float
millisiemens = float
kilosiemens = float

# current
amperes = float
nanoamperes = float
microamperes = float
milliamperes = float
kiloamperes = float

# data
exabytes = float
exabits = float

# data transfer
exabytes_per_second = float
exabits_per_second = float

# density
kilograms_per_cubic_meter = float
grams_per_milliliter = float
kilograms_per_liter = float
ounces_per_cubic_foot = float
ounces_per_cubic_inch = float
ounces_per_gallon = float
pounds_per_cubic_foot = float
pounds_per_cubic_inch = float
pounds_per_gallon = float
slugs_per_cubic_foot = float

# energy
joules = float
nanojoules = float
microjoules = float
millijoules = float
kilojoules = float
calories = float
nanocalories = float
microcalories = float
millicalories = float
kilocalories = float
kilowatt_hours = float
watt_hours = float
british_thermal_units = float
british_thermal_units_iso = float
british_thermal_units_59 = float
therms = float
foot_pounds = float

# force
newtons = float
nanonewtons = float
micronewtons = float
millinewtons = float
kilonewtons = float
pounds = float
dynes = float
kiloponds = float
poundals = float

# frequency
hertz = float
nanohertz = float
microhertz = float
millihertz = float
kilohertz = float

# illuminance
luxes = float
nanoluxes = float
microluxes = float
milliluxes = float
kiloluxes = float
footcandles = float
lumens_per_square_inch = float
phots = float

# inductance
henries = float
nanohenries = float
microhenries = float
millihenries = float
kilohenries = float

# length
meters = float
nanometers = float
micrometers = float
millimeters = float
centimeters = float
kilometers = float
feet = float
mils = float
inches = float
miles = float
nauticalMiles = float
astronicalUnits = float
lightyears = float
parsecs = float
angstroms = float
cubits = float
fathoms = float
chains = float
furlongs = float
hands = float
leagues = float
nauticalLeagues = float
yards = float

# luminous flux
lumens = float
nanolumens = float
microlumens = float
millilumens = float
kilolumens = float

# luminous intensity
candelas = float
nanocandelas = float
microcandelas = float
millicandelas = float
kilocandelas = float

# magnetic flux
webers = float
nanowebers = float
microwebers = float
milliwebers = float
kilowebers = float
maxwells = float

# magnetic strength
teslas = float
nanoteslas = float
microteslas = float
milliteslas = float
kiloteslas = float
gauss = float

# mass
grams = float
nanograms = float
micrograms = float
milligrams = float
kilograms = float
metric_tons = float
pounds = float
long_tons = float
short_tons = float
stone = float
ounces = float
carats = float
slugs = float

# moment of inertia
kilogram_square_meters = float

# power
watts = float
nanowatts = float
microwatts = float
milliwatts = float
kilowatts = float
horsepower = float

# pressure
pascals = float
nanopascals = float
micropascals = float
millipascals = float
kilopascals = float
bars = float
mbars = float
atmospheres = float
pounds_per_square_inch = float
torrs = float

# radiation
becquerels = float
nanobecquerels = float
microbecquerels = float
millibecquerels = float
kilobecquerels = float
grays = float
nanograys = float
micrograys = float
milligrays = float
kilograys = float
sieverts = float
nanosieverts = float
microsieverts = float
millisieverts = float
kilosieverts = float
curies = float
rutherfords = float
rads = float

# resistance
ohms = float
nanoohms = float
microohms = float
milliohms = float
kiloohms = float

# solid angle
steradians = float
nanosteradians = float
microsteradians = float
millisteradians = float
kilosteradians = float
degrees_squared = float
spats = float

# substance
moles = float

# temperature
kelvin = float
celsius = float
fahrenheit = float
reaumur = float
rankine = float

# time
seconds = float
nanoseconds = float
microseconds = float
milliseconds = float
kiloseconds = float
minutes = float
hours = float
days = float
weeks = float
years = float
julian_years = float
gregorian_years = float

# torque
newton_meters = float
foot_poundals = float
inch_pounds = float
meter_kilograms = float

# velocity
meters_per_second = float
feet_per_second = float
miles_per_hour = float
kilometers_per_hour = float
knots = float

# voltage
volts = float
nanovolts = float
microvolts = float
millivolts = float
kilovolts = float
statvolts = float
abvolts = float

# volume
cubic_meters = float
cubic_millimeters = float
cubic_kilometers = float
liters = float
nanoliters = float
microliters = float
milliliters = float
kiloliters = float
cubic_inches = float
cubic_feet = float
cubic_yards = float
cubic_miles = float
gallons = float
quarts = float
pints = float
cups = float
fluid_ounces = float
barrels = float
bushels = float
cords = float
cubic_fathoms = float
tablespoons = float
teaspoons = float
pinches = float
dashes = float
drops = float
fifths = float
drams = float
gills = float
pecks = float
sacks = float
shots = float
strikes = float