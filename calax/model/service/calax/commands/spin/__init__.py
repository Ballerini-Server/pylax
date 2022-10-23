# --------------- BUILT-IN PACKAGES ---------------
from random import (
    choice
)

# --------------- DISCORD PACKAGES ---------------
from discord.ext.commands.context import (
    Context
)
from discord.message import Message

# --------------- PERSONAL PACKAGES ---------------
from model.entities.player import (
    Player
)
from model.entities.room import (
    Room
)
from model.instances.calax import (
    calax
)
from util.room import (
    findRoomInCalaxByPlayerId
)


@calax.bot.command()
async def spin(context: Context):
    player: Player = Player(str(context.author.id))
    player.user = calax.bot.get_user(int(player.id))
    player_room: Room = findRoomInCalaxByPlayerId(player.id, calax)
    for room in calax.rooms:
        if str(context.channel.id) == room.id_txt_channel\
        and room.game.fase_controller == 1\
        and room.game.asker.id == player.id:
            punished_player_ids: list[str] =\
                        [punished_playes.id for punished_playes in room.game.punished_players]
            if len([player for player in room.game.players if player.id not in punished_player_ids]) > 1:
                room.game.is_victim_a_asker = False
                # Raffles a different person to the arker to be
                # the victim
                while not room.game.is_victim_a_asker:
                    room.game.victim = choice(room.game.players)
                    if room.game.victim.id != room.game.asker.id\
                        and room.game.victim.id not in punished_player_ids:
                        room.game.is_victim_a_asker = True

                # Show the bottle spining
                message: Message = await context.send(
                    content = f'Girando a garrafa: <@{choice(room.game.players).id}>'
                )
                for _ in range(10):
                    await message.edit(
                        content = f'Girando a garrafa: <@{choice(room.game.players).id}>'
                    )
                await message.edit(
                    content = f'Girando a garrafa: <@{room.game.victim.id}>'
                )
                await message.delete()

                await context.send(
                    content = f'<@{room.game.asker.id}> pergunta para <@{room.game.victim.id}>. Verdade ou consequência?'
                )
                room.game.fase_controller = 2
                break
            else:
                await context.send(f'Não é possível girar a garrafa agora agora. Veja o número de jogadores.')
        else:
            # [IMPLEMENTS]
            ...