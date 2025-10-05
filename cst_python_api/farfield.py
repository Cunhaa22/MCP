# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

"""High-level helpers for farfield post-processing."""

from __future__ import annotations

from typing import Any

import numpy as np
from pywintypes import com_error


__all__ = ["get_gain_at_freq", "get_axial_ratio_at_freq"]


async def _validate_common_inputs(myCST: Any, target_freq: float, port: int, mode: int) -> None:
    """Validate shared arguments for farfield helper routines."""

    if myCST is None:
        raise TypeError("ERROR: myCST object must be provided.")
    if not isinstance(target_freq, (float, int)):
        raise TypeError("ERROR: target_freq must be float or int.")
    if not isinstance(port, int):
        raise TypeError("ERROR: port must be of type int.")
    if port < 1:
        raise ValueError("ERROR: port must be an integer >= 1.")
    if not isinstance(mode, int):
        raise TypeError("ERROR: mode must be of type int.")
    if mode < 0:
        raise ValueError("ERROR: mode must be an integer >= 0.")


async def get_gain_at_freq(
    myCST: Any,
    *,
    target_freq: float = 0.868,
    port: int = 1,
    mode: int = 0,
) -> float:
    """Retrieve the realised gain (dBi) at boresight for a farfield monitor.

    The routine expects that a farfield monitor exists at ``target_freq`` and
    that the CST project has already been solved. It queries the monitor at
    ``theta = 0`` and ``phi = 0`` for both theta- and phi-polarised realised
    gain components, combines them in linear scale, and returns the total gain
    in dBi.

    Parameters
    ----------
    myCST : Any
        Active CST project wrapper exposing ``Results.getFarField``.
    target_freq : float, optional
        Frequency for which the farfield monitor was defined.
    port : int, optional
        Excitation port number. Must be greater or equal to 1.
    mode : int, optional
        Port mode number. Use 0 for single-mode ports.

    Returns
    -------
    float
        Realised gain at ``theta=0 degrees`` and ``phi=0 degrees`` in dBi.

    Raises
    ------
    TypeError
        If any argument does not present the expected type.
    ValueError
        If ``port`` or ``mode`` violate their allowed ranges.
    RuntimeError
        If the farfield monitor cannot be retrieved or parsed.
    """

    _validate_common_inputs(myCST, target_freq, port, mode)

    theta = np.array([0.0])
    phi = np.array([0.0])

    try:
        farfield_results_gain = await myCST.Results.getFarField(
            freq=target_freq,
            theta=theta,
            phi=phi,
            port=port,
            mode=mode,
            plotMode="realized gain",
            coordSys="spherical",
            polarization="circular",
            component=["theta", "phi"],
            complexComp=["abs", "abs"],
            linearScale=False,
        )
    except com_error as err:
        details = getattr(err, "excepinfo", (None, None, ""))
        raise RuntimeError(
            f"ERROR: CST failed to retrieve farfield data. Details: {details[2]}"
        ) from err
    except Exception as err:  # pragma: no cover - passthrough for unexpected errors
        raise RuntimeError(
            f"ERROR: Unexpected failure retrieving farfield results. {err}"
        ) from err

    if not farfield_results_gain or len(farfield_results_gain) < 2:
        raise RuntimeError("ERROR: Farfield results are empty or incomplete.")

    try:
        theta_component = float(np.asarray(farfield_results_gain[0]).item())
        phi_component = float(np.asarray(farfield_results_gain[1]).item())
    except Exception as err:  # pragma: no cover - defensive parsing guard
        raise RuntimeError(
            "ERROR: Could not extract theta/phi values from CST farfield."
        ) from err

    gain_dBi = 10.0 * np.log10(
        10.0 ** (theta_component / 10.0) + 10.0 ** (phi_component / 10.0)
    )

    return gain_dBi


async def get_axial_ratio_at_freq(
    myCST: Any,
    *,
    target_freq: float = 0.868,
    port: int = 1,
    mode: int = 0,
) -> float:
    """Retrieve the axial ratio (dB) at boresight for a farfield monitor.

    The routine expects that a farfield monitor exists at ``target_freq`` and
    that the CST project has already been solved. It queries the monitor at
    ``theta = 0`` and ``phi = 0`` for right- and left-hand circularly polarised
    electric field components, combines them in linear scale, and returns the
    axial ratio in dB.

    Parameters
    ----------
    myCST : Any
        Active CST project wrapper exposing ``Results.getFarField``.
    target_freq : float, optional
        Frequency for which the farfield monitor was defined.
    port : int, optional
        Excitation port number. Must be greater or equal to 1.
    mode : int, optional
        Port mode number. Use 0 for single-mode ports.

    Returns
    -------
    float
        Axial ratio at ``theta=0 degrees`` and ``phi=0 degrees`` in dB.

    Raises
    ------
    TypeError
        If any argument does not present the expected type.
    ValueError
        If ``port`` or ``mode`` violate their allowed ranges.
    RuntimeError
        If the farfield monitor cannot be retrieved or parsed.
    """

    _validate_common_inputs(myCST, target_freq, port, mode)

    theta = np.array([0.0])
    phi = np.array([0.0])

    try:
        farfield_results = await myCST.Results.getFarField(
            freq=target_freq,
            theta=theta,
            phi=phi,
            port=port,
            mode=mode,
            plotMode="efield",
            coordSys="spherical",
            polarization="circular",
            component=["right", "left"],
            complexComp=["abs", "abs"],
            linearScale=True,
        )
    except com_error as err:
        details = getattr(err, "excepinfo", (None, None, ""))
        raise RuntimeError(
            f"ERROR: CST failed to retrieve farfield data. Details: {details[2]}"
        ) from err
    except Exception as err:  # pragma: no cover - passthrough for unexpected errors
        raise RuntimeError(
            f"ERROR: Unexpected failure retrieving farfield results. {err}"
        ) from err

    if not farfield_results or len(farfield_results) < 2:
        raise RuntimeError("ERROR: Farfield results are empty or incomplete.")

    try:
        right = float(np.asarray(farfield_results[0]).item())
        left = float(np.asarray(farfield_results[1]).item())
    except Exception as err:  # pragma: no cover - defensive parsing guard
        raise RuntimeError(
            "ERROR: Could not extract circular components from CST farfield."
        ) from err

    emax, emin = (right, left) if right >= left else (left, right)
    numerator = emax + emin
    denominator = max(emax - emin, 1e-300)
    ar_linear = numerator / denominator
    ar_dB = 20.0 * np.log10(ar_linear)

    return ar_dB
