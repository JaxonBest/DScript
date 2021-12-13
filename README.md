# Discord Script

DSC is a preprocessor to create custom commands for discord users.

It's main goal is to allow users on discord to make their own custom commands to run on a bot straight in discord.

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

### Text Channels

Here are the following methods you can use with text channels.

#### Getting a Text Channel from ID/Name

```txt
// Do it this way.
getchannel id my_channel_stored_variable $my_channel_id_var
// Or this way
getch name my_channel_stored_variable_ general-chat
```

#### Send a message/variable to a channel via variable

```txt
var my_message "Hello, World!"
sendto $my_channel_id_var $my_message
sendto $my_channel_id_var Hello, World.. Again!
```

### Working with Python

A lot of the time you will want to work with straight Python.

So you can use the 'raw' keyword at the start of every line to write pure Python.

```py
raw if 1 + 1 >= 2:
raw     print("Did you know 1 + 1 >= 2?")
```

### External Modules

You can import a module inside of DS easily.

Here is an example.
```
use sleep from time
use datetime
```

### Comments

Feel free to make a comment inside of your code on any free new line.

Here is an example..

```txt
c Send the variable called 'string'
com This is the long way of making a comment.
// DSC also allows '//'
var string = "Hello, World"
send $string
```

### Arguments

Adding arguments are super simple.

Oftenly the best place to do it is at the top is the file so it doesn't blend in.

```txt
arg user

c The below argument will default to hello_world since any space will transfer to a _
arg hello world 
```

### Working with the Executer

By **Executer** I mean the user that has executed the command.

Here a couple of examples on things you can with the **executer**.

```txt
// Get the plain user object and store it into a variable.
// The first argument is the variable to store the user object into.
get_executer my_user
// or do it the short way
gex my_user_
```

### Get User

A lot of the time your command will involve other users.

Not just the one that executes the command. 

Inside of DSC there is a keyword you can use to get a user by their ID.

```txt
// Arguments: ID, Storing Variable.
getuser 10000 my_other_user
```

This command is very common and a lot of the time you really don't want to keep typing out `get_user`

So you can use another phrase/alias called `gus` - **G - Get | us - User**

```txt
// Same as before but shorter
gus 10000 my_other_user_
```

Finally instead of hard coding an identification.

You can use a variable instead. 

```txt
// My Variable
var somebody 10000
getuser $somebody _my_other_user_
```

### Moderation

A lot of bots target moderation as their main purpose.

DSC has simplified the process of moderating a user inside of Discord.

#### Kick a Discord User

The following command will kick a user for the reason: "My Reason"

```txt
getuser 10101010 my_user
kick $my_user My Reason
```

You do not have to specify a reason like the following.

```txt
kick $my_user
```

Or you can specify a reason inside of a variable like the following:

```
var kick_reason "Spam"
kick $my_user $kick_reason
```

You can also append str text to this
```
kick $my_user $kick_reason - Do not do this again!
```