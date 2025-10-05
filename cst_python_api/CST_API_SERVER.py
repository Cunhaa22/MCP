from re import I
from mcp.server.fastmcp import FastMCP
from .Boolean import Boolean
from .Build import Build
from .CheckParam import CheckParam
from .Component import Component
from .CST_MicrowaveStudio import CST_MicrowaveStudio
from .Material import Material,materials_dir
from .Parameter import Parameter
from .Port import Port
from .Project import Project
from .Results import Results
from .Shape import Shape
from .Solver import Solver
from .Transform import Transform
from .feed import create_coax_and_port
from .farfield import _validate_common_inputs, get_axial_ratio_at_freq, get_gain_at_freq



mcp = FastMCP("CST_API_SERVER")

mcp.tool(Boolean.add)
mcp.tool(Boolean.subtract)
mcp.tool(Boolean.intersect)
mcp.tool(Boolean.insert)
mcp.tool(Boolean.mergeCommonMaterials)

mcp.tool(Build.deleteObject)

mcp.tool(CheckParam.doCheck)

mcp.tool(Component.new)
mcp.tool(Component.delete)
mcp.tool(Component.rename)
mcp.tool(Component.exist)
mcp.tool(Component.ensureExistence)

mcp.tool(CST_MicrowaveStudio.__openFile)
mcp.tool(CST_MicrowaveStudio.__checkExtension)
mcp.tool(CST_MicrowaveStudio.saveFile)
mcp.tool(CST_MicrowaveStudio.closeFile)
mcp.tool(CST_MicrowaveStudio.quit)

mcp.tool(Material.addNormalMaterial)
mcp.tool(Material.addAnisotropicMaterial)
mcp.tool(Material.addMaterialFromLib)

mcp.tool(Shape.addBrick)
mcp.tool(Shape.addCylinder)
mcp.tool(Shape.addSphere)
mcp.tool(Shape.addPolygonBlock)

mcp.tool(Transform.translate)
mcp.tool(Transform.rotate)      
mcp.tool(Transform.mirror)
mcp.tool(Transform.scale)  

mcp.tool(Parameter.add)
mcp.tool(Parameter.delete)
mcp.tool(Parameter.exist)
mcp.tool(Parameter.change)
mcp.tool(Parameter.retrieve)
mcp.tool(Parameter.addDescription)
mcp.tool(Parameter.retrieveDescription)

mcp.tool(Port.addWaveguidePort)
mcp.tool(Port.addDiscretePort)

mcp.tool(Project.setUnits)

mcp.tool(Results.getSParameters)
mcp.tool(Results.getFarField)
mcp.tool(Results._portNumberProcessor)


mcp.tool(Solver.setFrequencyRange)
mcp.tool(Solver.getSolverType)
mcp.tool(Solver.changeSolverType)
mcp.tool(Solver.setBoundaryCondition)
mcp.tool(Solver.addSymmetryPlane)
mcp.tool(Solver.addFieldMonitor)
mcp.tool(Solver.setBackgroundMaterial)
mcp.tool(Solver.setBackgroundLimits)
mcp.tool(Solver.defineFloquetModes)
mcp.tool(Solver.runSimulation)

mcp.tool(create_coax_and_port)
mcp.tool(_validate_common_inputs)
mcp.tool(get_axial_ratio_at_freq)
mcp.tool(get_gain_at_freq)

# Adicionar como recurso
@mcp.resource("materials_dir")
def get_materials_dir():
    """Diretório global dos materiais CST Studio Suite."""
    return str(materials_dir)

if __name__ == "__main__":
    mcp.run(transport="stdio")