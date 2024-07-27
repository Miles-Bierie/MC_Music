use json::{self, object, JsonValue};
use lofty::file::AudioFile;
use std::fs::{self, File};
use std::io::{self, Read, Write};
use lofty::probe::Probe;
use std::path::Path;


fn main()
{
    // Ask user for the input file, as well as the name of the data pack / resource pack
    let mut user_input: String = String::new(); // Raw user input
    
    print!("Input file path: ");
    io::stdout().flush().expect("Could not flush stdout!");

    io::stdin().read_line(&mut user_input).expect("Could not parse input!");
    let data_file_path: String = String::from(user_input.trim()); // The path of the json file

    user_input.clear();

    print!("Pack Names: ");
    io::stdout().flush().expect("Could not flush stdout!");

    io::stdin().read_line(&mut user_input).expect("Could not parse input!");
    let pack_name: String = String::from(user_input.trim()); // The base name of the generated packs

    
    // Read in the data from the json file
    let mut file: File = File::open(data_file_path).expect("Could not open json file!"); // Reads in all files

    let mut json_data_raw:String = String::new();
    file.read_to_string(&mut json_data_raw).expect("Could not read json file!");


    let json_all: JsonValue = json::parse(&json_data_raw).unwrap(); // All json data is stored in here
    let json_songs: &JsonValue = &json_all["songs"];

    let datapack_format: u8 = if !json_all["data"]["pack_format"].is_null() {Option::expect(json_all["data"]["pack_format"].as_u8(), "Error!")} else {42 as u8};  // Grab pack format if specified
    let resourcepack_format: u8 = if !json_all["data"]["pack_format"].is_null() {Option::expect(json_all["data"]["pack_format"].as_u8(), "Error!")} else {42 as u8};
    let pack_description: &str = if !json_all["data"]["description"].is_null() {Option::expect(json_all["data"]["description"].as_str(), "Error!")} else {"Adds custom music discs to minecraft!"};  // Grab pack description if specified

    // Generate the data pack
    let song_dir: String = format!("./output/{}_datapack/data/{}/jukebox_song/", pack_name, pack_name.to_lowercase().replace(" ", "_")); // Keep track of directory for song file creation

    fs::create_dir_all(&song_dir).expect("Could not create datapack!");

    // Create pack.mcmeta
    let datapack_mcmeta_dump: String = 
    format!("
{{
    \"pack\": {{
        \"pack_format\": {},
        \"description\": \"{}\"
    }}
}}
", datapack_format, pack_description
    );

    let resourcepack_mcmeta_dump: String = 
    format!("
{{
    \"pack\": {{
        \"pack_format\": {},
        \"description\": \"{}\"
    }}
}}
", resourcepack_format, pack_description
    );
                                                                                                        // length of string "datapack"
    let mut meta_index: usize = Option::expect(song_dir.find("datapack/"), "Could not find index!") + 9;
    let mut mcmeta_path: &str = song_dir.split_at(meta_index).0;

    let mut mcmeta: File = File::create(mcmeta_path.to_string() + "pack.mcmeta").unwrap();
    mcmeta.write_all(datapack_mcmeta_dump.as_bytes()).expect("Could not generate mcmeta file for datapack!");

    for song in json_songs.entries()
    {
        // Grab song data from json file
        let comparator_output: &u8 = &song.1["power"].as_u8().unwrap();
        let description: &str = &song.1["description"].dump();
        // If a custom song duration is provided, use that; else calculate the length of the audio file
        let mut seconds: Option<u16> = song.1["seconds"].as_u16();
        if seconds.is_none() // Read audio file length
        {
            let file_path: &Path = Path::new(Option::expect(song.1["audio"].as_str(), "Could not find audio path!"));
            let audio_file = Probe::open(file_path).expect("Could not open file!").read().expect("Could not read file!");
            seconds = Option::from(audio_file.properties().duration().as_secs() as u16);
        }

        let mut song_file: File = File::create(song_dir.to_string() + song.0 + ".json").unwrap();

        let song_dump: String = String::from(
            format!("
{{
    \"comparator_output\": {},
    \"description\": 
        {},
    \"length_in_seconds\": {},
    \"sound_event\": {{
        \"sound_id\": \"{}\"
    }}
}}
", comparator_output, description, &Option::expect(Some(seconds), "Can't use seconds!").unwrap(), song.0)
            );

        song_file.write_all(song_dump.as_bytes()).expect("Could not write to file!");
    }

    // Generate the resource pack
    let song_file_dir: String = format!("./output/{}_resourcepack/assets/minecraft/sounds/", pack_name);
    fs::create_dir_all(&song_file_dir).expect("Unable to create custom sounds location!");

    let mut disc_texture_dir: String = String::new(); // So our code will compile
    let mut disc_model_dir: String = String::new();
    let mut disc_reroute_dir: String = String::new();

    if !json_all["data"]["item"].is_null()
    {
        disc_texture_dir = format!("./output/{}_resourcepack/assets/minecraft/textures/item/", pack_name);
        disc_model_dir = format!("./output/{}_resourcepack/assets/minecraft/models/item/", pack_name);
        disc_reroute_dir = format!("./output/{}_resourcepack/assets/minecraft/models/{}_models/", pack_name, pack_name.to_lowercase().replace(" ", "_"));
        fs::create_dir_all(&disc_texture_dir).expect("Unable to generate item texture location!");
        fs::create_dir_all(&disc_model_dir).expect("Unable to generate item model location!");
        fs::create_dir_all(&disc_reroute_dir).expect("Unable to generate item reroute location!");
    }
    
    meta_index = Option::expect(song_file_dir.find("resourcepack/"), "Could not find index!") + 13;
    mcmeta_path = &song_file_dir.split_at(meta_index).0;

    mcmeta = File::create(mcmeta_path.to_string() + "pack.mcmeta").unwrap();
    mcmeta.write_all(resourcepack_mcmeta_dump.as_bytes()).expect("Could not generate mcmeta file for resourcepack!");

    // Add sounds.json file
    let mut sounds_file: File = File::create(String::from(&song_file_dir[..&song_file_dir.len() - 7]) + "sounds.json").unwrap();

    let mut sound_obj: JsonValue = json::JsonValue::new_object();
    let mut model_obj: JsonValue = object! {
        "parent": "item/generated",
        "textures": {
            "layer0": format!("item/{}", json_all["data"]["item"])
        },
        "overrides": [
        ]
    };

    let mut model_overrides: JsonValue = json::JsonValue::new_array(); 

    let mut index: u16 = 0;

    for song in json_songs.entries()
    {
        let audio_location: &str = &song.1["audio"].as_str().unwrap().replace("\\", "/");
        let audio: &String = &String::from(Option::expect(String::from(audio_location.split_at(Option::expect(audio_location.rfind("/"), "Could not parse audio path!")).1).get(1..), "Could not parse audio name!"));
        std::fs::copy(&audio_location, String::from(&song_file_dir) + audio).expect("Could not copy audio file(s)!");

        // Add section to the sounds.json file
        sound_obj[song.0] = object!(
            "category": "record",
            "sounds": [{
                "name": audio.split_at(Option::expect(audio.rfind("."), "Could not split audio name from extension!")).0,
                "stream": true
            }]
        );

        // Add textures
        if !&song.1["texture"].is_empty()
        {
            let texture_location: &str = &song.1["texture"].as_str().unwrap().replace("\\", "/");
            let texture: &String = &String::from(Option::expect(String::from(texture_location.split_at(Option::expect(texture_location.rfind("/"), "Could not parse audio path!")).1).get(1..), "Could not parse audio name!"));
            std::fs::copy(&texture_location, (String::from(&disc_texture_dir) + texture).replace(" ", "_")).expect("Could not copy texture file(s)!");

            let texture_name: &str = texture.split_at(Option::expect(texture.rfind("."), "Could not split texture name from extension!")).0;
            // Add override to parent item file
            model_overrides[index as usize] =  object! {
                "predicate":{
                    "custom_model_data": song.1["model"].clone()
                },
                "model": format!("{}_models/{}", pack_name.to_lowercase().replace(" ", "_"), texture_name)
            };

            // Add reroute file
            let mut reroute_file: File = File::create(String::from(&disc_reroute_dir) + &String::from(texture_name) + &String::from(".json")).unwrap();
            
            let reroute_dump: JsonValue = object! {
                "parent": "item/generated",
                "textures": {
                    "layer0": format!("item/{}", texture_name)
                }
            };

            reroute_file.write_all(reroute_dump.dump().as_bytes()).expect("Could not write to texture reroute file!");
            index += 1; 
        }
    }
    model_obj["overrides"] = model_overrides;

    if !&json_all["data"]["item"].is_empty()
    {
        let mut item_file = File::create(String::from(&disc_model_dir) + json_all["data"]["item"].as_str().unwrap() + ".json").unwrap();
        item_file.write_all(&model_obj.dump().as_bytes()).expect("Could not write to file!");
    }

    sounds_file.write_all(&sound_obj.dump().as_bytes()).expect("Could not write to sounds.json!");

    println!("Sucessfully generated files!");

    println!("<Press RETURN to exit>");
    io::stdin().read_line(&mut user_input).expect("Idk how you could mess this up...");
}