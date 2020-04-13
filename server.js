const express = require('express');
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: false
}));

app.use(express.static('public'));

const mongoose = require('mongoose');

// connect to the database
mongoose.connect('mongodb://localhost:27017/greenhouse', {
  useNewUrlParser: true
});


// Configure multer so that it will upload to '/public/images'
const multer = require('multer')
const upload = multer({
  dest: './public/images/',
  limits: {
    fileSize: 10000000
  }
});

// Create a scheme for snapshot items in the greenhouse
const itemSchema = new mongoose.Schema({
  title: String,
  path: String,
  humid: Number,
  temp: Number,
  moisture: Boolean,
  intLight: Boolean,
  extLight: Boolean
});

itemSchema.virtual('id').get(function() 
{
  return this._id.toHexString();
});

// Create a model for items in the greenhouse database
const Item = mongoose.model('Item', itemSchema);

app.listen(9000, () => console.log('Server listening on port 9000!'));

// Create a new snpashot item in the greenohseu DB 
app.post('/api/items', async (req, res) => {
  console.log("HEYYYY");
  help = req.body.title
  console.log( typeof help )
  console.log( typeof req.body.temp )
  const item = new Item({
    //title: req.body.title,
    //path: req.body.imgPath,
    //temp: req.body.temp,
    //humid: req.body.humid,
    //: req.body.intLight,
    //extLight: req.body.extLight,
    //moisture: req.body.moisture
  });
  try {
    await item.save();
    res.send(item);
  } catch (error) {
    console.log(error);
    res.sendStatus(500);
  }
});

// Upload an image and keeps a path to the upladed imnage for future reference
app.post('/api/photos', upload.single('photo'), async (req, res) => {
  // Just a safety check
  if (!req.file) {
    return res.sendStatus(400);
  }
  res.send({
    path: "/images/" + req.file.filename
  });
});

// Get a list of all of the competertiors in the cute showdown
app.get('/api/items', async (req, res) => {
  try {
    let items = await Item.find();
    res.send(items);
  } catch (error) {
    console.log(error);
    res.sendStatus(500);
  }
});

// remove one of the items from the cute showdown
app.delete('/api/items/:id', async (req, res) => {
  try {
    await Item.deleteOne(
      {
        _id: req.params.id
      });
    res.sendStatus(200);
  } catch (error) {
    console.log(error);
    res.sendStatus(500);
  }
});

// edit one of the item's score in the database
app.put('/api/items/:id', async (req, res) => {
  try {
    let item = await Item.findOne(
      {
        _id: req.params.id
      });
    item.score = req.body.score;
    item.save();
    res.sendStatus(200);
  } catch (error) {
    console.log(error);
    res.sendStatus(500);
  }
});

// edit one of the item's name in the database
app.put('/api/change/:id', async (req, res) => {
  try {
    let item = await Item.findOne(
      {
        _id: req.params.id
      });
    item.title = req.body.title;
    item.save();
    res.sendStatus(200);
  } catch (error) {
    console.log(error);
    res.sendStatus(500);
  }
});
