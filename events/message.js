const discord = require('discord.js');
const prefix = (client.prefix)

module.exports = {
	name: 'message',
	execute(message, client) {
		if (message.author.bot) return;
        if (message.channel.type == 'dm') return;
        if (!message.content.startsWith(client.prefix));

        const args = message.content.slice(client.prefix.length).trim().split(/ +/);
        const commandName = args.shift().toLowerCase();

        const command = client.commands.get(commandName)
		|| client.commands.find(cmd => cmd.aliases && cmd.aliases.includes(commandName));

        if (!command) return;

        if (!client.commands.has(commandName)) return;

        if (command.permissions) {
            const authorPerms = message.channel.permissionsFor(message.author);
            if (!authorPerms || !authorPerms.has(command.permissions)) {
                return message.reply('Invalid permissions!!');
            }
        }

        if (command.args && !args.length) {
            let reply = `There are missing arguments`;
            
            if (command.usage) {
                reply += `\nThe proper usage would be: \`${prefix}${command.name} ${command.usage}\``;
             }
            
            return message.channel.send(reply);
        }

        //Cooldowns

        const { cooldowns } = client;

        if (!cooldowns.has(command.name)) {
	        cooldowns.set(command.name, new discord.Collection());
        }

        const now = Date.now();
        const timestamps = cooldowns.get(command.name);
        const cooldownAmount = (command.cooldown || 2) * 1000;

        if (timestamps.has(message.author.id)) {
        	const expirationTime = timestamps.get(message.author.id) + cooldownAmount;

        	if (now < expirationTime) {
	        	const timeLeft = (expirationTime - now) / 1000;
	        	return message.reply(`Please wait ${timeLeft.toFixed(1)} more second(s) before reusing this command.`);
	        }
        }
        timestamps.set(message.author.id, now);
        setTimeout(() => timestamps.delete(message.author.id), cooldownAmount);

        //Error logging
        try {
            command.execute(message, args, client);
        } catch (error) {
            console.log(error);
            message.reply('A error occured while trying to run this command.');
        }
	},
};