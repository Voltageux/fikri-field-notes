---
title: Why I'm building Crust & Crime
date: 2026-10-14
description: Building a restaurant-management game where the player belongs to the city, not just the balance sheet.
tags: Crust & Crime, Godot, Game design, Development diary
status: Introduction
---

Most of my work begins with a question. For **Crust & Crime**, that question is: *What would a restaurant-management game feel like if you could actually live inside the world you're managing?*

I'm developing a stylized 3D game that brings together two perspectives I enjoy: running a business and directly controlling a character in the city. The ambition is not just to build a restaurant, adjust some prices, and watch numbers rise. I want the player to be able to participate in the work and the wider world around that business.

The project is still under active development. Some systems already exist as prototypes, while others are ideas being tested rather than promises of finished features.

## A city that does more than decorate the background

I want restaurants, employees, pedestrians, and the player to operate in a world that behaves coherently. Managing multiple restaurants is one challenge. Making their customers feel like people who belong to the surrounding district is another.

One experiment I want to pursue is **organic customer behavior**: instead of creating a customer at a restaurant's entrance, a pedestrian already walking in the neighborhood might decide to eat, choose a destination, travel there, and return to everyday activity afterward. That raises interesting questions about agent state, pathfinding, restaurant capacity, performance, and how much simulation is actually necessary.

I also want to explore a controllable player character who can take on different roles, including hands-on restaurant work, management, and movement through the city. These ideas need to earn their place through playable tests.

## What I'll share in this journal

This is a development log, not a marketing brochure. I plan to write about:

- **Game systems:** restaurant operations, customer behavior, player controls, and how separate mechanics communicate.
- **Technical decisions:** Godot architecture, code excerpts, performance measurements, and the trade-offs behind an implementation.
- **Creative work:** prototypes, Blender workflows, interfaces, and experiments with the game's stylized look.
- **Failures and changes of direction:** bugs, overly ambitious ideas, rejected approaches, and what I learn from them.

I use AI tools as development assistants alongside conventional coding and modeling tools. I'll review and test their output, and I won't treat AI assistance as a substitute for responsibility over the resulting game or the requirements for shipped player-facing content.

## The next experiment

A useful near-term goal is to connect the pedestrian population more naturally with restaurant visits, then measure both behavior and performance in a small district. Does it feel organic? Are the transitions believable? How many active agents can the simulation comfortably support?

If it works, I'll document why. If it doesn't, I'll document that too.

**Welcome to the Crust & Crime development diary.**
