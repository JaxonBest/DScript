// Make sure the user has permission the kick members.
require commands.has_permissions(kick_members=True)

// Create the arguments that will be intaked.
arg target user
//  ^^^^^^ ^^^^ <= will get translated to 'target_user'

arg kicking reason 
//  ^^^^^^^ ^^^^^^ <= will get translated to 'kicking_reason'

// Kick the target user stored under the variable 'target_user'.
kick $target_user $reason

// Create a variable holding the success message.
// You can write it directly inside of the send command. 
// But for this sake I will create a variable.
var success_message 'Succesfully kicked ' + target_user.mention
//                                            ^ <= No '$' symbol because when creating variables
//                                                 It's executed as pure Python. (For flexibility). 
//                                                 Be careful because the compiler doesn't check pure Python..

// Send the message to the channel.
send $success_message

// Optionally you can also send a message to the user like this.

getexecuter executer
sendto $executer $success_message