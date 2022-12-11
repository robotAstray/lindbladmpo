# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
Definitions of the topologies for the example research projects.
"""
from typing import Tuple
import matplotlib.pyplot as plt
import numpy as np


coupling_maps = {}
"""A dictionary with coupling maps (lists of bonds) for different qubit configurations and topologies."""

qubit_coordinates = {}
"""A dictionary with coordinates lists positioning qubits in the plane for plotting configurations,
corresponding to those defined in the `coupling_maps` dictionary."""

h_z_patterns = {}
"""A dictionary with a pattern of the relative strength of h_z terms of a qubit configuration."""


def _create_ring_A(n_qubits: int, i_offset: int = 0) -> Tuple[list, list, list]:
    """Generate a ring topology of type A - indicating a ladder-like ordering of the qubits.

    Args:
            n_qubits: The number of qubits composing the ring.
            i_offset: The index offset of the first qubit.
    Returns:
            A tuple with the coupling map, qubit coordinates in the plane (with the first qubit placed
                    at [1, 1]), and a 0-1 pattern array with alternating values for neighboring qubits.
    """
    c_map = []
    q_coordinates = []
    h_z_pat = []
    c_map.extend([[i_offset, i_offset + 1], [i_offset, i_offset + 2]])
    for i in range(i_offset + 1, i_offset + n_qubits - 2):
        c_map.append([i, i + 2])
    c_map.append([i_offset + n_qubits - 2, i_offset + n_qubits - 1])
    h_z_pat.append(0)
    q_coordinates.append([1, 1])
    h_z_ = 1
    for i in range(1, n_qubits - 2, 2):
        h_z_pat.extend([h_z_, h_z_])
        q_coordinates.extend([[2 + int(i / 2), 0], [2 + int(i / 2), 2]])
        h_z_ = 0 if h_z_ == 1 else 1
    h_z_pat.append(h_z_)
    q_coordinates.append([1 + int(n_qubits / 2), 1])
    return c_map, q_coordinates, h_z_pat


# Add a 1D chain topology for an odd number of qubits (3 to 61 qubits).
# This chain topology entries have keys of the form 'N.chain.M' where N is the number of qubits,
# and M indicates that the middle qubit has h_z amplitude 0.
for n_qubits in range(3, 63, 2):
    c_map = []
    q_coordinates = []
    h_z_pat = []
    for i in range(n_qubits - 1):
        c_map.append([i, i + 1])
    driven_qubit_is_odd = 1 if (n_qubits - 1) % 4 != 0 else 0
    for i in range(n_qubits):
        q_coordinates.append([0, i])
        h_z_pat.append(0 if i % 2 == driven_qubit_is_odd else 1)
    s_key = f"{n_qubits}.chain.M"
    coupling_maps[s_key] = c_map
    qubit_coordinates[s_key] = q_coordinates
    h_z_patterns[s_key] = h_z_pat


# Add a 1D chain topology for all numbers of qubits (3 to 61 qubits).
# The chain topology entries have keys of the form 'N.chain.E' where N is the number of qubits,
# and E indicates that the left edge qubit (indexed 0) has h_z amplitude 0.
for n_qubits in range(2, 63):
    c_map = []
    q_coordinates = []
    h_z_pat = []
    for i in range(n_qubits - 1):
        c_map.append([i, i + 1])
    for i in range(n_qubits):
        q_coordinates.append([0, i])
        h_z_pat.append(0 if i % 2 == 0 else 1)
    s_key = f"{n_qubits}.chain.E"
    coupling_maps[s_key] = c_map
    qubit_coordinates[s_key] = q_coordinates
    h_z_patterns[s_key] = h_z_pat


# We add ring topologies for 4 to 62 qubits, with keys in the form 'N.ring.A' where N is the number
# of qubits, and A is the mpo_ordering - indicating a ladder-like ordering of the qubits.
for n_qubits in range(4, 64, 2):
    c_map, q_coordinates, h_z_pat = _create_ring_A(n_qubits)
    s_key = f"{n_qubits}.ring.A"
    coupling_maps[s_key] = c_map
    qubit_coordinates[s_key] = q_coordinates
    h_z_patterns[s_key] = h_z_pat


# We add ring topologies for 4 to 62 qubits, with keys in the form 'N.ring.B' where N is the number of
# qubits, and B is the mpo_ordering - indicating qubits ordered to have one large jump at the last one.
for n_qubits in range(4, 64, 2):
    c_map = []
    q_coordinates = []
    h_z_pat = []
    for i in range(n_qubits - 1):
        c_map.append([i, i + 1])
    c_map.append([n_qubits - 1, 0])
    for i in range(n_qubits):
        h_z_pat.append(0 if i % 2 == 0 else 1)
    q_coordinates.append([1, 1])
    N_by_2 = int(n_qubits / 2)
    for i in range(2, N_by_2 + 1):
        q_coordinates.append([i, 0])
    q_coordinates.append([N_by_2 + 1, 1])
    for i in range(N_by_2, 1, -1):
        q_coordinates.append([i, 2])
    s_key = f"{n_qubits}.ring.B"
    coupling_maps[s_key] = c_map
    qubit_coordinates[s_key] = q_coordinates
    h_z_patterns[s_key] = h_z_pat


# We add plaquette topologies for 6 to 62 qubits, with keys in the form 'N.plaquette.A' where N is
# the number of qubits, and A is the mpo_ordering - indicating a ladder-like ordering of the qubits.
for n_qubits in range(6, 64, 2):
    c_map1, q_coordinates1, h_z_pat1 = _create_ring_A(n_qubits - 2, 1)
    c_map = [[0, 1]]
    c_map.extend(c_map1)
    c_map.append([n_qubits - 2, n_qubits - 1])
    q_coordinates = [[0, 1]]
    q_coordinates.extend(q_coordinates1)
    q_coord_end = q_coordinates1[-1]
    q_coordinates.append([q_coord_end[0] + 1, q_coord_end[1]])
    h_z_pat = [0]
    for h_z in h_z_pat1:
        h_z_pat.append(1 if h_z == 0 else 0)
    h_z_pat.append(0)
    s_key = f"{n_qubits}.plaquette.A"
    coupling_maps[s_key] = c_map
    qubit_coordinates[s_key] = q_coordinates
    h_z_patterns[s_key] = h_z_pat


# We add a few plaquette topologies, with keys in the form 'N.plaquette.B' where N is the number of
# qubits, and B is the mpo_ordering - indicating qubits ordered to have one large jump at the last one.

coupling_maps["10.plaquette.B"] = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],
    [5, 6],
    [5, 7],
    [7, 8],
    [8, 9],
    [9, 1],
]
qubit_coordinates["10.plaquette.B"] = [
    [0, 1],
    [1, 1],
    [2, 0],
    [3, 0],
    [4, 0],
    [5, 1],
    [6, 1],
    [4, 2],
    [3, 2],
    [2, 2],
]
h_z_patterns["10.plaquette.B"] = [0, 1, 0, 1, 0, 1, 0, 0, 1, 0]

coupling_maps["12.plaquette.B"] = [
    [0, 1],
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],
    [5, 6],
    [6, 7],
    [6, 8],
    [8, 9],
    [9, 10],
    [10, 11],
    [11, 1],
]
qubit_coordinates["12.plaquette.B"] = [
    [0, 1],
    [1, 1],
    [2, 0],
    [3, 0],
    [4, 0],
    [5, 0],
    [6, 1],
    [7, 1],
    [5, 2],
    [4, 2],
    [3, 2],
    [2, 2],
]
h_z_patterns["12.plaquette.B"] = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0]


# Below are the connectivity map and qubit outline of the IBM Quantum Falcon devices

coupling_maps["27.falcon"] = [
    [0, 1],
    [1, 2],
    [1, 4],
    [2, 3],
    [3, 5],
    [4, 7],
    [5, 8],
    [6, 7],
    [7, 10],
    [8, 9],
    [8, 11],
    [10, 12],
    [11, 14],
    [12, 13],
    [12, 15],
    [13, 14],
    [14, 16],
    [15, 18],
    [16, 19],
    [17, 18],
    [18, 21],
    [19, 20],
    [19, 22],
    [21, 23],
    [22, 25],
    [23, 24],
    [24, 25],
    [25, 26],
]
qubit_coordinates["27.falcon"] = [
    [1, 0],
    [1, 1],
    [2, 1],
    [3, 1],
    [1, 2],
    [3, 2],
    [0, 3],
    [1, 3],
    [3, 3],
    [4, 3],
    [1, 4],
    [3, 4],
    [1, 5],
    [2, 5],
    [3, 5],
    [1, 6],
    [3, 6],
    [0, 7],
    [1, 7],
    [3, 7],
    [4, 7],
    [1, 8],
    [3, 8],
    [1, 9],
    [2, 9],
    [3, 9],
    [3, 10],
]
h_z_patterns["27.falcon"] = [0] * 27


coupling_maps["7.falcon"] = [
    [0, 1],
    [1, 2],
    [1, 3],
    [3, 5],
    [4, 5],
    [5, 6],
]
qubit_coordinates["7.falcon"] = [
    [1, 0],
    [1, 1],
    [1, 2],
    [2, 1],
    [3, 0],
    [3, 1],
    [3, 2],
]
h_z_patterns["7.falcon"] = [0] * 7


coupling_maps["127.eagle"] = [
    [0, 1],
    [0, 14],
    [1, 0],
    [1, 2],
    [2, 1],
    [2, 3],
    [3, 2],
    [3, 4],
    [4, 3],
    [4, 5],
    [4, 15],
    [5, 4],
    [5, 6],
    [6, 5],
    [6, 7],
    [7, 6],
    [7, 8],
    [8, 7],
    [8, 16],
    [9, 10],
    [10, 9],
    [10, 11],
    [11, 10],
    [11, 12],
    [12, 11],
    [12, 13],
    [12, 17],
    [13, 12],
    [14, 0],
    [14, 18],
    [15, 4],
    [15, 22],
    [16, 8],
    [16, 26],
    [17, 12],
    [17, 30],
    [18, 14],
    [18, 19],
    [19, 18],
    [19, 20],
    [20, 19],
    [20, 21],
    [20, 33],
    [21, 20],
    [21, 22],
    [22, 15],
    [22, 21],
    [22, 23],
    [23, 22],
    [23, 24],
    [24, 23],
    [24, 25],
    [24, 34],
    [25, 24],
    [25, 26],
    [26, 16],
    [26, 25],
    [26, 27],
    [27, 26],
    [27, 28],
    [28, 27],
    [28, 29],
    [28, 35],
    [29, 28],
    [29, 30],
    [30, 17],
    [30, 29],
    [30, 31],
    [31, 30],
    [31, 32],
    [32, 31],
    [32, 36],
    [33, 20],
    [33, 39],
    [34, 24],
    [34, 43],
    [35, 28],
    [35, 47],
    [36, 32],
    [36, 51],
    [37, 38],
    [37, 52],
    [38, 37],
    [38, 39],
    [39, 33],
    [39, 38],
    [39, 40],
    [40, 39],
    [40, 41],
    [41, 40],
    [41, 42],
    [41, 53],
    [42, 41],
    [42, 43],
    [43, 34],
    [43, 42],
    [43, 44],
    [44, 43],
    [44, 45],
    [45, 44],
    [45, 46],
    [45, 54],
    [46, 45],
    [46, 47],
    [47, 35],
    [47, 46],
    [47, 48],
    [48, 47],
    [48, 49],
    [49, 48],
    [49, 50],
    [49, 55],
    [50, 49],
    [50, 51],
    [51, 36],
    [51, 50],
    [52, 37],
    [52, 56],
    [53, 41],
    [53, 60],
    [54, 45],
    [54, 64],
    [55, 49],
    [55, 68],
    [56, 52],
    [56, 57],
    [57, 56],
    [57, 58],
    [58, 57],
    [58, 59],
    [58, 71],
    [59, 58],
    [59, 60],
    [60, 53],
    [60, 59],
    [60, 61],
    [61, 60],
    [61, 62],
    [62, 61],
    [62, 63],
    [62, 72],
    [63, 62],
    [63, 64],
    [64, 54],
    [64, 63],
    [64, 65],
    [65, 64],
    [65, 66],
    [66, 65],
    [66, 67],
    [66, 73],
    [67, 66],
    [67, 68],
    [68, 55],
    [68, 67],
    [68, 69],
    [69, 68],
    [69, 70],
    [70, 69],
    [70, 74],
    [71, 58],
    [71, 77],
    [72, 62],
    [72, 81],
    [73, 66],
    [73, 85],
    [74, 70],
    [74, 89],
    [75, 76],
    [75, 90],
    [76, 75],
    [76, 77],
    [77, 71],
    [77, 76],
    [77, 78],
    [78, 77],
    [78, 79],
    [79, 78],
    [79, 80],
    [79, 91],
    [80, 79],
    [80, 81],
    [81, 72],
    [81, 80],
    [81, 82],
    [82, 81],
    [82, 83],
    [83, 82],
    [83, 84],
    [83, 92],
    [84, 83],
    [84, 85],
    [85, 73],
    [85, 84],
    [85, 86],
    [86, 85],
    [86, 87],
    [87, 86],
    [87, 88],
    [87, 93],
    [88, 87],
    [88, 89],
    [89, 74],
    [89, 88],
    [90, 75],
    [90, 94],
    [91, 79],
    [91, 98],
    [92, 83],
    [92, 102],
    [93, 87],
    [93, 106],
    [94, 90],
    [94, 95],
    [95, 94],
    [95, 96],
    [96, 95],
    [96, 97],
    [96, 109],
    [97, 96],
    [97, 98],
    [98, 91],
    [98, 97],
    [98, 99],
    [99, 98],
    [99, 100],
    [100, 99],
    [100, 101],
    [100, 110],
    [101, 100],
    [101, 102],
    [102, 92],
    [102, 101],
    [102, 103],
    [103, 102],
    [103, 104],
    [104, 103],
    [104, 105],
    [104, 111],
    [105, 104],
    [105, 106],
    [106, 93],
    [106, 105],
    [106, 107],
    [107, 106],
    [107, 108],
    [108, 107],
    [108, 112],
    [109, 96],
    [109, 114],
    [110, 100],
    [110, 118],
    [111, 104],
    [111, 122],
    [112, 108],
    [112, 126],
    [113, 114],
    [114, 109],
    [114, 113],
    [114, 115],
    [115, 114],
    [115, 116],
    [116, 115],
    [116, 117],
    [117, 116],
    [117, 118],
    [118, 110],
    [118, 117],
    [118, 119],
    [119, 118],
    [119, 120],
    [120, 119],
    [120, 121],
    [121, 120],
    [121, 122],
    [122, 111],
    [122, 121],
    [122, 123],
    [123, 122],
    [123, 124],
    [124, 123],
    [124, 125],
    [125, 124],
    [125, 126],
    [126, 112],
    [126, 125],
]
qubit_coordinates["127.eagle"] = [
    [0, 0],
    [0, 1],
    [0, 2],
    [0, 3],
    [0, 4],
    [0, 5],
    [0, 6],
    [0, 7],
    [0, 8],
    [0, 9],
    [0, 10],
    [0, 11],
    [0, 12],
    [0, 13],
    [1, 0],
    [1, 4],
    [1, 8],
    [1, 12],
    [2, 0],
    [2, 1],
    [2, 2],
    [2, 3],
    [2, 4],
    [2, 5],
    [2, 6],
    [2, 7],
    [2, 8],
    [2, 9],
    [2, 10],
    [2, 11],
    [2, 12],
    [2, 13],
    [2, 14],
    [3, 2],
    [3, 6],
    [3, 10],
    [3, 14],
    [4, 0],
    [4, 1],
    [4, 2],
    [4, 3],
    [4, 4],
    [4, 5],
    [4, 6],
    [4, 7],
    [4, 8],
    [4, 9],
    [4, 10],
    [4, 11],
    [4, 12],
    [4, 13],
    [4, 14],
    [5, 0],
    [5, 4],
    [5, 8],
    [5, 12],
    [6, 0],
    [6, 1],
    [6, 2],
    [6, 3],
    [6, 4],
    [6, 5],
    [6, 6],
    [6, 7],
    [6, 8],
    [6, 9],
    [6, 10],
    [6, 11],
    [6, 12],
    [6, 13],
    [6, 14],
    [7, 2],
    [7, 6],
    [7, 10],
    [7, 14],
    [8, 0],
    [8, 1],
    [8, 2],
    [8, 3],
    [8, 4],
    [8, 5],
    [8, 6],
    [8, 7],
    [8, 8],
    [8, 9],
    [8, 10],
    [8, 11],
    [8, 12],
    [8, 13],
    [8, 14],
    [9, 0],
    [9, 4],
    [9, 8],
    [9, 12],
    [10, 0],
    [10, 1],
    [10, 2],
    [10, 3],
    [10, 4],
    [10, 5],
    [10, 6],
    [10, 7],
    [10, 8],
    [10, 9],
    [10, 10],
    [10, 11],
    [10, 12],
    [10, 13],
    [10, 14],
    [11, 2],
    [11, 6],
    [11, 10],
    [11, 14],
    [12, 1],
    [12, 2],
    [12, 3],
    [12, 4],
    [12, 5],
    [12, 6],
    [12, 7],
    [12, 8],
    [12, 9],
    [12, 10],
    [12, 11],
    [12, 12],
    [12, 13],
    [12, 14],
]
h_z_patterns["127.eagle"] = [0] * 127


def plot_topology(
    N: int,
    topology: str,
    s_coupling_map: str,
    b_save_figures: bool,
    s_file_prefix: str,
    b_transpose_plot=False,
    b_alternating_qubits=False,
):
    qubit_color = ["#648fff"] * N
    h_z_pattern = h_z_patterns[s_coupling_map]
    coupling_map = coupling_maps[s_coupling_map]
    qubit_coord = qubit_coordinates[s_coupling_map]
    if b_alternating_qubits:
        s_alternating = ".alternating"
        for i in np.nonzero(h_z_pattern)[0]:
            qubit_color[i] = "#ff6f64"
    else:
        s_alternating = ""

    if topology == "plaquette" or topology == "ring":
        figsize = (4, 7)
    else:
        figsize = (8, 2)
    q_coord = []
    if b_transpose_plot:
        figsize = (figsize[1], figsize[0])
        for ll in qubit_coord:
            q_coord.append([ll[1], ll[0]])
    else:
        q_coord = qubit_coord

    try:
        from qiskit.visualization.gate_map import plot_coupling_map

        fig = plot_coupling_map(
            num_qubits=N,
            qubit_coordinates=q_coord,
            coupling_map=coupling_map,
            figsize=figsize,
            qubit_color=qubit_color,
        )
        if b_save_figures:
            plt.savefig(s_file_prefix + s_alternating + ".png")
        plt.draw()
        plt.pause(0.1)
        plt.show(block=False)
    except Exception as e:
        print(str(e))
