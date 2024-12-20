import discord
import yt_dlp
import asyncio

async def get_song_info(query):
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if not query.startswith('http'):
                query = f"ytsearch:{query}"
            
        
            info = await asyncio.to_thread(ydl.extract_info, query, download=False)
            
            if 'entries' in info:
                info = info['entries'][0]
            song_info = {
                'title': info['title'],
                'url': info['webpage_url'],
                'duration': info['duration'],
                'thumbnail': info['thumbnails'][-1]['url'] if info.get('thumbnails') else None,
                'channel': info.get('uploader', 'Sconosciuto'),
                'views': info.get('view_count', 0),
                'likes': info.get('like_count', 0)
            }
            
            return song_info
            
    except Exception as e:
        print(f"Errore nel trovare la canzone: {e}")
        return None

def create_song_embed(song_info):
    """Crea un bell'embed per la canzone"""
    embed = discord.Embed(
        title="🎵 Ora in riproduzione",
        description=song_info['title'],
        color=discord.Color.blue()
    )
    
    embed.add_field(name="Canale", value=song_info['channel'])
    
    minutes = song_info['duration'] // 60
    seconds = song_info['duration'] % 60
    embed.add_field(name="Durata", value=f"{minutes}:{seconds:02d}")
    
    if song_info['views'] > 0:
        embed.add_field(name="👀 Views", value=f"{song_info['views']:,}")
    if song_info['likes'] > 0:
        embed.add_field(name="👍 Likes", value=f"{song_info['likes']:,}")
    
    if song_info['thumbnail']:
        embed.set_thumbnail(url=song_info['thumbnail'])
    
    return embed