let Owlbot = require('owlbot-js');
let fs = require('fs');

let client = Owlbot('ff85873d2bf1c0675c0a6bca48a9613a18534224');

words = [
  'ballroom',
  'five',
  'convertible',
  'cherry',
  'north',
  'family',
  'worm',
  'rust',
  'complete',
  'empty',
  'accountable',
  'twelve',
  'inner',
  'down',
  'positive',
  'brass',
  'honey',
  'bloodstream',
  'prayer',
  'military',
];

const getDefs = async () => {
  let cards = {};

  for (let i = 0; i < words.length; i++) {
    let result;
    result = await client.define(words[i]);
    cards[i] = result;
  }
  return cards;
};
getDefs()
  .then((cards) => {
    return JSON.stringify(cards);
  })
  .then((cards) => {
    fs.writeFile('cards_6.json', cards, 'utf8', (err) => {
      if (err) console.log(err);
      else {
        console.log('File written successfully\n');
        console.log('The written has the following contents:');
        console.log(fs.readFileSync('cards_6.json', 'utf8'));
      }
    });
  });
