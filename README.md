Masters Project Pipeline Tools


DO NOT USE WITHOUT READING THE CODE
These tools where specifically tailored to our pipeline and may not work somewhere else.
The primary purpose of this repo is be a reference and inspiration for custom tools that fit YOUR pipeline.
The code should be pretty well documented in most areas. I will not do fixes on the code however, so if there is a problem you have to find it yourself.
Again, I don't guarantee that they work on your end right away.


TOOLS

Asset IO
This was the main asset tool for the project. It handles exporting, importing/referencing and managing assets. 

Cache IO
When lighting you only care about the geometry. That's what this tool is for. It exports alembics and uses .ma files to retain the materials.

Proxy Texture
We worked on Maya 2017, which has a texture clamp option in the viewport. But it sucks. 
So I made my own that actually writes new texture files and remaps the paths.

Quick Material Setup
Browse for a texture set. Select any one. Apply. This creates a new material with all the textures found in the the set and applies it to the selected object. Of course this only works with the correct naming convention. See the code for info.

Scene Checker
Before rendering you should really check all of your settings, so you don't try to get you renders only to realize you missed one critical setting. To reduce the strain of making sure to remember everything, this tool does it all for you. 

Vray Attribute Manager
This tool enables adding and modifying multiple vray objects on multiple objects.