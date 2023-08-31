import json
import numpy as np
from glob import glob


def reader(filename):
    with open(filename) as f:
        info = json.load(f)
    rms_bbs = np.asarray(info['boxes'])
    fp_eds = info['edges']
    rms_type = info['room_type']
    eds_to_rms = info['ed_rm']
    s_r = 0
    for rmk in range(len(rms_type)):
        if rms_type[rmk] != 17:
            s_r = s_r + 1
    rms_bbs = np.array(rms_bbs) / 256.0
    fp_eds = np.array(fp_eds) / 256.0
    fp_eds = fp_eds[:, :4]
    tl = np.min(rms_bbs[:, :2], 0)
    br = np.max(rms_bbs[:, 2:], 0)
    shift = (tl + br) / 2.0 - 0.5
    rms_bbs[:, :2] -= shift
    rms_bbs[:, 2:] -= shift
    fp_eds[:, :2] -= shift
    fp_eds[:, 2:] -= shift
    tl -= shift
    br -= shift
    eds_to_rms_tmp = []

    for l in range(len(eds_to_rms)):
        eds_to_rms_tmp.append([eds_to_rms[l][0]])

    return rms_type, fp_eds, rms_bbs, eds_to_rms, eds_to_rms_tmp


file_list = glob('/home/akmal/APIIT/FYP Code/Housegan-data-reader/sample_out/*')
# with open('file_list.txt','r') as f:
#     lines = f.readlines()

lines = file_list

out_size = 64
length_edges = []
subgraphs = []
for line in lines:
    a = []
    with open(line) as f2:
        rms_type, fp_eds, rms_bbs, eds_to_rms, eds_to_rms_tmp = reader(line)

    eds_to_rms_tmp = []
    for l in range(len(eds_to_rms)):
        eds_to_rms_tmp.append([eds_to_rms[l][0]])

    rms_masks = []
    im_size = 256
    fp_mk = np.zeros((out_size, out_size))
    nodes = rms_type
    for k in range(len(nodes)):
        eds = []
        for l, e_map in enumerate(eds_to_rms_tmp):
            if (k in e_map):
                eds.append(l)
        b = []
        for eds_poly in [eds]:
            length_edges.append((line, np.array([fp_eds[l][:4] for l in eds_poly])))
chk = [x.shape for x in np.array(length_edges)[:, 1]]
idx = [i for i, x in enumerate(chk) if len(x) != 2]
final = np.array(length_edges)[idx][:, 0].tolist()
final = [x.replace('\n', '') for x in final]

import os

for fin in final:
    try:
        os.remove(fin)
    except:
        pass
