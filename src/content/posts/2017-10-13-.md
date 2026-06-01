---
title: "Determining the importance of predictors for health psychology questions"
description: "Determining the importance of predictors for health psychology questions"
published: 2017-10-13
lang: en
vetting_status: pending
migration_source: mattiheino-wp
draft: true
tags: ['o-data-punk-english']
wp_guid: "http://mattiheino.com/?p=3400"
---
There was a recent paper (ciber) and an ensuing [discussion](https://www.facebook.com/groups/853552931365745/permalink/1516842518370113/) on Facebook about the importance of determintants and how to determine it...
Eiko Fried pointed out
 Depression and anxiety are correlated, and there are different explanations. One is that they overlap in symptoms (MDD and GAD share 4 DSM criterion symptoms), so if a person endorses one, the person will with increased likelyhood also endorse the other. It's like having 2 personality subscales, where both subscales to 40% have the same items, and then including them in a prediction model. There are many other explanations (and some disorders co-occur without sharing symptoms of course), and depending on why you think that is, you would want to control for that or not. Imagine only the symptoms that are unique to MD relate to a criterion like mortality, and not the symptoms only unique to GAD, or the shared symptoms. What would happen if you include both as predictors? What if you use them in separate regression? Now change it around, what if only the shared symptoms predict an outcome? I strongly recommend simulating this, it's done in a few seconds and shared/unique variance experiments can often have counterintuitive outcomes.
And what with the case for disorders are related but do not share content? That certainly happens (female gender and neuroticism are correlated ~0.4, but do not share items). What if only female sex is predictive of the criterion in the true model, and not neuroticism, but you do not include female sex in the model and only predict the criterion with neuroticism? You get a spurious association. And so forth.
--
"important is that we mis-estimate colliders in networks. so if data come from a model where A causes C and B causes C (collider), including C in the model will induce a spurious negative edge between A and B. ​"
Dalege et al's causal attitude network paper: general strive for consistency and minimising energy expenditure means neighbouring nodes cause a node to have the a congruent value. So, what happens if being afraid causes being angry, and disgust causes anger likewise? Collider?
Anger causes restricted affect, negative beliefs cause restricted affect -> anger and negative beliefs have a connection?
So, we shouldn't put outcomes into networks at all? Also, we shouldn't put intention items into attitude networks (RAA).
