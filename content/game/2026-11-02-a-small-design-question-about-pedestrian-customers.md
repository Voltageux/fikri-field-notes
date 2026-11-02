---
title: A small design question about pedestrian customers
date: 2026-11-02
description: A design note on the smallest set of states and transitions a pedestrian might need to become a restaurant customer in Crust & Crime.
tags: Crust & Crime, Game Design, Simulation
status: Research Plan
topic_id: game-ped-plan-20261102
---

## Before they become customers

One design goal for Crust & Crime is for restaurant customers to feel like pedestrians in a living district. They should have a place in the street before they have a place in the restaurant, instead of suddenly appearing at the entrance.

That sounds like a small thing. Someone decides to eat, goes to a restaurant, then returns to the street. But I'm curious about how much state that simple trip actually needs. A customer system can become a bit complicated for something that sounds so ordinary.

Crust & Crime is still under active development. This is a design question to think through, with the work still ahead.

## How little state is enough?

The next question I want to work through is the minimum state and transitions needed for that trip. What does a pedestrian need to keep track of when deciding to eat? What needs to change when they start travelling to a restaurant? And what lets them return to being a pedestrian afterwards?

One possible starting point would be to write out just those steps and check the transitions between them. Would each step need its own state? Could some share a state without making the behaviour hard to follow? Those are questions to test, rather than answers I have already settled on.

I think the interesting part is how small this can stay while still supporting the feeling of a living district. Just going somewhere to eat. Somehow, that already leaves quite a bit to think about.
