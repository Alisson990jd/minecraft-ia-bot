const mineflayer = require('mineflayer');
const { pathfinder, goals } = require('mineflayer-pathfinder');
const { program } = require('commander');

// Configuração do bot
function criarBot() {
  const bot = mineflayer.createBot({
    host: 'Alisson9934.aternos.me',
    port: 45214,
    username: 'IA_Bot',
    version: '1.20.4'
  });

  // Recria o bot se a conexão for perdida
  bot.on('end', () => {
    console.log('Conexão perdida, reconectando...');
    setTimeout(criarBot, 5000);
  });

  // Trata erros de conexão
  bot.on('error', (err) => {
    console.error('Erro de conexão:', err.message);
  });

  // Garante que o bot só execute ações após estar pronto
  bot.on('spawn', () => {
    console.log('Bot conectado!');
    bot.loadPlugin(pathfinder.pathfinder);
    bot.pathfinder.setGoal(null);
  });

  // Plugin de pathfinding
  bot.loadPlugin(require('mineflayer-collectblock').plugin);

  // Comandos genéricos via linha de comando
  program
    .command('mover_para <x> <y> <z>')
    .description('Move o bot para uma posição específica')
    .action((x, y, z) => {
      const goal = new goals.GoalBlock(parseInt(x), parseInt(y), parseInt(z));
      bot.pathfinder.setGoal(goal);
    });

  program
    .command('coletar <item> [quantidade]')
    .description('Coleta um item específico')
    .action((item, quantidade = '1') => {
      coletarItem(bot, item, parseInt(quantidade));
    });

  program
    .command('craftar <item> [quantidade]')
    .description('Crafta um item')
    .action((item, quantidade = '1') => {
      craftarItem(bot, item, parseInt(quantidade));
    });

  program
    .command('construir <estrutura> <largura> <altura> <profundidade>')
    .description('Constrói uma estrutura')
    .action((estrutura, largura, altura, profundidade) => {
      construirEstrutura(bot, estrutura, parseInt(largura), parseInt(altura), parseInt(profundidade));
    });

  program
    .command('domar <animal>')
    .description('Domar um animal (cavalo, lobo, etc.)')
    .action((animal) => {
      domarAnimal(bot, animal);
    });

  program
    .command('encantar <item> <enchant>')
    .description('Encanta um item')
    .action((item, enchant) => {
      encantarItem(bot, item, enchant);
    });

  program
    .command('fazer_pocao <tipo>')
    .description('Faz uma poção usando uma mesa de poções')
    .action((tipo) => {
      fazerPocao(bot, tipo);
    });

  program.parse(process.argv);
}

// --- FUNÇÕES GENÉRICAS DO BOT ---

function coletarItem(bot, itemName, quantidade) {
  const mcData = require('minecraft-data')(bot.version);
  const blockId = Object.values(mcData.blocksByName).find(b => b.displayName === itemName)?.id;
  if (!blockId) return console.log(`Bloco "${itemName}" não encontrado`);

  const bloco = bot.findBlock({ matching: blockId, maxDistance: 64 });
  if (bloco) {
    bot.pathfinder.setGoal(new goals.GoalBlock(bloco.position.x, bloco.position.y, bloco.position.z));
    bot.once('goal_reached', () => {
      bot.dig(bloco, () => {
        console.log(`Coletou ${quantidade}x ${itemName}`);
      });
    });
  } else {
    console.log(`Nenhum ${itemName} encontrado`);
  }
}

function craftarItem(bot, itemName, quantidade) {
  const mcData = require('minecraft-data')(bot.version);
  const recipe = mcData.recipes.find(r => r.result.displayName === itemName);

  if (recipe) {
    bot.craft(recipe, quantidade, null, () => {
      console.log(`Craftou ${quantidade}x ${itemName}`);
    });
  } else {
    console.log(`Não foi possível craftar ${itemName}`);
  }
}

function construirEstrutura(bot, estrutura, largura, altura, profundidade) {
  const mcData = require('minecraft-data')(bot.version);
  const blockName = estrutura.replace('_', ' ');
  const blockId = mcData.blocksByName[blockName]?.id;

  if (!blockId) {
    console.log(`Bloco desconhecido: ${blockName}`);
    return;
  }

  const pos = bot.entity.position.offset(0, -1, 0);
  for (let x = 0; x < largura; x++) {
    for (let y = 0; y < altura; y++) {
      for (let z = 0; z < profundidade; z++) {
        const targetPos = pos.offset(x, y, z);
        const bloco = bot.blockAt(targetPos);
        if (!bloco || bloco.displayName === "Air") {
          bot.placeBlock(targetPos, blockId);
        }
      }
    }
  }

  console.log(`Construído: ${estrutura} (${largura}x${altura}x${profundidade})`);
}

function domarAnimal(bot, animal) {
  const mob = bot.nearestEntity(entity => entity.mobType === animal && entity.position.distanceTo(bot.entity.position) < 10);
  if (mob) {
    bot.lookAt(mob.position.offset(0, mob.height, 0));
    bot.activateEntity(mob);
    console.log(`Domando ${animal}...`);
  } else {
    console.log(`Nenhum ${animal} encontrado próximo.`);
  }
}

function encantarItem(bot, item, enchant) {
  const table = bot.findBlock({
    matching: bot.registry().blocksByName.enchanting_table.id,
    maxDistance: 16
  });

  if (table) {
    bot.pathfinder.setGoal(new goals.GoalNear(table.position.x, table.position.y, table.position.z, 1));
    bot.once('goal_reached', () => {
      bot.activateBlock(table).then(() => {
        console.log(`Encantando ${item} com ${enchant}`);
      });
    });
  } else {
    console.log("Nenhuma mesa de encantamento encontrada.");
  }
}

function fazerPocao(bot, tipo) {
  const brewStand = bot.findBlock({
    matching: bot.registry().blocksByName.brewing_stand.id,
    maxDistance: 16
  });

  if (brewStand) {
    bot.pathfinder.setGoal(new goals.GoalNear(brewStand.position.x, brewStand.position.y, brewStand.position.z, 1));
    bot.once('goal_reached', () => {
      bot.activateBlock(brewStand).then(() => {
        console.log(`Preparando poção de ${tipo}...`);
      });
    });
  } else {
    console.log("Nenhuma bancada de poções encontrada.");
  }
}

// Iniciar bot
criarBot();
