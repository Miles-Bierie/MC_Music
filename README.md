# MC Music (My first rust program!!!)
### Allows you to add custom music to Minecraft as music discs

<br>

## How to Use

When you run the mc_music executable, it will prompt you for a file path, and then for a name. In order to tell the program how to create the data and resource pack, you will have to create a json file (see below). This is what the "Input file path: " is refering to. The "Pack Names: " is the name of the data/resource pack. After running, it will generate an output folder containing the generated datapack and resource pack.

## Json format
    {
        "songs": {
            "song_name_here": {
                "power": <0-15>,
                "audio": "path/to/audio.ogg",
                "description": {
                    "text":"Description goes here"
                }
                "texture": "path/to/texture.png"
                "model": <custom model data index>
            },
            "next_song_name_here": {
                <...>
            }
        },
        "data": {
            "pack_format": <pack_format>,
            "description": "<Pack description>",
            "item": "<item being retextured>"
        }
    }

### Songs:
&nbsp; This will contain all the songs / audio you want to add to minecraft. You can add as many as you want. Replace "song_name_here" with the in-game name of the audio (it does not have to match the audio file's name, but it cannot contain spaces or capital letters).

#### Power:
An integer from 0 to 15; the signal strength a comparator will output when reading this disk in the jukebox.

#### Audio:
The path to the audio file you want to add to minecraft. This can be located anywhere, as it will be automatically coppied into the resource pack. This cannot contain any spaces or capital letters, and must be a .ogg file.

#### Description:
This is the rainbow text that will be displayed when the jukebox begins to play the song.

#### Texture (optional):
If you want to add a custom texture for this song, you may specify a path to a .png file. Like the audio file, it will be copied over into the resource pack.

#### Model (optional, required if using custom texture for this song):
An integer representing the custom model data index that the item will have to have to display this texture.

<br>

### Data:
&nbsp; This contains data seperate from the audio, for creating the data and resource pack.

#### Pack Format (optional):
The pack format that both the datapack and the resource pack will use (will be seperated in the future). Default is 42.

#### Description (optional):
The description of the datapack and the resource pack will have. Default is "Adds custom music discs to minecraft!"

#### Item (optional, required if using custom textures on any song)
This is the item that will be retextured. This uses the internal item name. For example, type "music_disc_5" to retexture Disc 5, or "paper" to retexture paper.

## Notes:
- I will be making a python tool that will generate this json file automatically, but you will manually have to type this out for now.


