# Database Workflow

## TODO

- rename groupby_style_desc_style column names
- rename 'style_desc' to 'style_definition' or something to that effect.

## Introduction

I have developed a workflow for aggregating the AOP information stored in the Guildsomm Compendium. It is based around tabulating the compendium and aggregating styles, with the result being a grouping of AOPs by common styles. For example in the Southern Rhone there is a number of AOPs who produce a GSM, but with different rules about the proportions of the individual varietals in the blend. Through this workflow we can produce a count of the AOP who can produce a GSM, and reveal AOPs who are adjacent, i.e. produce a GSM that can also use Cinsault, Carignan, etc. An example is shown below:

| first(style) | first(style_desc)    | count(style_desc) | group_concat(aop)                                           |
| ------------ | -------------------- | ----------------: | ----------------------------------------------------------- |
| rose         | grenache             |                 1 | tavel                                                       |
| rose         | grenache syrah blend |                 1 | cotes du vivarais                                           |
| rose         | gsc                  |                 1 | grignan-les-adhemar                                         |
| rose         | gsm                  |                 4 | costieres de nimes,cotes du rhone-villages,gigondas,luberon |
| rose         | gsm+c                |                 2 | lirac,vacqueyras                                            |
| rose         | gsm+c+c              |                 2 | duche d'Uzes,ventoux                                        |

As we can see, the count for each 'style_desc' is provided, as is the names of each of the AOP within the group. This is an excellent basis by which to analyse the various AOP of a region as with a little data cleaning and user interpretation, clear relationships between AOP, varietals and styles is revealed.

## Workflow

The workflow is as follows:

1. construct a table with the following columns:

1. aop: name of the AOP
1. style: type of style, i.e. blanc, rouge, rose
1. style_blend: the definition of the style.

For example:

| aop                     | style     | style_blend                                       |
| ----------------------- | --------- | ------------------------------------------------- |
| grignan-les-adhemar     | blanc     | min 30% viognier, grenache blanc, marsanne        |
| grignan-les-adhemar     | rouge     | min 70% grenache and syrah                        |
| grignan-les-adhemar     | rose      | min 70% grenache, syrah and cinsault              |
| beaumes-de-venise       | rouge     | min 80% blend of Grenache and Syrah               |
| clairette de bellegarde | blanc     | clairette                                         |
| gigondas                | blanc     | Min 70% Clairette Blanc                           |
| rasteau                 | vdn blanc | Grenache Blanc and Grenache Gris                  |
| rasteau                 | vdn ambre | Grenache Noir, Grenache Gris, Grenache Blanc      |
| rasteau                 | vdn rose  | Grenache Noir, Grenache Gris, Grenache Blanc      |
| ventoux                 | blanc     | Bourboulenc, Clairette, Grenache Blanc, Roussanne |

2. From style blend, begin to define individual styles, for example for aop='grignan-les-adhemar', style='blanc' we can call the style a vgm.
3. Through an iterative process we should form clusters of rows with the same style or similar enough that we have subjectively determined them to be the same, and the result looks like this:

| aop                     | style | style_blend                                | style_desc           |
| ----------------------- | ----- | ------------------------------------------ | -------------------- |
| grignan-les-adhemar     | blanc | min 30% viognier, grenache blanc, marsanne | vgm                  |
| grignan-les-adhemar     | rouge | min 70% grenache and syrah                 | grenache syrah blend |
| grignan-les-adhemar     | rose  | min 70% grenache, syrah and cinsault       | gsc                  |
| beaumes-de-venise       | rouge | min 80% blend of Grenache and Syrah        | grenache syrah blend |
| clairette de bellegarde | blanc | clairette                                  | clairette            |

4. Now its ready for aggregation. One aggregation will be how many AOP create the same style. I have defined a group by macro called `groupby_style_desc_style(style_val)` which filters the table to a `style` value then aggregates by style_desc. The result looks like this:

| first(style) | first(style_desc)    | count(style_desc) | group_concat(aop)                                                                |
| ------------ | -------------------- | ----------------: | -------------------------------------------------------------------------------- |
| rouge        | cdp rogue blend      |                 1 | chateauneuf-du-pape                                                              |
| rouge        | grenache syrah blend |                 2 | grignan-les-adhemar,beaumes-de-venise                                            |
| rouge        | gsm                  |                 6 | costieres de nimes,cotes du rhone-villages,gigondas,luberon,vacqueyras,vinsobres |
| rouge        | gsm+c                |                 1 | lirac                                                                            |
| rouge        | gsm+c+c              |                 2 | duche d'Uzes,ventoux                                                             |
| rouge        | rouge                |                 1 | rasteau                                                                          |
| rouge        | syrah blend          |                 1 | cotes du vivarais                                                                |

Where the count of AOPs for the style are listed as `count(style_desc)` and the actual AOP names under `group_concat(aop)`. Furthermore we can see relationships between similar style_desc groups, i.e. 'gsm', 'gsm+c' and 'gsm+c+c' are all very closely related and really should be considered one group.
