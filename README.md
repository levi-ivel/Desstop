 Introduction
---
Desstop is a simple workspace based TODO app made with Tauri, SvelteKit and Bun.


Contributing
---
This project is open source, so feel free to add or remove whatever you like. You can also make a pull request so your changes can be added to Desstop itself, documentation on how to create a pull request can be found [here](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request)


Disclaimer
---
This project is still being worked on and is in a very early stage, expect frequent changes.

Some window managers may not accept the window settings, such as always on top and the positioning.

One example of this is Hyprland, you can minigate this by adding this to your hyprconfig:
```
windowrule = float 1, match:class ^(desstop)$
windowrule = move 0 0, match:class ^(desstop)$
windowrule = pin 1, match:class ^(desstop)$
windowrule = no_initial_focus 1, match:class ^(desstop)$
```
