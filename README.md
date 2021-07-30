# runewatch

RuneScape packet watcher and notifier.
Currently only understands plaintext chatlog messages.

## Install
```sh
pip install git+https://github.com/ConnorNelson/runewatch
```

## Example Usage

### Fishing

```sh
runewatch -i enp4s0 -w 14 -c "play -q -n synth 0.1 sin 400" -n "You can't carry any more" -s "You catch" -t 10 -d 10
```

### Archaeology

```sh
runewatch -i enp4s0 -w 14 -c "play -q -n synth 0.1 sin 400" -n "(You find)|(You don't have enough inventory space)|(has depleted)" -s "You transport" -t 60 -d 10
```

### Cooking

```sh
runewatch -i enp4s0 -w 14 -c "play -q -n synth 0.1 sin 400" -s "(You successfully cook)|(You accidentally burn)" -t 3 -d 10
```

### Dungeoneering hole

```sh
runewatch -i enp4s0 -w 14 -c "play -q -n synth 0.1 sin 400" -n "(Well that was about 20 floors)|(You have reached the maximum temperature)"
```
