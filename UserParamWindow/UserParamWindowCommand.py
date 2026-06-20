import json
import traceback

import adsk.core
import adsk.fusion

handlers = []

PALETTE_WIDTH = 520
PALETTE_HEIGHT = 720
PALETTE_HTML = './palette.html'
PALETTE_CHROME_HEIGHT = 36
PALETTE_MIN_WIDTH = 300
PALETTE_MIN_HEIGHT = 480


def _get_app_context():
    app = adsk.core.Application.get()
    ui = app.userInterface
    design = adsk.fusion.Design.cast(app.activeProduct)
    units_manager = design.fusionUnitsManager if design else None
    return {
        'app': app,
        'ui': ui,
        'design': design,
        'units_manager': units_manager,
    }


def _get_design():
    app_objects = _get_app_context()
    return app_objects['design'], app_objects


def _is_text_param(param):
    value_type = param.valueType
    text_type = getattr(
        adsk.fusion.ParameterValueTypes,
        'TextParameterValueType',
        getattr(adsk.fusion.ParameterValueTypes, 'TextValueType', None),
    )
    if text_type is not None:
        return value_type == text_type
    # Fallback when enum members differ across Fusion versions.
    return value_type == 1 or param.unit == 'Text'


def _value_type_name(param):
    if _is_text_param(param):
        return 'text'
    return 'numeric'


def _validation_units(param, units_manager):
    if param.unit:
        return param.unit
    return units_manager.defaultLengthUnits


def _serialize_params(design):
    params = []
    for param in design.userParameters:
        params.append({
            'name': param.name,
            'expression': param.expression,
            'unit': param.unit,
            'comment': param.comment,
            'valueType': _value_type_name(param),
            'isDeletable': param.isDeletable,
            'isFavorite': param.isFavorite,
        })
    return params


def _ensure_palette_minimum_size(palette):
    if palette.height < PALETTE_MIN_HEIGHT:
        palette.height = PALETTE_MIN_HEIGHT
    palette.setMinimumSize(PALETTE_MIN_WIDTH, PALETTE_MIN_HEIGHT)


def _commit_palette_content_height(palette, content_height):
    if content_height <= 0:
        return

    target_height = max(
        int(content_height) + PALETTE_CHROME_HEIGHT,
        PALETTE_MIN_HEIGHT,
        palette.height,
    )
    if target_height > palette.height:
        palette.height = target_height


def _load_params_into_palette(palette):
    design, app_objects = _get_design()
    if not design:
        payload = {'params': [], 'error': 'Open a parametric design to manage user parameters.'}
    else:
        payload = {'params': _serialize_params(design), 'error': ''}

    palette.sendInfoToHTML('loadParams', json.dumps(payload))


def _apply_params(changes):
    design, app_objects = _get_design()
    if not design:
        return {'ok': False, 'errors': ['No active parametric design.'], 'applied': []}

    units_manager = app_objects['units_manager']
    errors = []
    applied = []

    for change in changes:
        name = change.get('name', '')
        expression = change.get('expression', '')
        param = design.userParameters.itemByName(name)

        if not param:
            errors.append('{}: parameter not found'.format(name))
            continue

        try:
            if _is_text_param(param):
                if expression.startswith("'") and expression.endswith("'"):
                    param.expression = expression
                else:
                    param.textValue = expression
            else:
                units = _validation_units(param, units_manager)
                if units_manager.isValidExpression(expression, units):
                    param.expression = expression
                else:
                    errors.append('{}: invalid expression "{}"'.format(name, expression))
                    continue
            applied.append(name)
        except Exception:
            errors.append('{}: failed to set expression'.format(name))

    return {'ok': len(errors) == 0, 'errors': errors, 'applied': applied}


def _add_param(data):
    design, app_objects = _get_design()
    if not design:
        return {'ok': False, 'error': 'No active parametric design.'}

    name = data.get('name', '').strip()
    expression = data.get('expression', '').strip()
    units = data.get('unit', 'mm').strip()
    comment = data.get('comment', '').strip()

    if not name:
        return {'ok': False, 'error': 'Parameter name is required.'}

    if design.userParameters.itemByName(name):
        return {'ok': False, 'error': 'A parameter named "{}" already exists.'.format(name)}

    units_manager = app_objects['units_manager']

    try:
        if units == 'Text':
            if not expression:
                expression = "''"
            elif not (expression.startswith("'") and expression.endswith("'")):
                expression = "'{}'".format(expression.replace("'", "\\'"))
            value_input = adsk.core.ValueInput.createByString(expression)
        else:
            validation_units = units if units else units_manager.defaultLengthUnits
            if not expression:
                expression = '0'
            if not units_manager.isValidExpression(expression, validation_units):
                return {'ok': False, 'error': 'Invalid expression "{}" for unit "{}".'.format(expression, units)}
            value_input = adsk.core.ValueInput.createByString(expression)

        new_param = design.userParameters.add(name, value_input, units, comment)
        if not new_param:
            return {'ok': False, 'error': 'Fusion could not create parameter "{}".'.format(name)}

        return {
            'ok': True,
            'param': {
                'name': new_param.name,
                'expression': new_param.expression,
                'unit': new_param.unit,
                'comment': new_param.comment,
                'valueType': _value_type_name(new_param),
                'isDeletable': new_param.isDeletable,
                'isFavorite': new_param.isFavorite,
            },
        }
    except Exception:
        return {'ok': False, 'error': 'Failed to create parameter: {}'.format(traceback.format_exc())}


def _delete_param(name):
    design, _ = _get_design()
    if not design:
        return {'ok': False, 'error': 'No active parametric design.'}

    param = design.userParameters.itemByName(name)
    if not param:
        return {'ok': False, 'error': 'Parameter "{}" not found.'.format(name)}

    if not param.isDeletable:
        return {'ok': False, 'error': 'Parameter "{}" cannot be deleted (it has dependents).'.format(name)}

    try:
        param.deleteMe()
        return {'ok': True, 'name': name}
    except Exception:
        return {'ok': False, 'error': 'Failed to delete parameter "{}".'.format(name)}


class PaletteHTMLEventHandler(adsk.core.HTMLEventHandler):
    def __init__(self, command_object):
        super().__init__()
        self._command = command_object

    def notify(self, args):
        html_args = adsk.core.HTMLEventArgs.cast(args)
        action = html_args.action

        try:
            if action == 'paletteReady':
                palette = self._command.get_palette()
                if palette and palette.isValid:
                    _ensure_palette_minimum_size(palette)
                    _load_params_into_palette(palette)
                html_args.returnData = json.dumps({'ok': True})
                return

            if action == 'commitPaletteSize':
                palette = self._command.get_palette()
                data = json.loads(html_args.data) if html_args.data else {}
                if palette and palette.isValid:
                    _commit_palette_content_height(
                        palette,
                        data.get('contentHeight', 0),
                    )
                html_args.returnData = json.dumps({'ok': True})
                return

            if action == 'refreshParams':
                palette = self._command.get_palette()
                if palette and palette.isValid:
                    _load_params_into_palette(palette)
                html_args.returnData = json.dumps({'ok': True})
                return

            if action == 'applyParams':
                changes = json.loads(html_args.data) if html_args.data else []
                result = _apply_params(changes)
                if result['ok'] or result['applied']:
                    palette = self._command.get_palette()
                    if palette and palette.isValid:
                        _load_params_into_palette(palette)
                html_args.returnData = json.dumps(result)
                return

            if action == 'addParam':
                data = json.loads(html_args.data) if html_args.data else {}
                result = _add_param(data)
                if result.get('ok'):
                    palette = self._command.get_palette()
                    if palette and palette.isValid:
                        _load_params_into_palette(palette)
                html_args.returnData = json.dumps(result)
                return

            if action == 'deleteParam':
                data = json.loads(html_args.data) if html_args.data else {}
                result = _delete_param(data.get('name', ''))
                if result.get('ok'):
                    palette = self._command.get_palette()
                    if palette and palette.isValid:
                        _load_params_into_palette(palette)
                html_args.returnData = json.dumps(result)
                return

            html_args.returnData = json.dumps({'ok': False, 'error': 'Unknown action: {}'.format(action)})
        except Exception:
            html_args.returnData = json.dumps({'ok': False, 'error': traceback.format_exc()})


class PaletteCloseHandler(adsk.core.UserInterfaceGeneralEventHandler):
    def notify(self, args):
        pass


class ShowPaletteExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_object):
        super().__init__()
        self._command = command_object

    def notify(self, args):
        self._command.show_palette()


class ShowPaletteCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_object):
        super().__init__()
        self._command = command_object

    def notify(self, args):
        on_execute = ShowPaletteExecuteHandler(self._command)
        args.command.execute.add(on_execute)
        handlers.append(on_execute)


class UserParamWindowCommand:
    def __init__(self, cmd_def, debug):
        self.cmd_name = cmd_def['cmd_name']
        self.cmd_description = cmd_def['cmd_description']
        self.cmd_resources = cmd_def['cmd_resources']
        self.cmd_id = cmd_def['cmd_id']
        self.workspace = cmd_def['workspace']
        self.toolbar_panel_id = cmd_def['toolbar_panel_id']
        self.palette_id = cmd_def['palette_id']
        self.palette_name = cmd_def['palette_name']
        self.palette_html = cmd_def['palette_html_file_url']
        self.debug = debug
        self._palette = None

    def get_palette(self):
        app = adsk.core.Application.get()
        ui = app.userInterface
        palette = ui.palettes.itemById(self.palette_id)
        if palette and palette.isValid:
            self._palette = palette
            return palette
        return None

    def show_palette(self):
        app = adsk.core.Application.get()
        ui = app.userInterface

        try:
            palette = ui.palettes.itemById(self.palette_id)
            is_new_palette = not palette or not palette.isValid

            if is_new_palette:
                palette = ui.palettes.add(
                    self.palette_id,
                    self.palette_name,
                    PALETTE_HTML,
                    False,
                    True,
                    True,
                    PALETTE_WIDTH,
                    PALETTE_HEIGHT,
                    True,
                )

                palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateFloating
                palette.dockingOption = adsk.core.PaletteDockingOptions.PaletteDockOptionsToVerticalAndHorizontal
                palette.setPosition(120, 120)
                palette.width = PALETTE_WIDTH
                palette.height = PALETTE_HEIGHT
                _ensure_palette_minimum_size(palette)

                on_html = PaletteHTMLEventHandler(self)
                palette.incomingFromHTML.add(on_html)
                handlers.append(on_html)

                on_close = PaletteCloseHandler()
                palette.closed.add(on_close)
                handlers.append(on_close)
            else:
                _ensure_palette_minimum_size(palette)
                if palette.height < PALETTE_HEIGHT:
                    palette.height = PALETTE_HEIGHT

            palette.isVisible = True
            self._palette = palette

            if not is_new_palette:
                _load_params_into_palette(palette)
        except Exception:
            ui.messageBox('Failed to open palette:\n{}'.format(traceback.format_exc()))

    def on_run(self):
        app = adsk.core.Application.get()
        ui = app.userInterface

        try:
            from .Fusion360Utilities.Fusion360CommandBase import (
                get_controls,
                command_definition_by_id,
            )

            controls = get_controls(False, self.workspace, self.toolbar_panel_id, ui)
            if controls.itemById(self.cmd_id):
                return

            cmd_def = ui.commandDefinitions.itemById(self.cmd_id)
            if not cmd_def:
                cmd_def = ui.commandDefinitions.addButtonDefinition(
                    self.cmd_id,
                    self.cmd_name,
                    self.cmd_description,
                    self.cmd_resources,
                )
                on_created = ShowPaletteCreatedHandler(self)
                cmd_def.commandCreated.add(on_created)
                handlers.append(on_created)

            controls.addCommand(cmd_def)
        except Exception:
            ui.messageBox('Add-in start failed:\n{}'.format(traceback.format_exc()))

    def on_stop(self):
        app = adsk.core.Application.get()
        ui = app.userInterface

        try:
            from .Fusion360Utilities.Fusion360CommandBase import (
                get_controls,
                destroy_object,
                command_definition_by_id,
            )

            palette = ui.palettes.itemById(self.palette_id)
            if palette:
                destroy_object(palette)

            controls = get_controls(False, self.workspace, self.toolbar_panel_id, ui)
            cmd_control = controls.itemById(self.cmd_id)
            if cmd_control:
                destroy_object(cmd_control)

            cmd_def = command_definition_by_id(self.cmd_id, ui)
            if cmd_def:
                destroy_object(cmd_def)
        except Exception:
            if ui:
                ui.messageBox('Add-in stop failed:\n{}'.format(traceback.format_exc()))