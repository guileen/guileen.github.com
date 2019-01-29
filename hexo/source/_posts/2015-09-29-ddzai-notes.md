---
title: ddz AI notes
layout: post
published: true
categories:
tags: [game, AI]
---
\`C\` is all cards.

\`p\` is the part of playing cards.

\`C_1\` is all cards after play \`p\`.

求：

\`P_a(C) = P_"activeWin"\`

\`P_p(C) = P_"passiveWin"\`

设：

\`P_d(p) = P_"dominate"\`

\`P_"f"(p) = P_"follow"\`

\`P_a(C) = max(P_a(p in C))\`

\`P_p(C) = max(P_p(p in C))\`

\`P_a(p,C) = P_d(p) * P_a(C_1) + (1-P_d(p)) * P_p(C_1)\`

\`P_p(p,C) = P_"f"(p) * P_a(p, C)\`
