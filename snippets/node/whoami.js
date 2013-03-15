var util = require('util');
var EventEmitter = require('events').EventEmitter;

function Foo(name) {
  EventEmitter.call(this);
  this.name = name;
}

util.inherits(Foo, EventEmitter);

var foo = new Foo('world');
foo.on('hello', function(){
    console.log(this.name);
});

foo.emit('hello');
