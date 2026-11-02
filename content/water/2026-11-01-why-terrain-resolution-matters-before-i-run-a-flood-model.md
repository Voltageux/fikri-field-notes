---
title: Why terrain resolution matters before I run a flood model
date: 2026-11-01
description: Planning a comparison of coarse and fine terrain data before interpreting flood simulation results.
tags: Water Engineering, GIS, Flood Modelling
status: Research Plan
topic_id: water-dem-plan-20261101
---

## Before running the model

I have been thinking about how much the terrain data can affect a flood model before I even start changing the hydraulic settings. A model can look quite convincing on a map, but that does not automatically mean the underlying terrain is good enough for the question I am trying to answer.

One thing I want to compare is a coarse DEM against a finer one. The main question is how each one represents the river channel and the surrounding floodplain. Small changes in elevation or a channel that is poorly represented could affect where the simulated water goes.

## Keeping the comparison fair

If I do this properly, I would keep the other model settings as consistent as possible. Otherwise, it would be hard to tell whether a difference in the flood map came from the terrain or from something else in the setup.

I also want to write down the assumptions I need to check first: elevation reference, channel representation, any gaps or odd features in the DEM, and whether the data actually describe the area well enough.

## A question for a future test

This is still a plan, not a report of simulations I have completed. I am curious to see how much the input resolution matters, especially when two maps look similar at first glance. A nice-looking inundation map is useful, of course, but I want to understand what I can actually trust in it.
