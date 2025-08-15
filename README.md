# RE JCNs Editor #
RE JCNs Editor is a Blender (3.0+) addon for editing JCNs (Joint Constraints) files from most RE Engine games. <br>
This addon is currently work in progress. Some features are not available. <br>

Research about JCNs (and other files) can be found [here](https://github.com/XenonBaruku/MHWs-Research-Templates)

# Current Status
VERSION: 0.0.3 - dev <br>
(:heavy_check_mark: – Finished; :heavy_exclamation_mark: – Partially; :x: – Not implemented)

## Games
| JCNs Version | Game                            | Import                   | Export    |
| ------       | ------                          | ------                   | ------    |
| 11           | Resident Evil 2 Remake          | :heavy_exclamation_mark: | :x:       |
| 12           | Resident Evil 3 Remake          | :heavy_exclamation_mark: | :x:       |
| 16           | Resident Evil 8                 | :heavy_exclamation_mark: | :x:       |
| 21           | Monster Hunter Rise Sunbreak    | :heavy_exclamation_mark: | :x:       |
| 22           | Resident Evil 4 Remake          | :heavy_exclamation_mark: | :x:       |
| 29           | Monster Hunter Wilds            | :heavy_exclamation_mark: | :x:       |

## Structures
| ID     | Description             | Import                   | Export    |
| ------ | ------                  | ------                   | ------    |
| 0      | General constraints     | :heavy_check_mark:       | :x:       |
| 1      | Unknown joints          | :x:                      | :x:       |
| 2      | Simple constraints (?)  | :heavy_check_mark:       | :x:       |
| 3      | Aim constraints         | :x:                      | :x:       |
| 4      | ?                       | :x:                      | :x:       |


# Credits
 * Some codes in this addon come from [RE-Mesh-Editor](https://github.com/NSACloud/RE-Mesh-Editor) and [RE-Chain-Editor](https://github.com/NSACloud/RE-Chain-Editor) by [NSACloud](https://github.com/NSACloud).
 * Thank [Feuleur](https://github.com/Feuleur) for providing some infomation about constraints and the codes to generate 32-bit MurmurHash 3.