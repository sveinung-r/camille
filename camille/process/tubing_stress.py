from math import cos, sin, radians, pi

def process(north, south, east, west,
            angle=None, level_offset=0,
            crs_thickness=None, crs_diameter=None):
    """

    Parameters
    ----------
    north : pandas.Series
        North strain [kN]
    south : pandas.Series
        South strain [kN]
    east : pandas.Series
        East strain [kN]
    west : pandas.Series
        West strain [kN]
    angle : int or float
        Angle (from north) at which the tension is to be computed [deg]
    level_offset : int or float, optional
        The offset angle (from north) of the cross section [deg]
    crs_thickness : int or float
        Thickness of the cross section [mm]
    crs_diameter : int or float
        Diameter of the cross section [m]

    Returns
    -------
    pandas.Series
        Stress in the material induced from tensions on the chains [MPa]
    """
    angle = radians(angle)
    level_offset = radians(level_offset)

    Emod = 2.07e11 / 1e3
    ID = crs_diameter - 2 * crs_thickness * 1e-3
    I = pi / 64 * (crs_diameter**4 - ID**4)
    EI = Emod * I

    mom_y = 0.5 * (north - south) * 1e-6 * EI / (ID/2)
    mom_z = 0.5 * (east - west) * 1e-6 * EI / (ID/2)
    #mom_y = (north - south) * 1e-6 * EI / ID
    #mom_z = (east - west) * 1e-6 * EI / ID

    # Rotate to account for level offset
    mom_y, mom_z = [
        mom_y * cos(level_offset) - mom_z * sin(level_offset),
        mom_z * cos(level_offset) + mom_y * sin(level_offset)
    ]
    print(mom_y[:20])
    exit()
    #import numpy as np
    #print(np.mean(mom_z))
    #print("mom_y mean: ", mom_y.mean())
    #print("mom_z mean: ", mom_z.mean())
    #print("mom_y std: ", mom_y.std())
    #print("mom_z std: ", mom_z.std())

    stress = 1e-3 * (mom_y * cos(angle) + mom_z * sin(angle)) / I * ID / 2

    return stress
