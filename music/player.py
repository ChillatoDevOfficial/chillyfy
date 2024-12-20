# music/player.py
import discord
import yt_dlp
import asyncio

class MusicPlayer:
    def __init__(self):
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        
        # Opzioni per youtube-dl
        self.YDL_OPTIONS = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True
        }
    
    async def create_audio_source(self, url):
        """Crea una fonte audio da un URL"""
        try:
            with yt_dlp.YoutubeDL(self.YDL_OPTIONS) as ydl:
                info = await asyncio.to_thread(ydl.extract_info, url, download=False)
                url2 = info['url']
                return discord.FFmpegPCMAudio(url2, **self.FFMPEG_OPTIONS)
        except Exception as e:
            print(f"Errore nella creazione dell'audio: {e}")
            return None

    @staticmethod
    async def connect_to_voice(interaction):
        """Connette il bot al canale vocale"""
        if not interaction.user.voice:
            return None
            
        channel = interaction.user.voice.channel
        
        try:
            if not interaction.guild.voice_client:
                return await channel.connect()
            elif interaction.guild.voice_client.channel != channel:
                await interaction.guild.voice_client.move_to(channel)
            
            return interaction.guild.voice_client
            
        except Exception as e:
            print(f"Errore nella connessione al canale vocale: {e}")
            return None

    @staticmethod
    def is_playing(voice_client):
        """Controlla se il bot sta riproducendo musica"""
        return voice_client and voice_client.is_playing()

    @staticmethod
    def pause(voice_client):
        """Mette in pausa la musica"""
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            return True
        return False

    @staticmethod
    def resume(voice_client):
        """Riprende la riproduzione"""
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            return True
        return False

    @staticmethod
    def stop(voice_client):
        """Ferma la riproduzione"""
        if voice_client:
            voice_client.stop()
            return True
        return False