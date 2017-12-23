import os
from itertools import groupby
import pandas as pd

def readFile(filename):
    file = open(os.path.join(filename), 'r')
    script = file.readlines()
    file.close()
    
    return script


def cleanSplitScript(script):
    skipwords = ['SMASH CUT TO']
    dialogues = [s.replace("\t", "").replace("\r", "").replace("\n", " ").strip() for s in script]
    dialogues = [x for x in dialogues if x]
    dialogues = [x[0] for x in groupby(dialogues)]
    dialogues = [x for x in dialogues if not any(w in x for w in skipwords)]
    
    return dialogues

def catScenes(split_movie):
    i = 0
    scene_groups = []
    scene = []
    contains_scenes = False
    for pos,d in enumerate(split_movie):
        if d != 'CUT TO:':
            scene.append(d)
        else:
            contains_scenes = True
            i += 1
            scene_obj = {}
            scene_obj['id'] = i
            scene_obj['scene'] = scene
            scene_groups.append(scene_obj)
            scene = []

    if not scene_groups:
        scene_obj = {}
        scene_obj['id'] = 1
        scene_obj['scene'] = scene
        scene_groups.append(scene_obj)

    return scene_groups

def catSceneDialogs(scene_groups):
    for g in scene_groups:
        g['scene_proc'] = []
        char = ""
        for d in g['scene']:
            if d.isupper():
                char = d
            else:
                g['scene_proc'].append({'speaker':char, 'dialogue':d})

    scene_proc = [{'id':x['id'], 'scene':x['scene_proc']} for x in scene_groups]

    return scene_proc

def flatProcSceneDialogs(scene_proc):
    scene_proc_flat = []
    for sp in scene_proc:
        for scn in sp['scene']:
            elem = []
            elem.append(sp['id'])
            elem.append(scn['speaker'])
            elem.append(scn['dialogue'])
            scene_proc_flat.append(elem)

    data = pd.DataFrame(scene_proc_flat, columns = ['id', 'speaker', 'dialogue'])
    return data

def getCharDialog(allDialogs, charName):
    return allDialogs[allDialogs['speaker'] == charName]

def concatDFColumn(df, columnname):
    v_data_grouped = df.groupby('speaker').apply(lambda x: ' '.join(x[columnname]))
    v_data_grouped = v_data_grouped.reset_index(name=columnname)
    v_dialogue = v_data_grouped[columnname]
    return v_dialogue[0]

