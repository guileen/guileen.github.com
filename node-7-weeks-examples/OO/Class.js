function task(url, callback) {
// ...
}

task(url, function(err, result) {
    save(results);
});

async.forEachLimit(urls, 10, task , callback);
async.map(urls, task, function(err, results) {

})

async.parallel([
    function task1(callback0){
        .....callback0(...)
  },
  function task2(callback1) {
      .....callback1(...);
  }
], callback);

// last argument is callback

function foo(callback) {...}
function bar(args..., callback) {...}

callback = function(err, data);
// js OO

function BookModel(db, redis) {
  this.db = db;
  this.redis = redis;
  this.book = db.collection('book');
}

BookModel.prototype.get = function(id, callback) {
  this.db.findOne({_id: id}, callback);
}

BookModel.prototype.getFavoriteBooks = function(uid, callback) {
  var self = this;
  this.redis.lrange('user:' + uid + ':favbooks', 0, -1, function(err, bids) {
      async.map(bids, function(bid, callback) {
          self.get(bid, callback);
      }, callback);
  });
}

var bookModel = new BookModel(db, redisClient);
bookModel.get(id, callback);

// closure

function BookModel(db, redis) {
  var book = db.collection('book');

  function get(id, callback) {
    db.findOne({_id: id}, callback);
  }

  function getFavoriteBooks(uid, callback) {
    redis.lrange('user:' + uid + ':favbooks', 0, -1, function(err, bids) {
        async.map(bids, get, callback);
    });
  }

  return {
    get: get,
    getFavoriteBooks: getFavoriteBooks
  }
}

var bookModel = BookModel(db, redisClient);
bookModel.get(id, callback);


// curry

function foo(key, value) {
  return function(callback) {
    bar(key, value, callback);
  }
}

Function.bind(thisArg, arg1, arg2, arg3...); 
return function(argx);
thisArg.....arg1..arg2 ... argx

var fn = foo('key', 'value');
var fn = bar.bind(redisClient, 'key', 'value');
fn(callback); // === bar('a', 'b', 'c');

// Function.bind
async.parallel([
    function(callback) {
      redisClient.set(key, value, callback);
    },
    function(callback) {
      redisClient.hgetall(key2, callback);
    }
], function(err, results) {
  console.log(results);
});

function doSomething(callback) {
  redisClient.set(key, value, callback);
  redisClient.hgetall(key, callback);
}

function doSomething(callback) {

  async.parallel([
      redisClient1.set.bind(redisClient1, 'key1', 'value'),
      redisClient2.hgetall.bind(redisClient2, 'key2'),
  ], callback);
}

// app.js

db = mongoskin.db(config.db.url);
redisClient = redis.createClient(config.redis.port, config.redis.host);
app.set('bookModel', BookModel(db, redisClient));

require('./routes')(app);

// routes/index.js

var exports = module.exports = function(app) {
  require('./books')(app);
  require('./users')(app);
}

// routes/books.js

var exports = module.exports = function(app) {
  var bookModel = app.get('bookModel');
  app.get('/favbooks', function(req, res, next) {
      bookModel.getFavoriteBooks(req.query.uid, function(err, books) {
          if(err) {return next(err);}
          res.render('favbooks', {books: books});
      });
  });

}
