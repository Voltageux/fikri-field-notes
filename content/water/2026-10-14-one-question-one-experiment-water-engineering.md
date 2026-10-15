---
title: One question, one experiment: A water engineering notebook
date: 2026-10-14
description: Practical GIS, hydrology, HEC-RAS, and computational hydraulics, investigated one reproducible question at a time.
tags: Water engineering, GIS, HEC-RAS, Hydrology, Python
status: Introduction
---

Water engineering has a useful way of keeping you humble. A beautiful flood map is not necessarily a reliable flood map. A model that runs without crashing is not necessarily a model that represents a river well. And a small assumption about terrain, roughness, or boundary conditions can change the story you think the results are telling.

My background is in **civil and environmental engineering**, especially water resources, hydrology, hydraulic modeling, and computational research. I created this notebook to keep exploring those subjects through small, practical investigations that others can follow.

The idea is simple: **one question, one experiment**. Not every entry needs to be a major paper or a polished breakthrough. A well-documented failed simulation, a terrain-processing mistake, or a clever Python script can be worth sharing.

## What I'll work on

Some recurring themes will be:

- **GIS and spatial data:** using QGIS and Python to prepare elevation models, delineate catchments, inspect terrain, and create maps that communicate more than just attractive colors.
- **River hydraulics:** investigating 1D and 2D HEC-RAS setups, mesh resolution, roughness, boundary conditions, numerical stability, and the interpretation of water levels and velocities.
- **Hydrology and flood studies:** rainfall, runoff, hydrographs, flood extent, and sensitivity to uncertain input data.
- **Computational tools:** using Python and, where appropriate, SRH-2D, OpenFOAM, or other modeling software to compare methods and automate repetitive tasks.

I want these to be *working notes*, not a collection of impressive-sounding software names. Every tool should answer a specific question.

## How an experiment will be documented

Whenever possible, each article will follow the same structure: the engineering question, the data and assumptions, the method, what happened, what remains uncertain, and what I would test next. I'll share reproducible code, configuration examples, and figures when licensing and confidentiality allow it.

I'll also distinguish **demonstration models** from validated studies. A tutorial using open data may show a useful method, but it should not be mistaken for a site-specific engineering assessment or design recommendation.

## Where I'll begin

My first candidate experiment is a compact GIS terrain-preparation workflow: obtain an appropriately licensed elevation dataset, inspect its resolution and coordinate system, prepare it in QGIS or Python, and document the choices that affect subsequent hydraulic modeling.

From there, we can ask better questions about hydraulic mesh size, model sensitivity, computational cost, and what is actually supported by the data.

This journal is for the questions that come before the figures, the figures that challenge our assumptions, and the methods worth keeping for the next project.

**Welcome to my water engineering notebook.**
