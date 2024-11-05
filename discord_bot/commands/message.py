import json
import disnake
from disnake.ext import commands

class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="сообщение", description="Создать сообщение", dm_permission=False)
    @commands.has_permissions(administrator=True)
    async def embed(self, interaction):
        pass

    @embed.sub_command(name="отправить", description="Отправить сообщение")
    async def embed_send(self, interaction, 
            json_data: str = commands.Param(
                name="json",
                description="Данные в формате JSON"
            )
        ):
        print(f"Права пользователя: {interaction.user.guild_permissions}")
        await self.send_message(interaction, json_data)

    @embed.sub_command(name="изменить", description="Изменить сообщение")
    async def embed_edit(self, interaction,
            json_data: str = commands.Param(
                name="json",
                description="Данные в формате JSON"
                ),
            message_id: str = commands.Param(
                name="id",
                description="ID сообщения, которое необходимо изменить"
                )
        ):
        await self.edit_message(interaction, message_id, json_data)

    async def get_embeds(self, json_data):
        data = json.loads(json_data)
        embeds_data = data.get("embeds", [])
        embeds = []

        for embed_data in embeds_data:
            embed = await self.create_embed(embed_data)
            embeds.append(embed)

        return embeds

    async def create_embed(self, embed_data):
        title = embed_data.get("title", "")
        description = embed_data.get("description", "")
        color = embed_data.get("color", "0x2b2d31")

        embed_color = int(color, 16) if isinstance(color, str) else color

        embed = disnake.Embed(
            title=title,
            description=description,
            color=embed_color
        )

        if embed_data.get("image"):
            embed.set_image(url=embed_data["image"]["url"])
        if embed_data.get("thumbnail"):
            embed.set_thumbnail(url=embed_data["thumbnail"]["url"])
        if embed_data.get("footer"):
            embed.set_footer(text=embed_data["footer"].get("text", ""), icon_url=embed_data["footer"].get("icon_url"))
        if embed_data.get("author"):
            embed.set_author(name=embed_data["author"].get("name", ""), url=embed_data["author"].get("url"), icon_url=embed_data["author"].get("icon_url"))

        for field in embed_data.get("fields", []):
            embed.add_field(name=field.get("name", ""), value=field.get("value", ""), inline=field.get("inline", False))

        return embed

    async def send_message(self, interaction, json_data):
        await interaction.response.defer(ephemeral=True)

        content = json.loads(json_data).get("content", "")
        embeds = await self.get_embeds(json_data)

        await interaction.channel.send(content, embeds=embeds)
        await interaction.followup.send("Сообщение успешно отправлено!", ephemeral=True)

    async def edit_message(self, interaction, message_id, json_data):
        await interaction.response.defer(ephemeral=True)

        content = json.loads(json_data).get("content", "")
        embeds = await self.get_embeds(json_data)
        message = await interaction.channel.fetch_message(message_id)

        await message.edit(content, embeds=embeds)
        await interaction.followup.send("Сообщение успешно обновлено!", ephemeral=True)

def setup(bot):
    bot.add_cog(Embed(bot))