# Floating palette for managing Fusion 360 user parameters.
# Forked from tapnair/ParamEdit — palette UI + create/delete support.

from .UserParamWindowCommand import UserParamWindowCommand

commands = []

cmd = {
    'cmd_name': 'User Parameters',
    'cmd_description': 'Open a floating window to manage user parameters',
    'cmd_resources': './resources',
    'cmd_id': 'cmdID_UserParamWindow',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_ids': [
        'SolidModifyPanel',
    ],
    'utilities_toolbar_panel': {
        'panel_id': 'UserParamWindowPanel',
        'panel_name': 'User Parameters',
    },
    'palette_id': 'UserParamWindow_Palette_v8',
    'palette_name': 'User Parameters',
    'palette_html_file_url': 'palette.html',
    'class': UserParamWindowCommand,
}

commands.append(UserParamWindowCommand(cmd, debug=False))


def run(context):
    for command in commands:
        command.on_run()


def stop(context):
    for command in commands:
        command.on_stop()