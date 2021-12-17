from argparse import ArgumentParser

parser = ArgumentParser(description='DScript Compiler.')

# Add the arguments.
parser.add_argument('--ignore-comments', dest='ignore_comments', action='store_false', required=False)
parser.add_argument('-o', '--out', dest='output', required=True)
parser.add_argument('-i', '--in', dest='infile', required=True)
parser.add_argument('-ignore-undefined-variables', required=False, dest='ignore_undefined_variable', action='store_true')

compiler_args = parser.parse_args()

lines = open(compiler_args.infile, 'r').read().splitlines() # Get each line.

finishing_lines = []
variables = []
to_import = ['discord']
from_imports = [{'from': 'discord.ext', 'import': 'commands'}]
args = []
name = 'untitled_command'
decorators = []

lines_written = 0

def com(command, ln) -> str:
    return '# {}'.format(' '.join(x for x in command['args'])) if compiler_args.ignore_comments else ''

def c(command, ln):
    return com(command, ln)

def getuser(command, ln) -> str:
    u_var, u_var_exists = _get_and_check_if_var(command['args'][0][1:])
    ref = 'int({})'.format(u_var['name'] if u_var_exists else ('"' + command['args'][0] + '"'))

    return '{}=self.client.get_user({})'.format(command['args'][1], ref)        


def ban(command, ln) -> str:
    if len(command['args']) < 1:
        SyntaxError('Line {}\nRequired a user variable.'.format(ln))
    # Check if variable exists
    _variable, _is_variable = _get_and_check_if_var(command['args'][0][1:])
    if not _is_variable and not compiler_args.ignore_undefined_variable:
        raise SyntaxError('Line {}\n"{}" does not exist.'.format(
            ln, command['args'][0][1:]))
    # Perform another check to see if a reason has been supplied.
    reason = None
    if len(command['args']) >= 2:
        reason = '"' + ' '.join(x for x in command['args'][1:]) + '"'
        vi = _get_and_check_if_var(command['args'][1][1:])
        if vi[1]:
            reason = "str(" + vi[0]['name'] + ")"
            if len(command['args']) >= 3:
                for _a in range(2, len(command['args'])):
                    reason += '+" {}"'.format(command['args']
                                              [_a].replace('"', "'"))

    return 'await {}.ban({})'.format(_variable['name'], ('reason=' + reason) if reason is not None else '')

def kick(command, ln) -> str:
    if len(command['args']) < 1:
        SyntaxError('Line {}\nRequired a user variable.'.format(ln))
    # Check if variable exists
    _variable, _is_variable = _get_and_check_if_var(command['args'][0][1:])
    if not _is_variable:
        if not compiler_args.ignore_undefined_variable:
            raise SyntaxError('Line {}\n"{}" does not exist.'.format(ln, command['args'][0][1:])) 
    # Perform another check to see if a reason has been supplied.
    reason = None
    if len(command['args']) >= 2:
        reason = '"' + ' '.join(x for x in command['args'][1:]) + '"'
        vi = _get_and_check_if_var(command['args'][1][1:])
        if vi[1]:
            reason = "str(" + vi[0]['name'] + ")"
            if len(command['args']) >= 3:
                for _a in range(2, len(command['args'])):
                    reason += '+" {}"'.format(command['args'][_a].replace('"', "'"))
    
    return 'await {}.kick({})'.format(_variable['name'], ('reason=' + reason) if reason is not None else '')

def require(command, ln) -> str:
    if len(command['args']) < 1:
        raise SyntaxError('Line {}\nMust supply at least one argument. aka the decorator value.')
    decorators.append('@'+' '.join(x.replace('"', "'") for x in command['args']))
    return ''

def sendto(command, ln) -> str:
    if len(command['args']) <= 1:
        raise SyntaxError('Line {}\nWhen using "sento" you must supply a channel and then a message/variable to use.'
        .format(ln))
    pos_var_content = command['args'][1]
    channel_var, is_channel_var = _get_and_check_if_var(command['args'][0][1:])
    if not is_channel_var and not compiler_args.ignore_undefined_variable:
        raise Exception('Line {}\n"{}" is not a variable. Maybe you forgot to add the "$"?'
        .format(ln, command['args'][0][1:]))

    cnt_res = '"{}"'.format(' '.join(x.replace('"', "'") for x in command['args'][1:]))
    cnt_var, cnt_is_var = _get_and_check_if_var(pos_var_content[1:]) # Indexing here to remove the '$'
    if cnt_is_var:
        cnt_res = cnt_var['name']
    return '{}.send({})'.format(channel_var['name'], cnt_res)

def log(command, ln) -> str:
    res = '""'
    for _argument in command['args']:
        if _argument[0] == '$':

            _v_check = _get_and_check_if_var(_argument[1:])
            if not _v_check[1] and not compiler_args.ignore_undefined_variable:
                raise SyntaxError(
                    'Line {}\n"{}" is not a variable. Maybe you forgot to add the "$"?'.format(ln, _argument[1:]))
            else:
                res += '+str({})'.format(_v_check[0]['name'])
                continue
        else:
            res += '+" {}"'.format(_argument.replace('"', "'"))
    return 'print({})'.format(res)

def use(command, ln) -> str:
    if len(command['args']) < 1:
        raise SyntaxError('Line {}\n"use" requires a import name/argument to be supplied.'.format(ln))
    if len(command['args']) >= 3:
        if command['args'][1].lower() != 'from':
            raise SyntaxError('Line {}\nExpected keyword "FROM" instead got "{}"'.format(ln, command['args'][1]))
        upper_import = command['args'][0] # from {}
        inner_import = command['args'][2] # import {}
        from_imports.append({'from': upper_import, 'import': inner_import})
    elif len(command['args']) <= 2:
        inner_import = command['args'][0]
        to_import.append(inner_import)
    return ''

def raw(command, ln) -> str:
    if len(command) < 1:
        raise SyntaxError('Line {}\nMust have one or more arguments inside of a "raw" method.'.format(ln))


    return ' '.join([command['args'][i] + ' ' for i in range(len(command['args']))])

def arg(command, ln) -> str:
    if len(command['args']) < 1:
        raise Exception('Line {}\nYou must give the argument a name.')
    args.append('_'.join(x for x in command['args'][0:]))
    variables.append({'name': '_'.join(x for x in command['args'][0:]), 'value': None, 'type': 'arg'})
    return ''

def r(command, ln):
    return raw(command, ln)

def getchannel(command, ln) -> str: 
    by = command['args'][0].lower()
    if len(command['args']) < 3:
        raise Exception('Line {}\nMust specify the value of the channels id OR name. Alongside you must also supply the variable name to store it into..'.format(ln))
    
    ref = ''
    var, is_var = _get_and_check_if_var(command['args'][2:][0][1:])
    if is_var:
        ref = var['name']
    else:
        ref = ('int(' if by == 'id' else '') + ('"') + command['args'][2] + ('"') + (')' if by == 'id' else '')
    
    variables.append({'name': command['args'][1], 'value': ref})
    return '{} = discord.utils.get(ctx.guild.channels, {}={})'.format(command['args'][1], command['args'][0].lower(), ref)

def getexecuter(command, ln) -> str:
    if len(command['args']) < 1:
        raise Exception('Line: {}\nWhen using the get_executer command you must reference the name of the variable to store it into. (New Variable)')
    saving_name = command['args'][0]
    variables.append({'name': saving_name, 'value': 'ctx.author', 'type': 'executer'})
    return '{} = ctx.author'.format(saving_name)

def gex(command, ln) -> str:
    return getexecuter(command, ln)

def _get_and_check_if_var(arg: str) -> tuple:
    is_v = None
    at_in = None
    for vI in range(len(variables)):
        if variables[vI]['name'] == arg:
            is_v = True
            at_in = vI
    if not is_v:
        return None, False
    return variables[at_in], True



def cvv(command, ln) -> str:
    var_info = None
    at_index = None
    for varI in range(len(variables)):
        var = variables[varI]
        if var['name'] == command['args'][0][1:]:
            var_info = var
            at_index = varI
    if var_info is None and not compiler_args.ignore_undefined_variable:
        raise ReferenceError('Line {}\nCannot find variable named "{}".\nReminder: You cannot change the value a variable before you have assigned it.'
        .format(ln, command['args'][0]))
    if len(command['args']) <= 1 and not compiler_args.ignore_undefined_variable:
        raise Exception('Line {}\nCannot reassign variable "{}" with no value.'.format(ln, var_info['name']))

    c = " ".join(x for x in command['args'][1:])
    return f'{var_info["name"]} = {c}'

def send(command, ln) -> str:
    val = '"' + ' '.join(x.replace('"', "'") for x in command['args']) + '"'
    
    if command['args'][0][0] == '$':
        used_var = ''.join(x for x in command['args'][0][1:])
        found_val_var = None
        for variable in variables:
            if variable['name'] == used_var:
                found_val_var = variable['name']
                break
        if found_val_var is None and not compiler_args.ignore_undefined_variable:
            raise ReferenceError('Line {}\nTried to find variable named "{}" but failed.'.format(ln, used_var))
            
        used_var = found_val_var if not None else ("'" + command['joined_args'] + '"')
        val = used_var

    return 'ctx.send({})'.format(val)


def sformat(command, ln) -> str:
    return ' '.join(x for x in command['args'])

def _filter_lines(lines) -> list:
    nll = [] # New line list.
    for line in lines:
        if line.replace(' ', '') == '':
            continue
        nll.append(line)
    return nll
        
def var(command, ln) -> str:
    name = command['args'][0]
    value = ' '.join(x for x in command['args'][1:])
    variables.append({
        'name': name,
        'value': value
    })
    if command['args'][0] == '=':
        raise SyntaxError('Line {}\nCannot use "=" sign when assigning a variable in DSC. (name value value value etc)')

    return '{}={}'.format(name, value)

def get_parts(line: str, line_number: int) -> dict:
    parts = line.split(' ')
    if len(parts) <= 0:
        raise Exception('Line {}\nThere is no function on this line.')
    
    return {
        'command': parts[0].lower(),
        'args': parts[1:],
        'args_joined': ' '.join(part for part in parts[1:])
    }

output = []
symbol_relations = {'//': com, 'getch': getchannel, 'gus': getuser}

fl = _filter_lines(lines)
for i in range(len(fl)):
    line = fl[i]
    line_number = i + 1

    p = get_parts(line, line_number)
    
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(p['command'])

    iv = False # Is Valid Symbol Command

    if not method:
        if symbol_relations.get(p['command']) is not None:
            iv = True
        elif symbol_relations.get(p['command']) is None and not compiler_args.ignore_undefined_variable:
            raise SyntaxError('Line {}\n"{}" does not exist. Maybe try checking your spelling.'.format(line_number, p['command']))
    
    ret = method(p, line_number) if not iv else symbol_relations[p['command']](p, line_number)
    output_line = ret + '\n' if ret != '' or ret != None else ''
    if output_line.replace(' ', '') != '':
        output.append(output_line)
    lines_written += 1

header = ''

compiled = ''
header += '# Imports\n'
for single_import in to_import:
    header += 'import {}\n'.format(single_import)
header += '\n'

header += '# From Imports\n'
for froms in from_imports:
    header += 'from {} import {}\n'.format(froms['from'], froms['import'])
header += '\n'

for line in output:
    compiled += '        ' + line


decorators_formatted = ''
for i in range(len(decorators)):
    decorators_formatted += '    ' + decorators[i] + ('\n' if i+1 < len(decorators) else '')

base = '''

class {}(commands.Bot):
    def __init__(self, client):
        self.client = client
    
{}
    @commands.command(name="{}")
    async def {}(self, ctx{} {}):
{}        

def setup(client):
    client.add_cog({}(client))
'''.format(name, decorators_formatted, name, name, "," if len(args) >= 1 else '', ",".join(x for x in args), compiled, name)

# Check if ctx is a variable used.
# If so raise an exception.
if 'ctx' in variables:
    raise Exception('Line UNKNOWN\nYou have tried to create the variable ctx.\nFor safety reason please remove this.')

print("Compiling DSC into Python..")
with open(compiler_args.output, 'w') as f:
    f.write('# Compiled with the DS Script Compiler.\n# {}\n\n'.format('-' * 35))
    final = header + '\n' + base
    final = '\n'.join(x for x in _filter_lines(final.split('\n')))
    f.write(final)

print('Successfully compiled DSC into Python.\nWrote {} lines.\n'.format(lines_written))
