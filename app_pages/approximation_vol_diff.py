import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import _canoeValues as cv

# Default file names and data directory
DEFAULT_INNER = "Inner Hull.csv"
DEFAULT_OUTER = "Outer Hull.csv"
DEFAULT_DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data'))


def load_hull_points(data_dir: str = DEFAULT_DATA_DIR,
                     inner_file: str = DEFAULT_INNER,
                     outer_file: str = DEFAULT_OUTER):
    """Load inner and outer hull CSVs from the repo-level data directory.
    Returns: (x_in,y_in,z_in,x_out,y_out,z_out)
    """
    script_dir = data_dir
    in_path = os.path.join(script_dir, inner_file)
    out_path = os.path.join(script_dir, outer_file)

    in_coor = pd.read_csv(in_path, header=None)
    out_coor = pd.read_csv(out_path, header=None)

    x_in = in_coor[0]
    y_in = in_coor[1]
    z_in = in_coor[2]

    x_out = out_coor[0]
    y_out = out_coor[1]
    z_out = out_coor[2]

    return x_in, y_in, z_in, x_out, y_out, z_out


def compute_hull_station_volumes(x, y, z):
    """Compute per-station volumes and plotting arrays for one hull (inner or outer).
    Returns: dict with keys: 'station', 'vol', 'plotHull', 'plotStation', 'crossSectionArea'
    """
    station = pd.Series(x).unique()
    station_no = len(station)

    vol = []
    plotHull = [[], []]
    plotStation = []
    crossSectionArea = [0] * (station_no - 1)

    for k in range(0, station_no - 1):
        plotStation.append([[], []])
        X1_value = station[k]
        X2_value = station[k + 1]

        Y1 = []
        Z1 = []
        Y2 = []
        Z2 = []

        # collect points for the two stations
        for i in range(len(x)):
            if x.iloc[i] == X1_value:
                Y1.append(y.iloc[i])
                Z1.append(z.iloc[i])
                plotHull[0].append(y.iloc[i])
                plotHull[1].append(z.iloc[i])
                plotStation[k][0].append(y.iloc[i])
                plotStation[k][1].append(z.iloc[i])
            elif x.iloc[i] == X2_value:
                Y2.append(y.iloc[i])
                Z2.append(z.iloc[i])

        # compute volume for this station
        volume = 0
        if k == 0:
            l = abs(max(Y2) - min(Y2))
            w = abs(max(Z2) - min(Z2))
            h = abs(X2_value - X1_value)
            volume = l * w * h / 3
        elif k == station_no - 2:
            l = abs(max(Y1) - min(Y1))
            w = abs(max(Z1) - min(Z1))
            h = abs(X1_value - X2_value)
            volume = l * w * h / 3
        elif len(Y1) != 0:
            n = (len(Y1) - 1) // 2
            for j in range(0, n):
                area1 = (abs(Y1[j]) + abs(Y1[j + 1])) * abs(Z1[j] - Z1[j + 1]) / 2 * 2
                area2 = (abs(Y2[j]) + abs(Y2[j + 1])) * abs(Z2[j] - Z2[j + 1]) / 2 * 2
                crossSectionArea[k] -= ((abs(Y1[j]) - abs(Y1[j + 1])) * abs(Z1[j] - Z1[j + 1]) + (abs(Y2[j]) - abs(Y2[j + 1])) * abs(Z2[j] - Z2[j + 1])) / 2
                volume += abs(X1_value - X2_value) * (area1 + area2) / 2
            # triangle at bottom
            area1 = abs(Y1[n - 1]) * abs(Z1[n] - Z1[n - 1]) / 2 * 2
            area2 = abs(Y2[n - 1]) * abs(Z2[n] - Z2[n - 1]) / 2 * 2
            crossSectionArea[k] -= (area1 + area2) / 2
            volume += abs(X1_value - X2_value) * (area1 + area2) / 2

        vol.append(volume)

    return {
        'station': station,
        'vol': vol,
        'plotHull': plotHull,
        'plotStation': plotStation,
        'crossSectionArea': crossSectionArea,
    }


def compute_canoe_mass(vol_in, vol_out, concrete_density=cv.concrete_density):
    """Compute station concrete volumes (outer - inner) and masses.

    vol_* inputs expected in mm^3 per station.
    Returns: stat_vol (mm^3), stat_mass (kg), canoe_m (kg)
    """
    stat_vol = [vo - vi for vi, vo in zip(vol_in, vol_out)]
    canoe_vol = sum(stat_vol)
    stat_mass = [v / (10 ** 9) * concrete_density for v in stat_vol]
    canoe_m = canoe_vol / (10 ** 9) * concrete_density
    return stat_vol, stat_mass, canoe_m


def compute_shear_and_moment(stat_mass, station, x_out, stand_positions=None, g=9.81):
    """Compute shear and bending moment along the canoe length.
    Returns: x (list), shear (list), moment (list), stand_positions
    """
    if stand_positions is None:
        length = max(x_out)
        stand_positions = [length / 3, length / 3 * 2]

    stat_x = [((station[i] + station[i + 1]) / 2) for i in range(len(station) - 1)]

    length = int(max(x_out))
    x = list(range(0, length))
    shear = []
    for xi in x:
        shear_force = 0
        for j, sx in enumerate(stat_x):
            if xi >= sx:
                shear_force += (-1) * stat_mass[j] * g
        for sp in stand_positions:
            if xi >= sp:
                shear_force += 0  # placeholder: stand force addition can be added by caller
        shear.append(shear_force)

    # compute bending moment from shear
    moment = [0]
    bending_moment = 0
    for i in range(0, len(x) - 1):
        bending_moment += (x[i + 1] - x[i]) * shear[i + 1] / 1000
        moment.append(bending_moment)

    return x, shear, moment, stand_positions


def export_station_tables(data_dir: str = DEFAULT_DATA_DIR,
                          station_by_length=None,
                          x=None,
                          shear=None,
                          moment=None,
                          station_info_df: pd.DataFrame = None,
                          shear_and_moment_df: pd.DataFrame = None):
    """Write a set of CSV outputs to the repo-level `data` folder.
    Only writes files for provided non-None arguments.
    """
    if station_by_length is not None and x is not None and shear is not None:
        df = pd.DataFrame({'Station': station_by_length, 'Length': x, 'Shear': shear})
        df.to_csv(os.path.join(data_dir, 'Length_vs_Shear_Display_Stand.csv'), index=False)

    if station_by_length is not None and x is not None and moment is not None:
        df = pd.DataFrame({'Station': station_by_length, 'Length': x, 'Moment': moment})
        df.to_csv(os.path.join(data_dir, 'Length_vs_Moment_Display_Stand.csv'), index=False)

    if station_info_df is not None:
        station_info_df.to_csv(os.path.join(data_dir, 'Station Information.csv'), index=False)

    if shear_and_moment_df is not None:
        shear_and_moment_df.to_csv(os.path.join(data_dir, 'Shear_and_Moment_Display_Stand.csv'), index=False)


def build_all(data_dir: str = DEFAULT_DATA_DIR,
              inner_file: str = DEFAULT_INNER,
              outer_file: str = DEFAULT_OUTER,
              concrete_density: float = None):
    """High-level function that loads data, computes volumes, mass, shear and moment.
    Returns a dict of computed objects useful for downstream code or testing.
    """
    if concrete_density is None:
        concrete_density = cv.concrete_density

    x_in, y_in, z_in, x_out, y_out, z_out = load_hull_points(data_dir, inner_file, outer_file)

    inner = compute_hull_station_volumes(x_in, y_in, z_in)
    outer = compute_hull_station_volumes(x_out, y_out, z_out)

    stat_vol, stat_mass, canoe_m = compute_canoe_mass(inner['vol'], outer['vol'], concrete_density=concrete_density)

    # For now, compute shear and moment using simplified routine
    x, shear, moment, stands = compute_shear_and_moment(stat_mass, outer['station'], x_out)

    results = {
        'inner': inner,
        'outer': outer,
        'stat_vol': stat_vol,
        'stat_mass': stat_mass,
        'canoe_mass': canoe_m,
        'x': x,
        'shear': shear,
        'moment': moment,
        'stands': stands,
    }

    return results


if __name__ == '__main__':
    res = build_all()
