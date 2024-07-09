# MC Music (My first rust program!!!)
### Allows you to add custom music to Minecraft as music discs

<br>

## How to Use

When you run the mc_music executable, it will prompt you for a file path, and then for a name. In order to tell the program how to create the data and resourcepack, you will have to create a json file (see below). This is what the "Input file path: " is refering to. The "Pack Names: " is the name of the data/resourcepack. After running, it will generate an output folder containing the generated datapack and resourcepack. If you see a message saying "Sucessfully generated files!", all went well! Else, something went wrong, and you should make sure the json file is formatted correctly, and that all referenced files exist.

## Json format
    {
        "songs": {
            "<song_name_here>": {
                "power": <0-15>,
                "audio": "path/to/audio.ogg",
                "description": {
                    "text":"<Description goes here>"
                }
                "texture": "path/to/texture.png"
                "model": <custom model data index>
            },
            "<next_song_name_here>": {
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
The path to the audio file you want to add to minecraft. This can be located anywhere, as it will be automatically coppied into the resourcepack. This cannot contain any spaces or capital letters, and must be a .ogg file.

#### Description:
This is the rainbow text that will be displayed when the jukebox begins to play the song.

#### Texture (optional):
If you want to add a custom texture for this song, you may specify a path to a .png file. Like the audio file, it will be copied over into the resourcepack.

#### Model (optional, required if using custom texture for this song):
An integer representing the custom model data index that the item will have to have to display this texture.

<br>

### Data:
&nbsp; This contains data seperate from the audio, for creating the data and resourcepack.

#### Pack Format (optional):
The pack format that both the datapack and the resourcepack will use (will be seperated in the future). Default is 42.

#### Description (optional):
The description of the datapack and the resourcepack will have. Default is "Adds custom music discs to minecraft!"

#### Item (optional, required if using custom textures on any song)
This is the item that will be retextured. This uses the internal item name. For example, type "music_disc_5" to retexture Disc 5, or "paper" to retexture paper.


## In-Game Usage
&nbsp; After adding your datapack, you should see an "experimental settings" warning message when loading into your world (if you add the datapack while your world is open, exit and re-enter your world). You may press "I know what I'm doing", or feel free to make a backup. Make sure your resourcepack is applied, and then type in the following command:

    /give @s <item>[custom_model_data=<Your model data index here>, jukebox_playable={song:<namespace>:<song>}]

- Replace \<item\> with the item you want to use as your music disc. If you specified any custom textures, use the item you specified in the data section of the json file.
- Replace \<Your model data index here\> with the custom model data you specified for the song you want the disc of, if you are using a custom texture. If you are not using a custom texture, you can omit the custom_model_data component entirely.
- Replace \<namespace\> with the name you gave your datapack and resourcepack. This is the name that the program aske you. This name is not specified in the json file! If you included any capital letters or spaces in your name, type everything in lowercase, and replace spaces with '_' (underscores).
- Replace \<song\> with the name of the song you want to use. This is the song in the "song name here" section of the json file.

<br>

### Example:
&nbsp; Say you make the following json file called dog_adder.json that adds the song Dog into minecraft:

    {
    "songs": {
        "dog": {
            "power": 7,
            "audio": "./music_folder/dog.ogg",
            "description": {
                "text": "C418 - Dog"
            },
            "texture": "./texture_folder/dog_texture.png",
            "model": 1
        }
    },
    "data": {
        "pack_foramt": 42,
        "description": "Adds the song Dog by C418 to minecraft!",
        "item": "music_disc_cat"
    }
}


After typing this  out, you would then run the MC_Music.exe file.

    Input file path: ./dog_adder.json

Then, you call it something memorable

    Input file path: ./dog_adder.json
    Pack Names: dog_disc

If all goes well, you should see an output that looks like this:

    Input file path: ./dog_adder.json
    Pack Names: dog_disc
    Sucessfully generated files!
    <Press RETURN to exit>

There will now be a folder called "output" in the same directory, and it will contain both the datapack and the resource pack.

After selecting the resource pack and adding the datapack to your world, you would run this command:

    /give @s minecraft:music_disc_cat[custom_model_data=1, jukebox_playable={song:"dog_disc:dog"}]

And the music disc should appear in your inventory.

If you don't want any custom textures, dog_adder.json would look something like this:

    {
        "songs": {
            "dog": {
                "power": 7,
                "audio": "./music_folder/dog.ogg",
                "description": {
                    "text": "C418 - Dog"
                }
            }
        },
        "data": {
            "pack_foramt": 42,
            "description": "Adds the song Dog by C418 to minecraft!"
        }
    }

And you would type in:

    /give @s minecraft:music_disc_cat[jukebox_playable={song:"dog_disc:dog"}]

## Notes:
- I will be making a GUI-based python tool that will generate this json file automatically, but you will manually have to type this out for now.


