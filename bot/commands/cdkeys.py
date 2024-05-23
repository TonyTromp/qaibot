import discord
from ..integrations.search_cdkeys import search_cdkeys
from urllib.parse import urlparse, urlunparse, quote
from ..utilities import send_large_message
import logging

async def handle_cdkeys(interaction: discord.Interaction, game_name: str):
    await interaction.response.defer()
    results = search_cdkeys(game_name)
    if results:
        formatted_results = []
        for result in results:
            game_title = result['game_title']
            price = result['price']
            detail_url = result['detail_url']
            # Ensure the URL is safe for Discord
            parsed_url = urlparse(detail_url)
            safe_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                quote(parsed_url.path),
                parsed_url.params,
                quote(parsed_url.query),
                parsed_url.fragment
            ))
            formatted_results.append(f"**{game_title}** - Price: {price}, [Buy Now]({safe_url})")

        message = "\n".join(formatted_results)
        final_message = f"**Original Question:** {game_name}\n**Response:**\n{message}"

        await send_large_message(interaction, final_message)
    else:
        logging.warning("No results found or there was an error fetching game details.")
        await interaction.followup.send("No results found or there was an error.")
