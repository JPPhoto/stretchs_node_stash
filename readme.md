# Stretch's Node Stash

A random collection of nodes for [InvokeAI](https://github.com/invoke-ai/InvokeAI)

## Install

- Manual
    - Hit the green Code button above and select Download ZIP.
    - Once downloaded extract the stretchs_node_stash folder in your invokeai/nodes folder.
    - Restart Invoke
- Git
    - Open a terminal/command prompt in the invokeai/nodes directory
    - enter `git clone https://github.com/TheCulprit/stretchs_node_stash.git`

## Node Breakdown

### Selectors

- `Integer Selector` - Takes two integer inputs and allows the user to decide which is used based on a toggle.
- `String Selector` - Same as above but for strings.

### Name Grabbers

- `Model Name Grabber` - A little awkward but takes input from a Model Identifier node and outputs the model's name.
- `LoRA Name Grabber` - Same as above but only for LoRAs. 

### LoRA Tools

- `LoRA Collection From Path` - Returns a collection of nodes that have a partial match to the given path. (Mostly useful if your loras are stored on disk in a categorised directory structure)
- `Lookup LoRA Triggers` - Takes input from a LoRA Selector node and outputs the trigger phrases that are defined for that LoRA in the model manager.
- `Random LoRA Mixer` - Takes a collection of LoRAs and returns a new, random collection based on the various input values.
- `Merge LoRA Collections` - Takes two collections of LoRAs and merges them into one Collection.
- `Reapply LoRA Weight` - Allows the setting of a LoRA's weight after it has been selected.

### String Tools

- `String Collection Joiner` - Takes in a Collection of of strings and returns a single string with all the entries separated by the given delimeter.
- `Load Text File To String` - Loads a file at the given path as a string and outputs it.
- `Load All Text Files In Folder` - Loads all files in the given directory which have the given extension as strings and returns them as a Collection of strings.
- `Merge String Collections` - Takes two collections of strings and merges them into one Collection.

### Debug Tools

- `Print String to Console` - Just prints the input string to the console in the selected colour combination. (Useful for quickly debugging string manipulations.)

### Tracery

- `Tracery` - Implement's Kate Compton's [Tracery](http://tracery.io/) as an Invoke node. 
    - Tracery is a simple grammar system which can replace #tokens# with random elements from a given grammar.
    - Grammars are input as a collection of JSON strings which will be merged. Any duplicate grammar entries may be lost. 
    - The given prompt will be expanded and it's #tokens# replaced with random entries from the grammar. 
    - Example Grammar:
        ```json
        {
            "subject": [ "young woman", "old woman", "small puppy"],
            "food": [ "#main_course#", "#dessert#" ],
            "main_course": [ "steak and potatoes", "burger and fries", "spaghetti" ],
            "dessert": [ "ice cream", "chocolate bar", "nachas" ]
        }
    - Example Prompt:
        ```
        A photograph of #subject# eating #food#
    - Example Output:
        ```
        A small puppy eating burger and fries
    - Modifiers:
        - Modifers can be applied to tokens to vary the output by writing a `.` and the name of the modifier after the token. `#token.modifier#`. If a modifier takes arguments they go in brackets after the modifier name. `#token.modifier(argument1,argument2)#`
        - Available modifiers
            - ran - *Will only add the exapanded text to the output if a random chance is met*
                - Random chance must be given as an integer value out of 100
                - Usage: `#token.ran(50)#` for a 50 percent chance. 
            - replace - *Replaces some of the expanded output*
                - Usage: `#token.replace(thin,fat)` will replace any instance of `thin` in the expanded output with `fat`
        - If the resulting expanded text contains your token as `((token))` then it failed to find that token in the grammar and there may be an issue with your grammar.
        - This node implements [Tracery](http://tracery.io/) by Kate Compton, using code from the [Python version](https://github.com/aparrish/pytracery) by Allison Parrish.

## Examples
Integer selector to toggle between a random or fixed seed.

![Integer Selector Example](images/int_selector.png)

Grabbing the name from a model.

![Model Name Grabber Example](images/model_name_grabber.png)

Merging LoRA Collections.

![Merge LoRA Collections Example](images/merge_lora_collections.png)

Looking up trigger phrases for a LoRA

![Lookup LoRA Triggers Example](images/lookup_lora_triggers.png)

Adding LoRAs to a Random LoRA Mixer

![Random LoRA Mixer 1](images/lora_mixer_1.png)

Selecting LoRAs for the LoRA mixer using LoRA Collections from Path and inserting the trigger phrases into the prompt.

![Random LoRA Mixer 2](images/lora_mixer_2.png)

Simplest Tracery example.

![Tracery Example 1](images/tracery_1.png)

Loading Tracery grammars from a directory.

![Tracery Example 2](images/tracery_2.png)

## License
This port uses code from the python port of Tracery by Allison Parish and therefore inherits the Apache License 2.0

```
    Tracery node Based on code by Allison Parrish and Kate Compton

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.`