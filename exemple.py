# example_bot.py
import discord
from discord.ext import commands
from discord import app_commands
from music.player import MusicPlayer
from music.queue import MusicQueue
from music.info import get_song_info, create_song_embed

class MusicBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.player = MusicPlayer()
        self.queue = MusicQueue()

    async def play_next(self, interaction):
        """Riproduce la prossima canzone in coda"""
        # Prendi la prossima canzone
        next_song = self.queue.get_next_song(interaction.guild_id)
        
        # Se c'è una canzone e siamo ancora connessi
        if next_song and interaction.guild.voice_client:
            # Crea la fonte audio
            audio = await self.player.create_audio_source(next_song['url'])
            if audio:
                # Riproduci la canzone
                interaction.guild.voice_client.play(
                    audio,
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self.play_next(interaction),
                        self.bot.loop
                    )
                )
                # Aggiorna lo stato
                self.queue.now_playing[interaction.guild_id] = next_song
        else:
            # Se non ci sono più canzoni, disconnetti
            if interaction.guild.voice_client:
                await interaction.guild.voice_client.disconnect()

    @app_commands.command(name="play")
    async def play(self, interaction, *, query: str):
        """Comando per riprodurre una canzone"""
        await interaction.response.defer()

        # Connetti al canale vocale
        voice_client = await self.player.connect_to_voice(interaction)
        if not voice_client:
            await interaction.followup.send("Devi essere in un canale vocale!")
            return

        # Ottieni le informazioni della canzone
        song_info = await get_song_info(query)
        if not song_info:
            await interaction.followup.send("Non ho trovato la canzone!")
            return

        # Se c'è già una canzone in riproduzione
        if self.player.is_playing(voice_client):
            # Aggiungi alla coda
            position = self.queue.add_song(interaction.guild_id, song_info)
            await interaction.followup.send(
                f"🎵 Aggiunto alla coda (posizione {position})",
                embed=create_song_embed(song_info)
            )
        else:
            # Riproduci subito
            audio = await self.player.create_audio_source(song_info['url'])
            if audio:
                voice_client.play(
                    audio,
                    after=lambda e: asyncio.run_coroutine_threadsafe(
                        self.play_next(interaction),
                        self.bot.loop
                    )
                )
                self.queue.now_playing[interaction.guild_id] = song_info
                await interaction.followup.send(
                    "🎵 Ora in riproduzione",
                    embed=create_song_embed(song_info)
                )

    @app_commands.command(name="skip")
    async def skip(self, interaction):
        """Salta la canzone corrente"""
        await interaction.response.defer()
        
        if not interaction.guild.voice_client:
            await interaction.followup.send("Non sto riproducendo nulla!")
            return
            
        interaction.guild.voice_client.stop()
        await interaction.followup.send("⏭️ Canzone saltata!")

    @app_commands.command(name="queue")
    async def show_queue(self, interaction):
        """Mostra la coda delle canzoni"""
        await interaction.response.defer()
        
        queue = self.queue.show_queue(interaction.guild_id)
        if not queue:
            await interaction.followup.send("La coda è vuota!")
            return
            
        embed = discord.Embed(
            title="🎵 Coda Musicale",
            color=discord.Color.blue()
        )
        
        # Mostra la canzone corrente
        now_playing = self.queue.now_playing.get(interaction.guild_id)
        if now_playing:
            embed.add_field(
                name="Ora in riproduzione",
                value=now_playing['title'],
                inline=False
            )
        
        # Mostra le prossime canzoni
        queue_text = "\n".join(
            f"`{i+1}.` {song['title']}"
            for i, song in enumerate(queue)
        )
        if queue_text:
            embed.add_field(
                name="Prossime canzoni",
                value=queue_text,
                inline=False
            )
            
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MusicBot(bot))

# Come usare il bot:
if __name__ == "__main__":
    import asyncio

    bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f'Bot connesso come {bot.user}')
        await setup(bot)
        await bot.tree.sync()

    # Inserisci qui il tuo token
    TOKEN = "token"