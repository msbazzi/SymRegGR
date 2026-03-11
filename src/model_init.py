"""Model initialization: native vessel and TEVG.

Keeps parser and mechanics separate. Use parsed dataclasses as input:

    native, scaffold, immune = load_case("Native_in_Lamb", "Scaffold_in_Lamb", "Immune_in_Lamb")
    native_vessel = initialize_native(native)
    tevg = initialize_tevg(scaffold=scaffold, native=native_vessel, immune=immune)
"""

from typing import Optional

from input_types import ImmuneParams, NativeParams, ScaffoldParams
from state_types import (
    ConstituentMassState,
    GeometryState,
    HemodynamicState,
    NativeVesselState,
    ScaffoldState,
    TEVGState,
)


def initialize_native(native: NativeParams) -> NativeVesselState:
    """Initialize native vessel from parsed NativeParams.

    Returns NativeVesselState with geometry, constituents, hemodynamics.
    """
    # TODO: Port full C++ initialization logic
    geometry = GeometryState(
        a=native.radius * 1e-3,  # mm -> m
        h=native.thickness * 1e-3,
        a_mid=native.radius * 1e-3 + native.thickness * 1e-3 / 2,
    )
    constituents = ConstituentMassState(rhoR_alpha=[], epsilon_alpha=[])
    hemodynamics = HemodynamicState(
        P=native.P_h,
        Q=native.Q_h,
        bar_tauw=0.0,  # computed from Q
    )
    return NativeVesselState(
        geometry=geometry,
        constituents=constituents,
        hemodynamics=hemodynamics,
        s=0.0,
        sn=0,
    )


def initialize_tevg(
    scaffold: ScaffoldParams,
    native: NativeVesselState,
    immune: Optional[ImmuneParams] = None,
) -> TEVGState:
    """Initialize TEVG from scaffold params and native vessel state.

    Args:
        scaffold: Parsed scaffold parameters
        native: Native vessel state from initialize_native()
        immune: Immune parameters (from Immune_in_* file); required for TEVG

    Returns:
        TEVGState
    """
    # TODO: Port full C++ TEVG initialization
    geometry = GeometryState(
        a=scaffold.radius * 1e-3,
        h=scaffold.thickness * 1e-3,
        a_mid=scaffold.radius * 1e-3 + scaffold.thickness * 1e-3 / 2,
    )
    constituents = ConstituentMassState(rhoR_alpha=[], epsilon_alpha=[])
    hemodynamics = HemodynamicState(P=0.0, Q=0.0, bar_tauw=0.0)
    return TEVGState(
        geometry=geometry,
        constituents=constituents,
        hemodynamics=hemodynamics,
        scaffold=ScaffoldState(),
        s=0.0,
        sn=0,
    )
