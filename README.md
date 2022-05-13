# prsw-minecraft-launcher

Simple and lightweight Minecraft launcher with basic Vanilla launch capabilities.

When opening for the first time, run install.bat first, then launch the launcher with launch.bat.

Some things to keep in mind:
<ul><li>The launcher only works while online.</li>
  <li>Instance names are folder names, name them accordingly.</li>
  <li>Instance names cannot be edited (at least for now), choose wisely the first time.</li>
  <li>Whenever saving something, it is best practice to reopen the launcher. Most data is stored in files which aren't constantly reloaded.</li>
  <li>Instance downloading is slow (single-threaded) and the log is clunky, but you can scroll faster using scroll click.</li>
  <li>If you want to share game files for any reason, be aware that accounts.json probably contains your Minecraft access token, which could be used to hijack your account.</li>
  <li>The launcher not responding usually means that it's working on something. It's nothing to worry about.</li>
  <li>Minecraft will close if either the cmd window or launcher is closed. This way of closing may corrupt world files, prefer the in-game quit button.</li></ul>
  
  The launcher has been tested with versions 1.18.2 and 1.8.9, but most release versions and modern snapshots should work in theory.
