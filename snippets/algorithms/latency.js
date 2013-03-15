var data = [1, 3,4,3,3.5,3.6,2.8,4.2,8,3.7,10]

function sum(data) {
  var ret= 0;
  for (var i = data.length - 1; i >= 0; i --) {
    ret += data[i];
  }
  return ret;
}
function mean(data) {
  return sum(data) / data.length
}
function standardDeviation(data) {
  var m = mean(data);
  var sumd = 0;
  for (var i = data.length - 1; i >= 0; i --) {
    var d = data[i] - m;
    sumd += d * d;
  }
  return Math.sqrt(sumd / (data.length - 1))
}

var m = mean(data)
var sd = standardDeviation(data)
console.log('mean', mean(data))
console.log('sd', standardDeviation(data))
for (var i = data.length - 1; i >= 0; i --) {
  var x = data[i];
  console.log('x', x, 'w', Math.abs(x - m) / sd);
}
