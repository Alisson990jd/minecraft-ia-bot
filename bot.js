const mineflayer = require('mineflayer');
const { goals } = require('mineflayer-pathfinder');
const pathfinder = require('mineflayer-pathfinder').pathfinder;
const collectBlock = require('mineflayer-collectblock');

function criarBot() {
  const bot = mineflayer.createBot({
    host: 'Alisson9934.aternos.me',
    port: 45214,
    username: 'IA_Bot',
    version: '1.20.4'
  });

  // ✅ Plugins carregados corretamente
  bot.loadPlugin(pathfinder);
  bot.loadPlugin(collectBlock.plugin);

  // ✅ Reconnect automático
  bot.on('end', () => {
    console.log('Conexão perdida, reconectando...');
    setTimeout(criarBot, 5000);
  });

  // ✅ Comandos CLI
  program
    .command('coletar <item> [quantidade]')
    .description('Coleta um item específico')
    .action((item, quantidade = '1') => {
      coletarItem(bot, item, parseInt(quantidade));
    });

  program
    .command('domar <animal>')
    .description('Domar um animal')
    .action((animal) => {
      domarAnimal(bot, animal);
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
      bot.collectBlock.collect(bloco).then(() => {
        console.log(`Coletou ${quantidade}x ${itemName}`);
      }).catch(err => {
        console.error(`Falha ao coletar: ${err.message}`);
      });
    });
  } else {
    console.log(`Nenhum ${itemName} encontrado`);
  }
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

criarBot();
