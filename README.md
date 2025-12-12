### The Project Idea
As a mix between past-time and coding practice, I wanted to work on a roguelike game / story generator, the likes of dwarf fortress or caves of qud - a game that randomly creates a world, plays out detailed interactions between NPCs and derives playable
content from the current world state. Now, for starters I wanted to create worlds that are earthlike, i.e. that have oceans, continents, and smaller islands, that look like they could have originated on our planet at some point, and it turned
out that there is quite a bit more to our continents than meets the eye. The project contains some research notes and sources, scripts that randomly create a world as a coordinate system of datapoints, and some visualizations.

### Current State
The current master branch contains the first, functional version of my world generator, written purely in python. It currently creates a topography map and an overlapping mineralogy map for a given world seed. The topography and mineralogy are visualized using matplotlib. On a second branch ("performance"), I started to fully rewrite the whole thing in C++, as python begins to struggle with very detailed maps (200 x 200 pixels), since in the process of world creation, the dimensions are exponentially expanded multiple times, to add finer details - python does not support true multithreading, and is slow when handling its native data structures, after all. The C++ version currently runs, and some of the steps have been verified to run as intended, but there is currently no full visualization, therefore I was not able to test the validity of its final results. Yet.
Some examples of randomly created worlds will be added below.

### Technical Details
Here follows a brief description of the scientific models I used in my world generation, some of the sources I relied on are mentioned, the overall code structure, and a short explanation on how to create some worlds with this yourself.

#### Model Base
For my research about the very basic processes of land formation, I used a number of articles from [wikipedia.org](wikipedia.org), [geologyin.com](geologyin.com), [geologyscience.com](geologyscience.com) and [opengeology.org](opengeology.org). This is, in the briefest terms, how these sites explain land formation:
Earth's crust is split into large plates, called tectonic plates. These tectonic plates move around over time, driven partly by movements of the underlying magma. When they collide, land is formed by a number of different processes, like subduction or volcanism. The land that forms around plate boundaries spreads out over time, as plates move back and forth, however, direct plate boundaries typically feature very high mountain ranges, rich in volcanoes and minerals.
Additionally, different interactions between tectonic plates help the formation of metallic ores/minerals.
The information provided by the named sources goes into much further detail, any interested party should check them out. 

As a special shoutout, I would like to name [this blog](madelinejameswrites.com), where the author has created a worldbuilding guide for aspiring phantasy authors and does pretty much what I am trying to accomplish here, only with pencil and paper. The blog posts were a good point to search for additional sources, such as [this](youtube.com/@sprottedu2478) youtube channel, focused on metal ore formation. 
I had quite a bit of trouble finding good sources about metal ore formation at first, until I saw the sources mentioned on the blog, thanks :)

#### World Generation Steps
On a technical level, the world creation follows these steps:
- Creation of tectonic plate boundaries (handled by ```TectonicSplits``` objects)

  From randomly chosen start points, lines expand in a semi-random fashion, creating jagged boundaries until they hit the coordinate limits or another boundary
- Consolidation of plates using these boundaries (handled by ```TectonicPlates``` object)

  The coordinates claimed by each TectonicSplit object are consolidated into a single coordinate system. Using these boundaries, each coordinate is assigned the id number of its owner plate. Where tectonic plates meet, a coordinate is owned by multiple plates, with the lowest id being the priority owner. This is used later on for identifying coordinates at the boundary of a plate, while the actual plate boundaries have no actual dimensions.
- Simulation of tectonic plate movement

For this step, each coordinate contains a dictionary with numerical values for different rock types and ore deposits. Higher numerical values for rock types indicate land mass and the resulting height at a coordinate, while ore values are a comparative value, meant to symbolize where especially many instances of metal ore formation have occurred. Based on the heights for each coordinate, a general sea level can be calculated in periodic intervals, as this is relevant for some ore formations.

  The ```TectonicMovement``` object picks out a random plate, and determines a two-dimensional movement vector for it, using a ```MagmaCurrentMap``` object. For each coordinate owned by a plate, a movement vector is calculated based on its surrounding coordinates, and the sum of these vectors is applied to the entire plate (apparently, higher crust on a plate let less heat escape from earth's core, resulting in hot and cold spots underneath a tectonic plate, which results in slow magma currents that move the plate back and forth).
  Once the movement vector for a plate is calculated, each coordinate of the plate interacts with its neighbors based on that movement vector (this simulates land mass stored in one coordinate moving towards another). Special interactions occur at coordinates that are considered plate boundaries, such as subduction, or convergence/divergence, which result in special behavior (volcanism, ore formation, newly created land mass as magma between plates hits ocean water, etc.)
  After a set number of plate movements, the world is considered finished and a topography, and comparative mineralogy map can be created.

- Dimension expansion and blur

  The resulting maps still lack at lot of detail, and have very strong differences in heights between neighboring coordinates. To address this, I implemented my own basic gaussian blur, which also increases the dimensions for a map, to give it more detail while smoothing out the differences.


#### Test this Yourself

### Future Plans
The created worlds look a little too flat and round (mountain ranges look uniform, coastlines are not jagged enough), and I suspect that is both due to the relatively small scale of the coordinate systems being created, and to the fact that much of our natural topography is shaped by rivers and glaciers, which are currently not modeled.
Glaciers, rivers, the resulting climate zones, and vegetation are in planning.
