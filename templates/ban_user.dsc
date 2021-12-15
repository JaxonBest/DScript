require commands.has_permissions(ban_members=True)

arg target
arg reason

ban $target $reason
var ban_success_message "{} was successfully banned!".format(target.discriminator)

send $ban_success_message