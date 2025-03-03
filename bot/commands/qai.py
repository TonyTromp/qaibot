# bot/commands/qai.py
import discord, logging
from ..integrations.openai_chat import ask_question
from ..utilities import send_large_message

async def handle_qai(interaction: discord.Interaction, question: str):
    await interaction.response.defer()
    progress_message = await interaction.followup.send(f"QAI leest je vraag: {question}. Ok, momentje ...")
    logging.info(f"Qai was asked a question: {question}. Processing with OpenAI...")
    processed_text = ask_question(question)
    
    if processed_text:
        logging.info("Qai has generated an answer and is sending it to Discord now.")
        message = f"**Original Question:** {question}\n**Response:**\n{processed_text}"
        await send_large_message(interaction, message)
        # await send_large_message(interaction, processed_text)
        
    else:
        logging.error("Error: No response received from processing at OpenAI.")
        await interaction.followup.send("Error: No response received from processing.")


        
