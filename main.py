lines = open('./test.dsc', 'r').read().splitlines() # Get each line.

variables = []
to_import = ['discord']
from_imports = [{'from': 'discord.ext', 'import': 'commands'}]
args = []
name = 'untitled_command'

def com(command, ln) -> str:
    return '# {}'.format(' '.join(x for x in command['args']))

def c(command, ln):
    return com(command, ln)

def getuser(command, ln) -> str:
    u_var, u_var_exists = _get_and_check_if_var(command['args'][0][1:])
    ref = 'int({})'.format(u_var['name'] if u_var_exists else ('"' + command['args'][0] + '"'))

    return '{} = self.client.get_user({})'.format(command['args'][1], ref)        

def sendto(command, ln) -> str:
    if len(command['args']) <= 1:
        raise SyntaxError('Line {}\nWhen using "sento" you must supply a channel and then a message/variable to use.'
        .format(ln))
    pos_var_content = command['args'][1]
    channel_var, is_channel_var = _get_and_check_if_var(command['args'][0][1:])
    if not is_channel_var:
        raise Exception('Line {}\n"{}" is not a variable. Maybe you forgot to add the "$"?'
        .format(ln, command['args'][0][1:]))

    cnt_res = '"{}"'.format(' '.join(x.replace('"', "'") for x in command['args'][1:]))
    cnt_var, cnt_is_var = _get_and_check_if_var(pos_var_content[1:]) # Indexing here to remove the '$'
    if cnt_is_var:
        cnt_res = cnt_var['name']
    return '{}.send({})'.format(channel_var['name'], cnt_res)

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


    return ' '.join([command['args'][i] + ' ' for i in range(len())])

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

def get_executer(command, ln) -> str:
    if len(command['args']) < 1:
        raise Exception('Line: {}\nWhen using the get_executer command you must reference the name of the variable to store it into. (New Variable)')
    saving_name = command['args'][0]
    variables.append({'name': saving_name, 'value': 'ctx.author', 'type': 'executer'})
    return '{} = ctx.author'.format(saving_name)

def gex(command, ln) -> str:
    return get_executer(command, ln)

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
    if var_info is None:
        raise ReferenceError('Line {}\nCannot find variable named "{}".\nReminder: You cannot change the value a variable before you have assigned it.'
        .format(ln, command['args'][0]))
    if len(command['args']) <= 1:
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
        if found_val_var is None:
            raise SyntaxError('Line {}\nTried to find variable named "{}" but failed.'.format(ln, used_var))
            
        used_var = found_val_var if not None else ("'" + command['joined_args'] + '"')
        val = used_var

    return 'ctx.send({}) # Sending a message to the same channel the message was sent in.'.format(val)



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

    return '{} = {}'.format(name, value)

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
symbol_relations = {'//': com, 'getch': getchannel}

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
        else:
            raise SyntaxError('Line {}\n"{}" does not exist. Maybe try checking your spelling.'.format(line_number, p['command']))
    
    ret = method(p, line_number) if not iv else symbol_relations[p['command']](p, line_number)
    output.append(ret + '\n' if ret != '' or ret != None else '')

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

base = '''
class {}(commands.Bot):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="{}")
    async def {}(self, ctx{} {}):
{}        

def setup(client):
    client.add_cog({}(client))
'''.format(name, name,  name, ", " if len(args) >= 1 else '', ",".join(x for x in args), compiled, name)

# Check if ctx is a variable used.
# If so raise an exception.
if 'ctx' in variables:
    raise Exception('Line UNKNOWN\nYou have tried to create the variable ctx.\nFor safety reason please remove this.')

print("Compiling DSC into Python..")
with open('test.py', 'w') as f:
    f.write('# Compiled with the DS Script Compiler.\n# {}\n\n'.format('-' * 35))
    f.write(header)
    f.write(base)

print('Successfully compiled command.')