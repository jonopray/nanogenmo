nanogenmo
=========

Generate a novel, for the NaNoGenMo project

General plan of attack:
1. Generate a plot, by:
    * Create an environment with heirarchical structure and generated with a config file. {"port monsmouth" : {"castle" : {"gate", "king's chamber"}, "dock" : {"pier", "tavern"}}}
    * Create characters with different attributes {"loyal", "old", "weak", "wise", "royal", "Red team"}, {"young", "opportunist", "strong", "foolish", "Blue team"}. Draw from list of attributes to create.
    * Create objectives for the characters by combining their affiliations, personality, with things in the environment. 
        - generate_goals() -> {"protect family": {"find brother" : {"port monsmouth" : {"ask lord"}}, "protect brother" : {"requires" : {"with brother"}}}}. Fills out a couple top level goals completely? But what about changing environments?
        - choose_action() -> looks at goals and requirements and priorities and ease of doing. Picks highest prioritized goal divided by ease that is currently available. If the goal score is too low, perform refresh_goals(). If no sufficient action exists within a high priority top level goal, then generate a subgoal?
        - refresh_goals() -> adds a new top level goal?
        - Goals need 'priority', 'ease', 'requirement' fields. 'requirement' can be another goal, or it can be a bottom level action, like "get information from X person", "go to X location", "fight X person", "assist X person with their goal", "recruit X person to help self". 'ease' can be determined by personal modifiers
        - A dictionary of predefined goals should exist.
    * Determine interactions within scene by using motivations to draw them. 
2. Write the actual story, by plugging the actions generated in the plot into multi-level templating
    * Pick sentence types (sentence for action, sentence for describing something, sentence for this action)
    * Writing sentence types. generate_sentence(character, action, object)
3. Generate characters with goals and relationships.
   * Each character needs distinct personalities (generated on creation, with some development functions.)
