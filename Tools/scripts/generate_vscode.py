#!/usr/bin/env python

"""
script to build all of our bootloaders using AP_Bootloader and put the resulting binaries in Tools/bootloaders
"""

import os
import json
import sys

import shutil
import subprocess
import fnmatch

board_pattern = '*'

# allow argument for pattern of boards to build
if len(sys.argv)>1:
    board_pattern = sys.argv[1]

os.environ['PYTHONUNBUFFERED'] = '1'

BOARD_SELECT = "sitl"
if len(sys.argv[1:]) >= 1:
    BOARD_SELECT = sys.argv[1:][0]

print(BOARD_SELECT)

vehicle_builds = ['antennatracker', 'copter', 'heli', 'plane', 'rover', 'sub', 'bootloader','iofirmware','AP_Periph','replay']

def get_board_list():
    '''add boards based on existance of hwdef-bl.dat in subdirectories for ChibiOS'''
    board_list = []
    dirname, dirlist, filenames = next(os.walk('libraries/AP_HAL_ChibiOS/hwdef'))
    for d in dirlist:
        hwdef = os.path.join(dirname, d, 'hwdef-bl.dat')
        if os.path.exists(hwdef):
            board_list.append(d)
    return sorted(list(board_list), key=lambda v: v.lower())

_reconfigure_vscode_tasks = {
    "version": "2.0.0",
    "tasks": [],
    "inputs": [
        {
            "type": "pickString",
            "id": "boardType",
            "description": "Build for which board?",
            "options": [
                "sitl"
            ]
        }
    ]
}

_reconfigure_vscode_project_files = {
    "label": "Reconfigure VSCode Project Files for ArduPilot",
    "type": "shell",
    "linux": {
        "command": "${workspaceRoot}/Tools/scripts/generate_vscode.py"
    },
    "windows": {
        "command": "${workspaceRoot}\\Tools\\scripts\\generate_vscode.py"
    },
    "args": [
        "${input:boardType}"
    ]
}

_reconfigure_vscode_tasks["tasks"].append(_reconfigure_vscode_project_files)

_configure_ardupilot = {
    "label": "Configure ArduPilot (Debug)",
    "type": "shell",
    "windows": {
        "command": "${workspaceFolder}\\waf"
    },
    "linux": {
        "command": "${workspaceFolder}/waf"
    },
    "args": [
        "configure",
        "--debug",
    ],
}
_configure_ardupilot["args"].append("--board={}".format(BOARD_SELECT))
_reconfigure_vscode_tasks["tasks"].append(_configure_ardupilot)


def configure_project_vehicle_builds(vehicle):
    _build_vehicle_config = {
        "label": "Build ArduPilot (Debug)",
        "type": "shell",
        "dependsOn": "Configure ArduPilot (Debug)",
        "windows": {
            "command": "${workspaceFolder}\\waf"
        },
        "linux": {
            "command": "${workspaceFolder}/waf"
        },
        "args": [
        ],
        "group": "build"
    }
    _build_vehicle_config["label"] = "Build ArduPilot ({}) (Debug)".format(vehicle.capitalize())
    _build_vehicle_config["args"].append(vehicle)
    return _build_vehicle_config

for v in sorted(list(vehicle_builds), key=lambda v: v.lower()):
    _reconfigure_vscode_tasks["tasks"].append(configure_project_vehicle_builds(v))


_reconfigure_vscode_launch = {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Reconfigure VSCode Project Files",
            "type": "python",
            "request": "launch",
            "windows": {
                "program": "${workspaceRoot}\\Tools\\scripts\\generate_vscode.py"
            },
            "linux": {
                "program": "${workspaceRoot}/Tools/scripts/generate_vscode.py"
            },
            "args": [
                "${input:boardType}"
            ],
            "presentation": {
                "hidden": False,
                "group": "999_ReconfigureProjectFiles",
                "order": 999
            }
        }
    ],
    "inputs": [
        {
            "type":"pickString",
            "id": "boardType",
            "description": "Build for which board?",
            "options": [
                "sitl"
            ]
        }
    ]
}

print(get_board_list())
for vscode_task_input in _reconfigure_vscode_tasks["inputs"]:
    if vscode_task_input["id"] == "boardType":
        for board in get_board_list():
            vscode_task_input["options"].append(board)

for vscode_launch_input in _reconfigure_vscode_launch["inputs"]:
    if vscode_launch_input["id"] == "boardType":
        for board in get_board_list():
            vscode_launch_input["options"].append(board)

with open(os.path.join(".vscode", "tasks.json"), 'w') as tasks:
    tasks.write(json.dumps(_reconfigure_vscode_tasks, indent=4))

with open(os.path.join(".vscode", "launch.json"), "w") as launch:
    launch.write(json.dumps(_reconfigure_vscode_launch, indent=4))