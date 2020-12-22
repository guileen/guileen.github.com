function testProfit(initial, winRate, max_ratio, betRatio, hands) {
    var value = initial;
    for (var i = 0; i < hands; i++) {
        var bit = value * betRatio;
        var ratio = Math.random() * max_ratio;
        var win = Math.random() < winRate
        if (win) {
            value = value + bit * ratio
        } else {
            value = value - bit * ratio
        }
        if (value < 1000){
            console.log(initial, "xxxx", i )
            break;
        } 
    }
    if(value>0) {
        // console.log(initial, "=>", value)
    }
    return value
}

var bcount = 0;
var wcount = 0;
var ary = []
var total = 0;
for(var j=0;j<1000;j++) {
    let v = testProfit(10000, 0.6, 0.20, 1, 1000)
    ary.push(v)
    if(v<5000) {
        bcount++;
    }
    if(v>1000000) {
        wcount++;
    }
    total += v
}
console.log("bao:" + bcount, "wcount:" + wcount, "avg:", Math.floor(total/1000/10000))
