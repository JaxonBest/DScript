lines = open('./test.dsc', 'r').read().splitlines() # Get each line.

variables = []

def raw(command, ln):
    if len(command) < 1:
        raise SyntaxError('Line {}\nMust have one or more arguments inside of a "raw" method.')
    return ' '.join(x for x in command['args'])

def arg(command, ln) -> str:
    if len(command['args']) < 1:
        raise Exception('Line {}\nYou must give the argument a name alongside with an optional type.')
    return '# Argument "{}" now assigned with type "{}"'.format(command['args'][0], command['args'][1] if len('args') >= 2 else 'any')

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
    
    return '{} = discord.utils.get(ctx.guild.channels, {}={})'.format(command['args'][1], command['args'][0].lower(), ref)

def get_executer(command, ln) -> str:
    if len(command['args']) < 1:
        raise Exception('Line: {}\nWhen using the get_executer command you must reference the name of the variable to store it into. (New Variable)')
    saving_name = command['args'][0]

    return '{} = ctx.author'.format(saving_name)

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
        if var['name'] == command['args'][0]:
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

output = ''

for i in range(len(lines)):
    line = lines[i]
    line_number = i + 1

    p = get_parts(line, line_number)
    
    possibles = globals().copy()
    possibles.update(locals())
    method = possibles.get(p['command'])
    if not method:
        raise SyntaxError('Line {}\n"{}" does not exist. Maybe try checking your spelling.'.format(line_number, p['command']))
    output += (method(p, line_number) + '\n')


print("Compiling DSC into Python..")
with open('test.py', 'w') as f:
    f.write('# Compiled with the DS Script Compiler.\n\nimport discord\nfrom discord.ext import commands\n\n')
    f.write(output)

print(output)