# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from .CST_MicrowaveStudio import *
from .Parameter import Parameter 
from .Material import Material
from .Shape import Shape
from .Boolean import Boolean
from .Transform import Transform
from .Component import Component
from .Port import Port
from .Solver import Solver
from .Results import Results
from .Build import Build
from .CheckParam import CheckParam
from .assemblies import create_coax_and_port
from .analysis import get_gain_at_freq, get_axial_ratio_at_freq

__version__ = "0.1.1"
__version_name__ = "Hanter dro"