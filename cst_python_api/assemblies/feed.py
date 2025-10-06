# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Any


def create_coax_and_port(
    myCST: Any,
    *,
    xfeed: float = 0.0,
    yfeed: float = 0.0,
    feed_z_bot: float = -3.0,
    feed_z_top: float = 0.6,
    inner_conn_rad: float = 0.65,
    consub_outer_rad: float = 2.05,
    outer_shield_outer_rad: float = 3.0,
    coax_component: str = "Coax",
    inner_name: str = "InnerConn",
    consub_name: str = "ConSubstrate",
    outer_name: str = "OuterShield",
    inner_mat: str = "Copper (annealed)",
    consub_mat: str = "PTFE (lossy)",
    outer_mat: str = "Copper (annealed)",
    make_ground_cut: bool = True,
    ground_component: str = "component1:Groundplane",
    nModes: int = 1,
    orientation: str = "zmin",
) -> None:
    """Create a coaxial feed structure and associated port inside a CST model.

    Parameters
    ----------
    myCST : Any
        Handle to the active CST project (Hermes API MWS instance).
    xfeed, yfeed : float
        X and Y coordinates of the coax centre.
    feed_z_bot : float
        Lowest z-coordinate of the coax (port plane).
    feed_z_top : float
        Highest z-coordinate of the inner pin (penetration above ground plane).
    inner_conn_rad : float
        Radius of the inner conductor.
    consub_outer_rad : float
        Outer radius of the dielectric substrate surrounding the inner pin.
    outer_shield_outer_rad : float
        Outer radius of the metallic shield.
    coax_component : str
        Name of the component where the coax solids are stored/created.
    inner_name, consub_name, outer_name : str
        Solid names for the inner conductor, dielectric, and outer shield.
    inner_mat, consub_mat, outer_mat : str
        CST material library names for the coax solids.
    make_ground_cut : bool
        If True, cut a circular opening in the ground geometry.
    ground_component : str
        Identifier of the ground solid to be cut (component:solid format).
    nModes : int
        Number of modes to excite in the coaxial waveguide port.
    orientation : str
        Orientation of the waveguide port (e.g., "zmin").

    Returns
    -------
    None
        The CST project is modified in place.
    """

    # Ensure required materials are loaded from the CST library.
    myCST.Build.Material.addMaterialFromLib(inner_mat)
    myCST.Build.Material.addMaterialFromLib(consub_mat)
    myCST.Build.Material.addMaterialFromLib(outer_mat)

    # Ensure the destination component exists before creating solids.
    myCST.Build.Component.ensureExistence(coax_component)

    # Inner conductor (solid cylinder spanning the feed penetration depth).
    myCST.Build.Shape.addCylinder(
        xMin=xfeed,
        yMin=yfeed,
        zMin=feed_z_bot,
        zMax=feed_z_top,
        extRad=inner_conn_rad,
        intRad=0.0,
        name=inner_name,
        component=coax_component,
        material=inner_mat,
        orientation="z",
    )

    # Dielectric layer (hollow cylinder stopping at the ground reference plane).
    myCST.Build.Shape.addCylinder(
        xMin=xfeed,
        yMin=yfeed,
        zMin=feed_z_bot,
        zMax=0.0,
        extRad=consub_outer_rad,
        intRad=inner_conn_rad,
        name=consub_name,
        component=coax_component,
        material=consub_mat,
        orientation="z",
    )

    # Outer metallic shield (hollow cylinder terminating at the ground plane).
    myCST.Build.Shape.addCylinder(
        xMin=xfeed,
        yMin=yfeed,
        zMin=feed_z_bot,
        zMax=0.0,
        extRad=outer_shield_outer_rad,
        intRad=consub_outer_rad,
        name=outer_name,
        component=coax_component,
        material=outer_mat,
        orientation="z",
    )

    if make_ground_cut:
        cut_name = "CoaxCut"
        myCST.Build.Shape.addCylinder(
            xMin=xfeed,
            yMin=yfeed,
            zMin=feed_z_bot,
            zMax=feed_z_top,
            extRad=outer_shield_outer_rad,
            intRad=0.0,
            name=cut_name,
            component=coax_component,
            material="Vacuum",
            orientation="z",
        )
        myCST.Build.Boolean.subtract(
            f"{ground_component}",
            f"{coax_component}:{cut_name}"
        )

    myCST.Solver.Port.addWaveguidePort(
        xMin=xfeed - outer_shield_outer_rad,
        xMax=xfeed + outer_shield_outer_rad,
        yMin=yfeed - outer_shield_outer_rad,
        yMax=yfeed + outer_shield_outer_rad,
        zMin=feed_z_bot,
        zMax=feed_z_bot,
        orientation=orientation,
        nModes=nModes,
    )
