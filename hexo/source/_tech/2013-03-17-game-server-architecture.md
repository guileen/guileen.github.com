---
title: Game server architecture
layout: post
published: false
categories:
tags: [game-dev]
---

* ✓ Router
* ✓ SessionContext
* ✓ AppContext
*  SuperManager - load player(from online, pool or db), create player
*  SessionManager - player online, player offline, send message to other player
* WorldManager - A whole world controller (get player ? find player, get clans)
* ✕ RoomManager sub world?
* ✕ RoomNodeManager Room is tree?
* ✓ PlayerWritePool -
PlayerCache -
* ✓ PlayerStore -
