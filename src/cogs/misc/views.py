import discord


class PollView(discord.ui.View):
    # Horribly fucky
    def __init__(self):
        super().__init__()
        # Yes I know this could be a dict.
        self.users_yes = []
        self.users_no = []

    # I hate all of this.
    # Once discord.py has delete_after for interactions, we can implement that.
    @discord.ui.button(label="Yes.", style=discord.ButtonStyle.green)
    async def yes_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if str(interaction.user) in self.users_yes:
            await interaction.response.send_message(
                "You already voted Yes", ephemeral=True
            )
            return
        elif str(interaction.user) in self.users_no:
            self.users_no.remove(str(interaction.user))
            await interaction.response.send_message(
                "Changed your vote to Yes", ephemeral=True
            )
        else:
            await interaction.response.send_message("You voted Yes", ephemeral=True)
        self.users_yes.append(str(interaction.user))
        print(f"{interaction.user} voted yes")

    @discord.ui.button(label="No.", style=discord.ButtonStyle.red)
    async def no_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if str(interaction.user) in self.users_no:
            await interaction.response.send_message(
                "You already voted No", ephemeral=True
            )
            return
        elif str(interaction.user) in self.users_yes:
            self.users_yes.remove(str(interaction.user))
            await interaction.response.send_message(
                "Changed your vote to No", ephemeral=True
            )
        else:
            await interaction.response.send_message("You voted No", ephemeral=True)
        self.users_no.append(str(interaction.user))
        print(f"{interaction.user} voted no")

    async def disable_view(self) -> None:
        """
        Called when the poll runs out
        """
        for child in self.children:
            child.label = "Poll Finished"
            child.disabled = True
            child.style = discord.ButtonStyle.grey
