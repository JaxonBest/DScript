# Discord Script

## How to use.

1. Create a file like 'first.dsc'
2. Write the following contents into the file.

```
var first "Hello! This is **Discord Script**"
send $first
```

### Variables

There will be many senarios when you want to use a variable.

These are the best following ways to work with them.

##### Creating a Variable

```
var my_name "Hello, World"
```

##### Changing the value of a Variable

```
cvv my_name "Hello, Universe!"
```

##### Calling a Variable

```
$my_name
```

##### Example

```
var welcome None
get_executer variable_name_storing_author
cvv welcome f"Hello, {variable_name_storing_author}"
send $welcome
```

##### Example Output

```
import discord
from discord.ext import commands

welcome = None
variable_name_storing_author = ctx.author
welcome = f"Hello, {variable_name_storing_author}"
ctx.send(welcome) # Sending a message to the same channel the message was sent in.
```

### 

### Text Channels

Here are the following methods you can use with text channels.

##### Getting a Text Channel from ID/Name

```
getchannel id my_channel_stored_variable $my_channel_id_var
```