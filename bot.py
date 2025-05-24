import discord  # type: ignore
from discord import app_commands  # type: ignore
from discord.ext import commands  # type: ignore

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

customers = []  # Liste globale des clients

@bot.event
async def on_ready():
    print(f"{bot.user} est connecté.")
    try:
        synced = await bot.tree.sync()
        print(f"Commandes synchronisées: {len(synced)}")
    except Exception as e:
        print(e)

@bot.tree.command(name="customer", description="Affiche la liste des clients ajoutés")
async def customer_command(interaction: discord.Interaction):
    if not customers:
        await interaction.response.send_message("Aucun client ajouté pour l'instant.", ephemeral=True)
        return

    description = ""
    for i, user in enumerate(customers, start=1):
        description += f"Customer #{i} • {user.mention} • ID : {user.id}\n"

    embed = discord.Embed(title="Liste des clients", description=description, color=discord.Color.purple())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="addcustomer", description="Ajoute un client à la liste via son ID Discord")
@app_commands.describe(user_id="L'ID Discord du client à ajouter")
async def addcustomer_command(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
    except Exception:
        await interaction.response.send_message("ID invalide ou utilisateur introuvable.", ephemeral=True)
        return

    if user in customers:
        await interaction.response.send_message(f"{user.mention} est déjà dans la liste des clients.", ephemeral=True)
        return

    customers.append(user)  # Ajoute à la fin de la liste
    await interaction.response.send_message(f"{user.mention} a bien été ajouté à la liste des clients.")

@bot.tree.command(name="buy", description="PayPal Mail")
async def buy_command(interaction: discord.Interaction):
    embed = discord.Embed(title="<:paypal2:1375858352751382759> : kikamail@protonmail.com", color=discord.Color.blue())
    await interaction.response.send_message(embed=embed)

bot.run("token")
