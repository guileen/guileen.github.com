---
title: 桂糊涂的德州扑克AI
layout: post
published: true
categories:
tags: [game, AI]
---

如何编写德州扑克的AI。

德州扑克与其他的棋牌类游戏不同，他不一定存在着最优解，更多的是一种心理竞技。这对于人类来说可能很简单，但对于电脑来说却并不擅长。我的目标就是将人类的思维用代码的方式重现出来。

对德州的分析，首先是概率。一手牌的胜率是多少。在底牌，翻牌，转牌，河牌阶段的算法依次如下：

底牌阶段的算法采用查表法。13不同花色的牌组合共有169种，分为，对子面，同花面，杂花面。这里有个小技巧，13可以用4个bit来表示，两张底牌的组合，正好可以用一个字节来表示。我用高位在前表示同花，低位在前表示杂花。

河牌阶段的胜率算法也比较简单。我采用的是穷举法————去除自己的底牌和公牌后，组合遍历对手可能的底牌，将对手的底牌与自己的底牌比较，胜率=获胜次数/组合数。组合数共有995种。这里的关键是如何高效比较我方牌与对手牌的大小。

转牌阶段的胜率，依然采用穷举法————组合遍历河牌，并计算河牌胜率的平均值。河牌共有46种可能，因此算法复杂度为O(45540)。这一切比较都依赖于快速比较手牌，如果手牌比较速度慢，将无法快速计算出这一胜率。

翻牌阶段胜率，无法再采用转牌阶段胜率的算法，这里有个技巧，翻牌阶段胜率近似=发一张牌后的胜率。

如何快速比较自己和对方的手牌。这里也使用了一个小技巧，就是将每张牌面的大小数值化。德州牌面比较是先比较牌型，再比较牌值。因此，将牌型的值作为最高位，将牌面的值作为后5位，即可形成一个比较值。如红3黑5方A梅5方5，牌值为=3555e3。3代表3条牌型，555e3是牌面值。A一般作为14牌值处理。从高牌，对子，两对，三条，顺子，葫芦，同花，四条，同花顺，依次是0，1，2，3，4，5，6，7，8。牌面值直接用2,3,4,5,6,7,8,9,A,B,C,D,E。以16进制表示依然可以有很好的可读性。

在做牌型检测时，同花，顺子比较特殊，其他的4条，3条，葫芦，两对，对子，高牌，都是相似的。

同花检测，将同样花色的牌放进桶里，一个桶里的牌大于等于5张，则为同花，若这5张还能成顺，则为同花顺。

顺子检测时，A较为特殊，既可以和10，J，Q，K搭配，也可以和2，3，4，5，6搭配。将14位数组，设置1，0，1表示存在该牌，0表示不存在。从大到小遍历计数，连续计数5次则为顺子。之所以从大到小遍历是为了找到最大的顺子而不是最小的顺子。

其他牌型比较，先将牌放进13个桶里，然后将这些桶排序。排序方法是，桶里的牌越多越大，牌一样多比较桶本身的编号。这样我们就得出了\[3个3，2个J，2个8，1个K\]的桶列表。如果第一个桶是4张，那我们的牌型就是4条。第一个桶是3张就是3条，同时第二个桶是2张就是葫芦，前两个桶是两张就是两对，第一个桶是两张是一对，否则就是杂牌。

但是仅仅知道胜率是远远不够的，这只是人类思维的开始。人类对于胜率的判断很多是基于经验，但这种经验非常高效，综合考虑了很多数学概率中没考虑到的因素：比如，玩家数量，底池大小，对手下注量。人类有恐惧感，也有冒险精神，这都是电脑所不具备的。

有没有可能设计一种AI，只根据标准的概率下注，完全不考虑人类心理因素呢？

德州高手会研究对手。如果一个玩家从来不Bluff（诈赌），并且他的下注量和他的胜率相关。有经验的牌手，可以根据他的下注量反推出他的胜率，再根据他的胜率反推出他的手牌。与一个透明的玩家玩牌，要赢可能要看手气，要输真的很难。

另一方面，一个绝不冒险的玩家，也会被轻易的Bluff掉，从而使对手的实际胜率远大于理论上的胜率。

还有一方面，那就是恐惧。电脑不会恐惧，当对手ALLIN的时候，人类会忌惮，会重新评估对手的牌力。但电脑不会，他认为的大牌，无论多大的注都会跟。

因此，学会冒险与恐惧是编写德州AI的最大难点。

人数概率修正。人数影响概率。
恐惧修正。
安全跟注值计算。
Value控制。
Balnace。
BLUFF。Bluff的时机。